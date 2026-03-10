#!/usr/bin/env python3
"""
Doc page chat agent service.

Provides a pydantic-ai powered CodeWikiAgent with:
1) Read-only code access
2) Writable documentation access for markdown files
3) A bash tool executed in a constrained session workspace
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import secrets
import shlex
import shutil
import subprocess
import threading
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Callable, AsyncIterator

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelSettings
from pydantic_ai.providers.openai import OpenAIProvider

from codewiki.src.utils import file_manager
from .config import WebAppConfig
from .github_processor import GitHubRepoProcessor

logger = logging.getLogger(__name__)
MAX_TOOL_RELPATH_CHARS = 512


def _clip_text(value: str, max_chars: int = 12_000) -> str:
    if len(value) <= max_chars:
        return value
    omitted = len(value) - max_chars
    return f"{value[:max_chars]}\n\n... [truncated {omitted} chars]"


def _normalize_relpath(raw_path: Any) -> str:
    normalized = str(raw_path or "").strip().replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.strip("/")


def _sanitize_current_page_path(raw_path: str) -> str:
    value = _normalize_relpath(raw_path)
    if not value:
        return "overview.md"
    if len(value) > 260:
        return "overview.md"
    if any(ch in value for ch in ("\n", "\r", "\x00")):
        return "overview.md"
    if _looks_like_markdown_blob(value):
        return "overview.md"
    return value


def _looks_like_markdown_blob(value: str) -> bool:
    text = (value or "").lstrip()
    if not text:
        return False
    return text.startswith("#") or "```" in text or "\n\n" in text


def _resolve_under(base: Path, rel_path: str) -> Path:
    normalized = _normalize_relpath(rel_path)
    if not normalized:
        raise ValueError("Path is empty")
    if len(normalized) > MAX_TOOL_RELPATH_CHARS:
        raise ValueError("Path is too long")
    if any(ch in normalized for ch in ("\n", "\r", "\x00")):
        raise ValueError("Path must be single-line text")
    if _looks_like_markdown_blob(normalized):
        raise ValueError("Path looks like markdown content, not a file path")
    try:
        candidate = (base / normalized).resolve()
    except OSError as exc:
        raise ValueError(f"Invalid path: {exc}") from exc
    if not candidate.is_relative_to(base.resolve()):
        raise ValueError("Path escapes allowed workspace")
    return candidate


@dataclass
class _ChatSession:
    session_id: str
    job_id: str
    repo_url: str
    docs_dir: Path
    current_page: str
    created_at: datetime
    updated_at: datetime
    sandbox_root: Path
    workspace_dir: Path
    repo_root_dir: Optional[Path] = None
    repo_dir: Optional[Path] = None
    subproject_path: str = ""
    temp_user: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)
    trace_events: list[dict[str, Any]] = field(default_factory=list)
    model_name: str = ""
    event_emitter: Optional[Callable[[dict[str, Any]], None]] = None
    is_running: bool = False
    run_started_at: str = ""
    run_finished_at: str = ""


@dataclass
class _ChatDeps:
    service: "CodeWikiChatService"
    session: _ChatSession


async def _list_docs_tool(ctx: RunContext[_ChatDeps], subpath: str = "", limit: int = 200) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "list_docs",
        {"subpath": subpath, "limit": limit},
    )
    docs_root = ctx.deps.session.docs_dir
    try:
        target = _resolve_under(docs_root, subpath or ".")
        if not target.exists():
            result = f"Path not found: {target}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result
        if target.is_file():
            result = str(target.relative_to(docs_root))
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        rows: list[str] = []
        for path in sorted(target.rglob("*")):
            if len(rows) >= max(1, limit):
                break
            rel = path.relative_to(docs_root).as_posix()
            prefix = "d" if path.is_dir() else "f"
            rows.append(f"[{prefix}] {rel}")
        result = "\n".join(rows) if rows else "No files found"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _read_doc_tool(ctx: RunContext[_ChatDeps], relative_path: str) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "read_doc",
        {"relative_path": relative_path},
    )
    docs_root = ctx.deps.session.docs_dir
    try:
        target = _resolve_under(docs_root, relative_path)
        if not target.exists() or not target.is_file():
            result = f"Document not found: {relative_path}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result
        if target.suffix.lower() not in {".md", ".txt", ".json"}:
            result = f"Unsupported doc file type: {target.suffix}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result
        result = _clip_text(file_manager.load_text(target), WebAppConfig.CHAT_MAX_TOOL_OUTPUT_CHARS)
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _write_doc_tool(
    ctx: RunContext[_ChatDeps],
    relative_path: str,
    content: str,
    mode: str = "overwrite",
) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "write_doc",
        {
            "relative_path": relative_path,
            "mode": mode,
            "content_chars": len(content or ""),
        },
    )
    docs_root = ctx.deps.session.docs_dir
    try:
        normalized_mode = (mode or "overwrite").strip().lower()
        if normalized_mode not in {"overwrite", "append"}:
            result = "Unsupported mode, expected overwrite|append."
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        target = _resolve_under(docs_root, relative_path)
        if target.suffix.lower() not in {".md", ".markdown"}:
            result = "Only markdown files can be modified (.md/.markdown)."
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        target.parent.mkdir(parents=True, exist_ok=True)
        text = str(content or "")
        if normalized_mode == "append":
            with target.open("a", encoding="utf-8") as fp:
                fp.write(text)
        else:
            file_manager.save_text(target, text)

        rel = target.relative_to(docs_root).as_posix()
        result = (
            f"Updated document: {rel}\n"
            f"mode={normalized_mode}\n"
            f"chars={len(text)}"
        )
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _list_code_tool(ctx: RunContext[_ChatDeps], subpath: str = "", limit: int = 400) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "list_code_files",
        {"subpath": subpath, "limit": limit},
    )
    repo_root = ctx.deps.session.repo_dir
    try:
        if not repo_root or not repo_root.exists():
            result = "Code repository is unavailable for this chat session."
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        target = _resolve_under(repo_root, subpath or ".")
        if not target.exists():
            result = f"Path not found: {target}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result
        if target.is_file():
            result = str(target.relative_to(repo_root))
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        rows: list[str] = []
        for path in sorted(target.rglob("*")):
            if len(rows) >= max(1, limit):
                break
            rel = path.relative_to(repo_root).as_posix()
            prefix = "d" if path.is_dir() else "f"
            rows.append(f"[{prefix}] {rel}")
        result = "\n".join(rows) if rows else "No files found"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _read_code_tool(
    ctx: RunContext[_ChatDeps],
    relative_path: str,
    start_line: int = 1,
    end_line: int = 220,
) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "read_code",
        {"relative_path": relative_path, "start_line": start_line, "end_line": end_line},
    )
    repo_root = ctx.deps.session.repo_dir
    try:
        if not repo_root or not repo_root.exists():
            result = "Code repository is unavailable for this chat session."
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        target = _resolve_under(repo_root, relative_path)
        if not target.exists() or not target.is_file():
            result = f"Code file not found: {relative_path}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        text = file_manager.load_text(target)
        lines = text.splitlines()
        line_count = len(lines)
        lo = max(1, start_line)
        hi = min(max(lo, end_line), line_count)
        selected = lines[lo - 1 : hi]
        numbered = [f"{idx + lo:>5} | {line}" for idx, line in enumerate(selected)]
        payload = "\n".join(numbered) if numbered else ""
        header = f"# {target.relative_to(repo_root).as_posix()} ({lo}-{hi}/{line_count})"
        result = _clip_text(f"{header}\n{payload}", WebAppConfig.CHAT_MAX_TOOL_OUTPUT_CHARS)
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _grep_code_tool(
    ctx: RunContext[_ChatDeps],
    pattern: str,
    subpath: str = "",
    limit: int = 80,
) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "grep_code",
        {"pattern": pattern, "subpath": subpath, "limit": limit},
    )
    repo_root = ctx.deps.session.repo_dir
    try:
        if not repo_root or not repo_root.exists():
            result = "Code repository is unavailable for this chat session."
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        target = _resolve_under(repo_root, subpath or ".")
        if not target.exists():
            result = f"Path not found: {target}"
            ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
            return result

        regex = re.compile(pattern)
        rows: list[str] = []
        for path in sorted(target.rglob("*")):
            if not path.is_file():
                continue
            try:
                text = file_manager.load_text(path)
            except Exception:
                continue
            for idx, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    rel = path.relative_to(repo_root).as_posix()
                    rows.append(f"{rel}:{idx}: {line.strip()}")
                    if len(rows) >= max(1, limit):
                        result = "\n".join(rows)
                        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
                        return result
        result = "\n".join(rows) if rows else "No matches found."
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


async def _run_bash_tool(
    ctx: RunContext[_ChatDeps],
    command: str,
    timeout_seconds: int = 20,
) -> str:
    trace_id = ctx.deps.service.trace_tool_start(
        ctx.deps.session,
        "bash",
        {"command": command, "timeout_seconds": timeout_seconds},
    )
    try:
        result = ctx.deps.service.run_shell_command(
            session=ctx.deps.session,
            command=command,
            timeout_seconds=timeout_seconds,
        )
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=True)
        return result
    except Exception as exc:
        result = f"Tool failed: {exc}"
        ctx.deps.service.trace_tool_end(ctx.deps.session, trace_id, result, ok=False)
        return result


class CodeWikiChatService:
    """Stateful chat service for generated documentation pages."""

    def __init__(self, background_worker, cache_manager):
        self.background_worker = background_worker
        self.cache_manager = cache_manager
        self._sessions: dict[str, _ChatSession] = {}
        self._lock = threading.RLock()
        self._provider = OpenAIProvider(
            base_url=WebAppConfig.AGENT_MODEL_BASE_URL,
            api_key=WebAppConfig.AGENT_MODEL_API_KEY,
        )

    def _serialize_trace_payload(self, payload: Any, max_chars: int = 1400) -> str:
        if payload is None:
            return ""
        try:
            text = json.dumps(payload, ensure_ascii=False, indent=2)
        except Exception:
            text = str(payload)
        return _clip_text(text, max_chars)

    def _append_history_message(
        self,
        session: _ChatSession,
        role: str,
        content: str,
        *,
        events: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        item: dict[str, Any] = {
            "role": (role or "").strip().lower() or "assistant",
            "content": str(content or ""),
            "timestamp": datetime.now().isoformat(),
        }
        if events is not None:
            item["events"] = [dict(event) for event in events if isinstance(event, dict)]
        session.history.append(item)

    def _emit_live_event(self, session: _ChatSession, payload: dict[str, Any]) -> None:
        emitter = session.event_emitter
        if not emitter:
            return
        try:
            emitter(dict(payload))
        except Exception:
            logger.debug("Failed to emit live trace event", exc_info=True)

    def _push_trace_event(
        self,
        session: _ChatSession,
        event_type: str,
        title: str,
        content: str,
        collapsed: bool = True,
        **extra: Any,
    ) -> int:
        started_at = datetime.now().isoformat()
        event = {
            "type": event_type,
            "title": title,
            "content": _clip_text(str(content or ""), 6000),
            "collapsed": collapsed,
            "timestamp": started_at,
            "started_at": started_at,
            "duration_ms": 0,
        }
        event.update(extra)
        session.trace_events.append(event)
        session.updated_at = datetime.now()
        index = len(session.trace_events) - 1
        self._emit_live_event(
            session,
            {
                "type": "trace.append",
                "index": index,
                "event": dict(event),
            },
        )
        return index

    def trace_tool_start(self, session: _ChatSession, tool_name: str, payload: Optional[dict[str, Any]] = None) -> int:
        return self._push_trace_event(
            session=session,
            event_type="tool",
            title=f"工具调用: {tool_name}",
            content="执行中...",
            collapsed=True,
            tool_name=tool_name,
            status="running",
            input=self._serialize_trace_payload(payload),
        )

    def trace_tool_end(self, session: _ChatSession, trace_id: int, output: str, ok: bool = True) -> None:
        status = "ok" if ok else "error"
        clipped_output = _clip_text(str(output or ""), 4500)
        if 0 <= trace_id < len(session.trace_events):
            event = session.trace_events[trace_id]
            if isinstance(event, dict) and event.get("type") == "tool":
                started_at_raw = str(event.get("started_at") or event.get("timestamp") or "")
                duration_ms = 0
                if started_at_raw:
                    try:
                        started_dt = datetime.fromisoformat(started_at_raw)
                        duration_ms = max(0, int((datetime.now() - started_dt).total_seconds() * 1000))
                    except Exception:
                        duration_ms = 0
                event["status"] = status
                event["content"] = clipped_output
                event["finished_at"] = datetime.now().isoformat()
                event["duration_ms"] = duration_ms
                self._emit_live_event(
                    session,
                    {
                        "type": "trace.update",
                        "index": trace_id,
                        "event": dict(event),
                    },
                )
                return
        self._push_trace_event(
            session=session,
            event_type="tool",
            title="工具调用",
            content=clipped_output,
            collapsed=True,
            status=status,
        )

    def _normalize_chat_payload(
        self,
        job_id: str,
        user_query: str,
        session_id: str,
        current_page: str,
        messages: Optional[list[dict[str, str]]],
    ) -> tuple[_ChatSession, str, Agent, str, _ChatDeps]:
        self._cleanup_expired_sessions()
        safe_session_id = (session_id or "").strip() or secrets.token_hex(12)
        safe_current_page = _sanitize_current_page_path(current_page)
        session = self._create_or_get_session(job_id, safe_session_id, current_page=safe_current_page)

        safe_messages = list(messages or [])
        prompt = self._format_prompt(session, safe_messages, user_query=user_query)
        agent, model_name = self._build_agent(session)
        deps = _ChatDeps(service=self, session=session)
        return session, prompt, agent, model_name, deps

    def _build_tools(self) -> list[Tool]:
        """Build fresh tool instances for each chat agent instance."""
        return [
            Tool(
                function=_list_docs_tool,
                name="list_docs",
                description="List generated documentation files under docs directory.",
                takes_ctx=True,
            ),
            Tool(
                function=_read_doc_tool,
                name="read_doc",
                description=(
                    "Read one generated documentation file by relative path "
                    "(e.g., overview.md or modules/api.md)."
                ),
                takes_ctx=True,
            ),
            Tool(
                function=_write_doc_tool,
                name="write_doc",
                description=(
                    "Write markdown file under docs directory by relative path only. "
                    "Supports mode=overwrite|append, docs only."
                ),
                takes_ctx=True,
            ),
            Tool(
                function=_list_code_tool,
                name="list_code_files",
                description="List code files inside the read-only repository snapshot.",
                takes_ctx=True,
            ),
            Tool(
                function=_read_code_tool,
                name="read_code",
                description="Read code file content by relative path and line range.",
                takes_ctx=True,
            ),
            Tool(
                function=_grep_code_tool,
                name="grep_code",
                description="Regex search across repository files with line numbers.",
                takes_ctx=True,
            ),
            Tool(
                function=_run_bash_tool,
                name="bash",
                description=(
                    "Execute linux shell command in chat workspace. "
                    "Read-only for code repository; avoid destructive operations."
                ),
                takes_ctx=True,
            ),
        ]

    def _make_models(self) -> tuple[Any, str]:
        names = [name.strip() for name in WebAppConfig.AGENT_MODEL_NAMES if name and name.strip()]
        if not names:
            names = ["kimi-k2.5"]

        models = [
            OpenAIModel(
                model_name=name,
                provider=self._provider,
                settings=OpenAIModelSettings(
                    temperature=0.1,
                    max_tokens=4096,
                ),
            )
            for name in names
        ]
        primary_name = names[0]
        if len(models) == 1:
            return models[0], primary_name
        return FallbackModel(*models), primary_name

    def _load_metadata_commit(self, docs_dir: Path) -> str:
        metadata_file = docs_dir / "metadata.json"
        if not metadata_file.exists():
            return ""
        try:
            metadata = file_manager.load_json(metadata_file)
        except Exception:
            return ""
        generation = metadata.get("generation_info") if isinstance(metadata, dict) else None
        commit_id = generation.get("commit_id") if isinstance(generation, dict) else None
        return str(commit_id or "").strip()

    def _normalize_subproject_path(self, raw_path: str) -> str:
        normalized = (raw_path or "").strip().replace("\\", "/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized.strip("/")
        if normalized in {"", "."}:
            return ""
        return normalized

    def _resolve_code_scope_dir(self, repo_root: Optional[Path], subproject_path: str) -> Optional[Path]:
        if not repo_root or not repo_root.exists():
            return repo_root
        normalized = self._normalize_subproject_path(subproject_path)
        if not normalized:
            return repo_root.resolve()

        try:
            target = (repo_root / normalized).resolve()
            if not target.is_relative_to(repo_root.resolve()):
                logger.warning("Subproject path escapes repo root: %s", normalized)
                return repo_root.resolve()
            if not target.exists() or not target.is_dir():
                logger.warning("Subproject path does not exist in cloned repo: %s", normalized)
                return repo_root.resolve()
            return target
        except Exception:
            logger.warning("Failed resolving subproject path, fallback to repo root: %s", normalized)
            return repo_root.resolve()

    def _resolve_job_context(self, job_id: str) -> tuple[str, Path, str, str]:
        job = self.background_worker.get_job_status(job_id)
        if job and job.docs_path and Path(job.docs_path).exists():
            docs_dir = Path(job.docs_path).resolve()
            commit_id = (job.commit_id or "").strip() or self._load_metadata_commit(docs_dir)
            subproject_path = ""
            if job.options and getattr(job.options, "subproject_path", None):
                subproject_path = self._normalize_subproject_path(job.options.subproject_path)
            return job.repo_url, docs_dir, commit_id, subproject_path

        for entry in self.cache_manager.cache_index.values():
            if entry.job_id != job_id:
                continue
            if not entry.docs_path:
                continue
            docs_dir = Path(entry.docs_path)
            if not docs_dir.exists():
                continue
            commit_id = self._load_metadata_commit(docs_dir.resolve())
            # Cache entry currently does not persist subproject_path.
            return entry.repo_url, docs_dir.resolve(), commit_id, ""

        raise FileNotFoundError(f"Unable to resolve job context for: {job_id}")

    def _create_temp_user(self, session_id: str) -> str:
        if os.geteuid() != 0:
            return ""

        user_suffix = hashlib.sha1(session_id.encode("utf-8")).hexdigest()[:10]
        username = f"cwchat_{user_suffix}"

        exists = subprocess.run(
            ["id", "-u", username],
            capture_output=True,
            text=True,
            check=False,
        )
        if exists.returncode == 0:
            return username

        create = subprocess.run(
            ["useradd", "-M", "-s", "/bin/sh", username],
            capture_output=True,
            text=True,
            check=False,
        )
        if create.returncode == 0:
            return username
        return ""

    def _clone_repo_readonly(self, clone_url: str, commit_id: str, target_dir: Path) -> Optional[Path]:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)

        success = GitHubRepoProcessor.clone_repository(clone_url, str(target_dir), commit_id or None)
        if not success:
            return None

        for root, dirs, files in os.walk(target_dir):
            for dname in dirs:
                path = Path(root) / dname
                try:
                    mode = os.stat(path).st_mode
                    os.chmod(path, mode & ~0o222)
                except Exception:
                    pass
            for fname in files:
                path = Path(root) / fname
                try:
                    mode = os.stat(path).st_mode
                    os.chmod(path, mode & ~0o222)
                except Exception:
                    pass

        return target_dir.resolve()

    def _create_or_get_session(
        self,
        job_id: str,
        session_id: str,
        current_page: str,
    ) -> _ChatSession:
        with self._lock:
            existing = self._sessions.get(session_id)
            if existing and existing.job_id == job_id:
                existing.updated_at = datetime.now()
                if current_page:
                    existing.current_page = current_page
                return existing

        repo_url, docs_dir, commit_id, subproject_path = self._resolve_job_context(job_id)
        created_at = datetime.now()
        sandbox_root = (Path(WebAppConfig.TEMP_DIR) / "chat_sessions" / session_id).resolve()
        workspace_dir = sandbox_root / "workspace"
        repo_root_dir = sandbox_root / "repo"

        if sandbox_root.exists():
            shutil.rmtree(sandbox_root, ignore_errors=True)
        workspace_dir.mkdir(parents=True, exist_ok=True)

        read_only_repo_root = self._clone_repo_readonly(repo_url, commit_id, repo_root_dir)
        code_scope_dir = self._resolve_code_scope_dir(read_only_repo_root, subproject_path)
        temp_user = self._create_temp_user(session_id)
        if temp_user and os.geteuid() == 0:
            subprocess.run(
                ["chown", "-R", f"{temp_user}:{temp_user}", str(workspace_dir)],
                capture_output=True,
                text=True,
                check=False,
            )

        _, model_name = self._make_models()

        session = _ChatSession(
            session_id=session_id,
            job_id=job_id,
            repo_url=repo_url,
            docs_dir=docs_dir,
            current_page=current_page or "overview.md",
            created_at=created_at,
            updated_at=created_at,
            sandbox_root=sandbox_root,
            workspace_dir=workspace_dir,
            repo_root_dir=read_only_repo_root,
            repo_dir=code_scope_dir,
            subproject_path=subproject_path,
            temp_user=temp_user,
            model_name=model_name,
        )
        logger.info(
            "CodeWikiAgent session initialized: job_id=%s session_id=%s docs_dir=%s repo_dir=%s subproject_path=%s",
            job_id,
            session_id,
            session.docs_dir.as_posix(),
            session.repo_dir.as_posix() if session.repo_dir else "(unavailable)",
            session.subproject_path or "(repo-root)",
        )

        with self._lock:
            self._sessions[session_id] = session
        return session

    def _cleanup_expired_sessions(self):
        ttl = timedelta(minutes=WebAppConfig.CHAT_SESSION_TTL_MINUTES)
        now = datetime.now()
        stale_ids: list[str] = []
        with self._lock:
            for session_id, session in self._sessions.items():
                if now - session.updated_at > ttl:
                    stale_ids.append(session_id)
            for session_id in stale_ids:
                session = self._sessions.pop(session_id, None)
                if not session:
                    continue
                shutil.rmtree(session.sandbox_root, ignore_errors=True)

    def run_shell_command(self, session: _ChatSession, command: str, timeout_seconds: int = 20) -> str:
        timeout = max(1, min(WebAppConfig.CHAT_SHELL_TIMEOUT_SECONDS, int(timeout_seconds)))
        cmd_text = (command or "").strip()
        if not cmd_text:
            return "Empty command."

        blocked_reason = self._check_command_policy(session, cmd_text)
        if blocked_reason:
            return f"Command blocked by policy: {blocked_reason}"

        base_command = ["sh", "-lc", cmd_text]
        if session.temp_user:
            if shutil.which("runuser"):
                base_command = ["runuser", "-u", session.temp_user, "--", "sh", "-lc", cmd_text]
            elif shutil.which("su"):
                base_command = ["su", "-s", "/bin/sh", "-c", cmd_text, session.temp_user]

        env = os.environ.copy()
        env["CODEWIKI_DOCS_DIR"] = session.docs_dir.as_posix()
        env["CODEWIKI_REPO_DIR"] = session.repo_dir.as_posix() if session.repo_dir else ""
        env["CODEWIKI_READONLY_REPO"] = "1"

        try:
            completed = subprocess.run(
                base_command,
                cwd=str(session.workspace_dir),
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout}s."
        except Exception as exc:
            return f"Command failed: {exc}"

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        parts = [f"$ {cmd_text}", f"exit_code={completed.returncode}"]
        if stdout:
            parts.append(stdout)
        if stderr:
            parts.append(f"[stderr]\n{stderr}")
        return _clip_text("\n".join(parts), WebAppConfig.CHAT_MAX_TOOL_OUTPUT_CHARS)

    def _check_command_policy(self, session: _ChatSession, cmd_text: str) -> str:
        """Best-effort guardrail: deny write/destructive commands and off-scope paths."""
        lowered = cmd_text.lower()
        blocked_markers = [
            " rm ",
            " mv ",
            " cp ",
            " chmod ",
            " chown ",
            " sed -i",
            " git commit",
            " git push",
            " git reset",
            " git checkout",
            " tee ",
            ">>",
            ">",
            "touch ",
            "truncate ",
            "dd if=",
        ]
        wrapped = f" {lowered} "
        for marker in blocked_markers:
            if marker in wrapped:
                return f"contains forbidden operation: {marker.strip()}"

        if any(token in lowered for token in ["shutdown", "reboot", "init 0", "halt"]):
            return "contains unsafe system operation"

        allowed_prefixes = [session.workspace_dir.resolve().as_posix(), session.docs_dir.resolve().as_posix()]
        if session.repo_dir:
            allowed_prefixes.append(session.repo_dir.resolve().as_posix())

        try:
            tokens = shlex.split(cmd_text, posix=True)
        except Exception:
            tokens = []
        abs_path_re = re.compile(r"^/[^;&|]+")
        for token in tokens:
            if not token.startswith("/"):
                continue
            match = abs_path_re.match(token)
            if not match:
                continue
            path_token = match.group(0)
            if not any(path_token.startswith(prefix) for prefix in allowed_prefixes):
                return f"path outside allowed directories: {path_token}"

        return ""

    def _build_agent(self, session: _ChatSession) -> tuple[Agent, str]:
        model_chain, primary_name = self._make_models()
        docs_dir = session.docs_dir.as_posix()
        repo_dir = session.repo_dir.as_posix() if session.repo_dir else "(unavailable)"
        repo_root = session.repo_root_dir.as_posix() if session.repo_root_dir else "(unavailable)"
        subproject = session.subproject_path or "(仓库根目录)"
        workspace_dir = session.workspace_dir.as_posix()
        system_prompt = (
            "你是 CodeWikiAgent（CodeDocAgent 运行时），非常熟悉目标代码库与其生成文档。\n"
            "回答规则：\n"
            "1) 默认使用中文回答（除非用户明确要求其他语言）。\n"
            "2) 先基于证据回答，不确定时必须先用工具检索文档与代码。\n"
            "3) 引用结论时给出具体相对路径与关键片段。\n\n"
            "访问边界（严格）:\n"
            f"- 仅可访问文档目录: {docs_dir}\n"
            f"- 代码仓库根目录(仅参考): {repo_root}\n"
            f"- 本文档对应代码目录(可访问范围): {repo_dir}\n"
            f"- 该代码目录在仓库中的子目录路径: {subproject}\n"
            f"- 命令工作目录: {workspace_dir}\n"
            "- 允许修改文档目录中的 Markdown 文件（.md/.markdown），优先使用 write_doc 工具。\n"
            "- 严禁修改代码目录、仓库历史、系统权限与非文档目录文件。\n"
            "- 若用户要求修改代码，请明确拒绝并说明仅允许更新文档目录。"
        )
        return (
            Agent(
                model_chain,
                name="CodeWikiAgent",
                deps_type=_ChatDeps,
                tools=self._build_tools(),
                system_prompt=system_prompt,
            ),
            primary_name,
        )

    def _flatten_exception_messages(self, exc: BaseException, depth: int = 0) -> list[str]:
        """Extract concise messages from nested ExceptionGroup / chained errors."""
        if depth > 4:
            return []

        messages: list[str] = []
        text = str(exc).strip()
        if text:
            messages.append(text)

        # Python 3.11+ ExceptionGroup
        sub_errors = getattr(exc, "exceptions", None)
        if isinstance(sub_errors, tuple):
            for sub in sub_errors:
                messages.extend(self._flatten_exception_messages(sub, depth + 1))

        cause = getattr(exc, "__cause__", None)
        if cause is not None:
            messages.extend(self._flatten_exception_messages(cause, depth + 1))

        context = getattr(exc, "__context__", None)
        if context is not None and context is not cause:
            messages.extend(self._flatten_exception_messages(context, depth + 1))

        dedup: list[str] = []
        seen = set()
        for item in messages:
            if not item or item in seen:
                continue
            seen.add(item)
            dedup.append(item)
        return dedup

    def _build_model_diagnostics(
        self,
        exc: Exception,
        primary_model: str,
        session: Optional[_ChatSession] = None,
    ) -> str:
        """Build user-visible diagnostics for model/auth/base_url failures."""
        model_list = [name.strip() for name in WebAppConfig.AGENT_MODEL_NAMES if name and name.strip()]
        if not model_list:
            model_list = [primary_model]
        base_url = (WebAppConfig.AGENT_MODEL_BASE_URL or "").strip()
        api_key_exists = bool((WebAppConfig.AGENT_MODEL_API_KEY or "").strip())
        raw_msgs = self._flatten_exception_messages(exc)
        hints = []
        for msg in raw_msgs:
            lowered = msg.lower()
            if any(k in lowered for k in ["401", "unauthorized", "invalid api key", "authentication"]):
                hints.append("可能是 AGENT_MODEL_API_KEY 不正确或无权限。")
            if any(k in lowered for k in ["404", "not found", "model", "unsupported"]):
                hints.append("可能是 AGENT_MODEL_NAMES 中模型名与网关不匹配。")
            if any(k in lowered for k in ["connection", "timeout", "dns", "refused", "ssl", "certificate"]):
                hints.append("可能是 AGENT_MODEL_BASE_URL 不可达或证书配置异常。")
            if "file name too long" in lowered:
                hints.append("工具参数可能把整段文档内容当成文件路径，请改传相对路径（如 overview.md）。")

        unique_hints: list[str] = []
        for hint in hints:
            if hint not in unique_hints:
                unique_hints.append(hint)

        details = raw_msgs[:4] if raw_msgs else [str(exc)]
        lines = [
            "CodeWikiAgent 模型调用失败。",
            f"- base_url: {base_url or '(empty)'}",
            f"- api_key_provided: {'yes' if api_key_exists else 'no'}",
            f"- models: {', '.join(model_list)}",
        ]
        if session:
            lines.extend(
                [
                    f"- docs_dir: {session.docs_dir.as_posix()}",
                    (
                        "- repo_dir: "
                        + (session.repo_dir.as_posix() if session.repo_dir else "(unavailable)")
                    ),
                ]
            )
        lines.append("- errors:")
        for item in details:
            lines.append(f"  - {item}")
        if unique_hints:
            lines.append("- hints:")
            for hint in unique_hints[:3]:
                lines.append(f"  - {hint}")
        return "\n".join(lines)

    def _format_prompt(
        self,
        session: _ChatSession,
        messages: list[dict[str, str]],
        user_query: str,
    ) -> str:
        history_tail = messages[-10:]
        history_lines: list[str] = []
        for item in history_tail:
            role = (item.get("role") or "user").strip().lower()
            content = (item.get("content") or "").strip()
            if not content:
                continue
            history_lines.append(f"{role.upper()}:\n{content}")

        context_lines = [
            f"job_id={session.job_id}",
            f"current_page={session.current_page}",
            f"docs_dir={session.docs_dir.as_posix()}",
            f"repo_root_dir={session.repo_root_dir.as_posix() if session.repo_root_dir else '(unavailable)'}",
            f"repo_dir={session.repo_dir.as_posix() if session.repo_dir else '(unavailable)'}",
            f"subproject_path={session.subproject_path or '(repo-root)'}",
            f"workspace_dir={session.workspace_dir.as_posix()}",
        ]
        return (
            "Context:\n"
            + "\n".join(context_lines)
            + "\n\nConversation so far:\n"
            + ("\n\n".join(history_lines) if history_lines else "(empty)")
            + "\n\nUser question:\n"
            + user_query
        )

    async def chat(
        self,
        job_id: str,
        user_query: str,
        session_id: str = "",
        current_page: str = "overview.md",
        messages: Optional[list[dict[str, str]]] = None,
    ) -> dict[str, Any]:
        session, prompt, agent, model_name, deps = self._normalize_chat_payload(
            job_id=job_id,
            user_query=user_query,
            session_id=session_id,
            current_page=current_page,
            messages=messages,
        )
        if session.is_running:
            raise RuntimeError("当前会话仍在处理中，请等待完成后再发送新问题。")
        session.trace_events = []
        session.is_running = True
        session.updated_at = datetime.now()
        session.run_started_at = session.updated_at.isoformat()
        session.run_finished_at = ""
        self._append_history_message(session, "user", user_query)

        self._push_trace_event(
            session=session,
            event_type="thinking",
            title="思考",
            content=f"正在分析问题，并规划检索路径（当前页面: {session.current_page}）。",
            collapsed=True,
            status="done",
        )
        self._push_trace_event(
            session=session,
            event_type="skill",
            title="已启用技能",
            content=(
                "list_docs / read_doc / write_doc / list_code_files / read_code / grep_code / bash\n"
                f"文档目录(可写 .md): {session.docs_dir.as_posix()}\n"
                f"代码作用域: {session.repo_dir.as_posix() if session.repo_dir else '(unavailable)'}"
            ),
            collapsed=True,
            status="ready",
        )

        try:
            result = await agent.run(prompt, deps=deps)
        except Exception as exc:
            diagnostics = self._build_model_diagnostics(exc, model_name, session=session)
            self._push_trace_event(
                session=session,
                event_type="content",
                title="执行失败",
                content=diagnostics,
                collapsed=False,
                status="error",
            )
            trace_events = [dict(item) for item in session.trace_events]
            self._append_history_message(session, "assistant", diagnostics, events=trace_events)
            session.updated_at = datetime.now()
            session.is_running = False
            session.run_finished_at = session.updated_at.isoformat()
            logger.exception("CodeWikiAgent run failed. %s", diagnostics)
            raise RuntimeError(diagnostics) from exc
        output = str(result.output).strip()
        if not output:
            output = "No answer generated."
        self._push_trace_event(
            session=session,
            event_type="content",
            title="回答",
            content=output,
            collapsed=False,
            status="ok",
        )

        now = datetime.now()
        session.updated_at = now
        session.model_name = model_name
        session.is_running = False
        session.run_finished_at = now.isoformat()
        trace_events = [dict(item) for item in session.trace_events]
        self._append_history_message(session, "assistant", output, events=trace_events)

        return {
            "protocol": "a2ui-0.1",
            "session_id": session.session_id,
            "agent": "CodeWikiAgent",
            "model": model_name,
            "output": output,
            "messages": [{"role": "assistant", "content": output, "events": trace_events}],
            "events": trace_events,
            "timestamp": now.isoformat(),
        }

    async def chat_stream(
        self,
        job_id: str,
        user_query: str,
        session_id: str = "",
        current_page: str = "overview.md",
        messages: Optional[list[dict[str, str]]] = None,
    ) -> AsyncIterator[dict[str, Any]]:
        session, prompt, agent, model_name, deps = self._normalize_chat_payload(
            job_id=job_id,
            user_query=user_query,
            session_id=session_id,
            current_page=current_page,
            messages=messages,
        )
        if session.is_running:
            raise RuntimeError("当前会话仍在处理中，请等待完成后再发送新问题。")
        session.trace_events = []
        session.is_running = True
        session.updated_at = datetime.now()
        session.run_started_at = session.updated_at.isoformat()
        session.run_finished_at = ""
        self._append_history_message(session, "user", user_query)

        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        done = asyncio.Event()

        def emit(payload: dict[str, Any]) -> None:
            queue.put_nowait(payload)

        session.event_emitter = emit

        async def _runner() -> None:
            try:
                self._push_trace_event(
                    session=session,
                    event_type="thinking",
                    title="思考",
                    content=f"正在分析问题，并规划检索路径（当前页面: {session.current_page}）。",
                    collapsed=True,
                    status="done",
                )
                self._push_trace_event(
                    session=session,
                    event_type="skill",
                    title="已启用技能",
                    content=(
                        "list_docs / read_doc / write_doc / list_code_files / read_code / grep_code / bash\n"
                        f"文档目录(可写 .md): {session.docs_dir.as_posix()}\n"
                        f"代码作用域: {session.repo_dir.as_posix() if session.repo_dir else '(unavailable)'}"
                    ),
                    collapsed=True,
                    status="ready",
                )
                result = await agent.run(prompt, deps=deps)
                output = str(result.output).strip()
                if not output:
                    output = "No answer generated."
                self._push_trace_event(
                    session=session,
                    event_type="content",
                    title="回答",
                    content=output,
                    collapsed=False,
                    status="ok",
                )
                now = datetime.now()
                session.updated_at = now
                session.model_name = model_name
                session.is_running = False
                session.run_finished_at = now.isoformat()
                trace_events = [dict(item) for item in session.trace_events]
                self._append_history_message(session, "assistant", output, events=trace_events)
                emit(
                    {
                        "type": "result",
                        "data": {
                            "protocol": "a2ui-0.1",
                            "session_id": session.session_id,
                            "agent": "CodeWikiAgent",
                            "model": model_name,
                            "output": output,
                            "messages": [{"role": "assistant", "content": output, "events": trace_events}],
                            "events": trace_events,
                            "timestamp": now.isoformat(),
                        },
                    }
                )
            except Exception as exc:
                diagnostics = self._build_model_diagnostics(exc, model_name, session=session)
                self._push_trace_event(
                    session=session,
                    event_type="content",
                    title="执行失败",
                    content=diagnostics,
                    collapsed=False,
                    status="error",
                )
                trace_events = [dict(item) for item in session.trace_events]
                self._append_history_message(session, "assistant", diagnostics, events=trace_events)
                session.updated_at = datetime.now()
                session.is_running = False
                session.run_finished_at = session.updated_at.isoformat()
                logger.exception("CodeWikiAgent stream run failed. %s", diagnostics)
                emit({"type": "error", "message": diagnostics})
            finally:
                session.event_emitter = None
                done.set()

        runner_task = asyncio.create_task(_runner())
        emit(
            {
                "type": "session",
                "session_id": session.session_id,
                "agent": "CodeWikiAgent",
                "model": model_name,
                "timestamp": datetime.now().isoformat(),
            }
        )

        try:
            while True:
                if done.is_set() and queue.empty():
                    break
                try:
                    item = await asyncio.wait_for(queue.get(), timeout=0.6)
                    yield item
                except asyncio.TimeoutError:
                    yield {"type": "heartbeat", "timestamp": datetime.now().isoformat()}
        finally:
            # Keep background run alive even if client disconnects.
            # This allows the browser to reconnect and fetch completed session output.
            if done.is_set() and not runner_task.done():
                try:
                    await runner_task
                except asyncio.CancelledError:
                    pass

    def get_session_state(self, job_id: str, session_id: str) -> dict[str, Any]:
        """Fetch server-side session snapshot for browser resume/recovery."""
        self._cleanup_expired_sessions()
        safe_session_id = (session_id or "").strip()
        if not safe_session_id:
            raise FileNotFoundError("session_id is required")

        with self._lock:
            session = self._sessions.get(safe_session_id)
            if not session or session.job_id != job_id:
                raise FileNotFoundError(f"Chat session not found: {safe_session_id}")
            history = [dict(item) for item in session.history[-80:]]
            events = [dict(item) for item in session.trace_events]
            snapshot = {
                "protocol": "a2ui-0.1",
                "session_id": session.session_id,
                "job_id": session.job_id,
                "agent": "CodeWikiAgent",
                "model": session.model_name,
                "status": "running" if session.is_running else "idle",
                "run_started_at": session.run_started_at,
                "run_finished_at": session.run_finished_at,
                "updated_at": session.updated_at.isoformat(),
                "current_page": session.current_page,
                "messages": history,
                "events": events,
            }
        return snapshot
