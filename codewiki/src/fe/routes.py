#!/usr/bin/env python3
"""
FastAPI route handlers for the CodeWiki web application.
"""

from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import asdict
import json
import re
import threading
import secrets
from urllib.parse import urlencode

from traceback import format_exc

from fastapi import Form, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse

from .models import JobStatus, JobStatusResponse, GenerationOptions, DocChatRequest
from .github_processor import GitHubRepoProcessor
from .background_worker import BackgroundWorker
from .cache_manager import CacheManager
from .templates import ADMIN_TEMPLATE, WEB_INTERFACE_TEMPLATE
from .template_utils import render_template
from .config import WebAppConfig
from .chat_agent import CodeWikiChatService
from codewiki.src.utils import file_manager
from codewiki.src.be.doc_type_profiles import (
    list_doc_type_profiles,
    upsert_doc_type_profile,
    delete_doc_type_profile,
    normalize_doc_type_name,
)


class WebRoutes:
    """Handles all web routes for the application."""
    VERSION_PATTERN = re.compile(r"^\d{6}-\d{6}$")
    
    def __init__(self, background_worker: BackgroundWorker, cache_manager: CacheManager):
        self.background_worker = background_worker
        self.cache_manager = cache_manager
        self.chat_service = None
        self._engagement_lock = threading.RLock()
        self._engagement_file = Path(WebAppConfig.CACHE_DIR) / "docs_engagement.json"

    def _get_chat_service(self) -> CodeWikiChatService:
        """Lazily create chat service only when chat is actually used."""
        if self.chat_service is None:
            self.chat_service = CodeWikiChatService(
                background_worker=self.background_worker,
                cache_manager=self.cache_manager,
            )
        return self.chat_service
    
    async def index_get(self, request: Request) -> HTMLResponse:
        """Main page with form for submitting Git repositories."""
        recent_jobs = self._collect_completed_docs()
        home_cards, home_leaderboard, home_stats = self._build_home_cards(recent_jobs)
        
        context = {
            "message": None,
            "message_type": None,
            "repo_url": "",
            "commit_id": "",
            "recent_jobs": recent_jobs,
            "home_cards": home_cards,
            "home_leaderboard": home_leaderboard,
            "home_stats": home_stats,
        }
        
        return HTMLResponse(content=render_template(WEB_INTERFACE_TEMPLATE, context))
    
    async def index_post(
        self,
        request: Request,
        repo_url: str = Form(...),
        commit_id: str = Form(""),
    ) -> HTMLResponse:
        """Handle repository submission."""
        # Clean up old jobs before processing
        self.cleanup_old_jobs()
        
        message = None
        message_type = None
        
        repo_url = repo_url.strip()
        commit_id = commit_id.strip() if commit_id else ""
        
        if not repo_url:
            message = "Please enter a Git repository URL"
            message_type = "error"
        elif not GitHubRepoProcessor.is_valid_github_url(repo_url):
            message = "Please enter a valid Git repository URL (GitHub, GitLab, or any Git repository)"
            message_type = "error"
        else:
            # Normalize the repo URL for comparison
            normalized_repo_url = self._normalize_github_url(repo_url)
            
            # Get repo info for job ID generation
            repo_info = GitHubRepoProcessor.get_repo_info(normalized_repo_url)
            job_id = self._repo_full_name_to_job_id(repo_info['full_name'])
            title = GitHubRepoProcessor.generate_title(normalized_repo_url)
            
            # Check if already in queue, processing, or recently failed
            existing_job = self.background_worker.get_job_status(job_id)
            recent_cutoff = datetime.now() - timedelta(minutes=WebAppConfig.RETRY_COOLDOWN_MINUTES)
            
            if existing_job:
                if existing_job.status in ['queued', 'processing']:
                    pass  # Will handle below
                elif existing_job.status == 'failed' and existing_job.created_at > recent_cutoff:
                    pass  # Will handle below
                else:
                    existing_job = None  # Job is old or completed, can reuse
            
            if existing_job:
                if existing_job.status in ['queued', 'processing']:
                    message = f"Repository is already being processed (Job ID: {existing_job.job_id})"
                else:
                    message = f"Repository recently failed processing. Please wait a few minutes before retrying (Job ID: {existing_job.job_id})"
                message_type = "error"
            else:
                # Check cache
                cached_docs = self.cache_manager.get_cached_docs(
                    normalized_repo_url,
                    cache_scope=self._job_cache_scope(job_id),
                )
                if cached_docs and Path(cached_docs).exists():
                    message = "Documentation found in cache! Redirecting to view..."
                    message_type = "success"
                    # Create a dummy completed job for display
                    job = JobStatus(
                        job_id=job_id,
                        repo_url=normalized_repo_url,  # Use normalized URL
                        title=title,
                        status='completed',
                        created_at=datetime.now(),
                        completed_at=datetime.now(),
                        docs_path=cached_docs,
                        progress="Retrieved from cache",
                        commit_id=commit_id if commit_id else None
                    )
                    self.background_worker.set_job_status(job_id, job)
                else:
                    # Add to queue
                    try:
                        job = JobStatus(
                            job_id=job_id,
                            repo_url=normalized_repo_url,  # Use normalized URL
                            title=title,
                            status='queued',
                            created_at=datetime.now(),
                            progress="Waiting in queue...",
                            commit_id=commit_id if commit_id else None
                        )
                        
                        self.background_worker.add_job(job_id, job)
                        message = f"Repository added to processing queue! Job ID: {job_id}"
                        message_type = "success"
                        repo_url = ""  # Clear form
                        
                    except Exception as e:
                        message = f"Failed to add repository to queue: {str(e)}\n{format_exc()}"
                        message_type = "error"
        
        recent_jobs = self._collect_completed_docs()
        home_cards, home_leaderboard, home_stats = self._build_home_cards(recent_jobs)
        
        context = {
            "message": message,
            "message_type": message_type,
            "repo_url": repo_url or "",
            "commit_id": commit_id or "",
            "recent_jobs": recent_jobs,
            "home_cards": home_cards,
            "home_leaderboard": home_leaderboard,
            "home_stats": home_stats,
        }
        
        return HTMLResponse(content=render_template(WEB_INTERFACE_TEMPLATE, context))
    
    async def get_job_status(self, job_id: str) -> JobStatusResponse:
        """API endpoint to get job status."""
        job = self.background_worker.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobStatusResponse(**asdict(job))
    
    async def view_docs(self, job_id: str, version: str = "", lang: str = "") -> RedirectResponse:
        """View generated documentation."""
        job = self.background_worker.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status != 'completed' or not job.docs_path:
            raise HTTPException(status_code=404, detail="Documentation not available")
        
        docs_path = Path(job.docs_path)
        if not docs_path.exists():
            raise HTTPException(status_code=404, detail="Documentation files not found")
        self._record_doc_view(job_id)
        
        # Redirect to the documentation viewer
        redirect_url = f"/static-docs/{job_id}/"
        query_params = {}
        if version:
            query_params["version"] = version
        if lang:
            query_params["lang"] = lang
        if query_params:
            redirect_url = f"{redirect_url}?{urlencode(query_params)}"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    
    async def serve_generated_docs(
        self,
        job_id: str,
        filename: str = "overview.md",
        version: str = "",
        lang: str = "",
        content_only: bool = False,
    ) -> HTMLResponse:
        """Serve generated documentation files."""
        job = self.background_worker.get_job_status(job_id)
        docs_path = None
        repo_url = None
        
        if job:
            # Job status exists - use it
            if job.status != 'completed' or not job.docs_path:
                raise HTTPException(status_code=404, detail="Documentation not available")
            docs_path = Path(job.docs_path)
            repo_url = job.repo_url
        else:
            # No job status - try to find documentation in cache by job_id
            potential_repo_url = None
            cached_docs = None
            matched_cache_entry = None

            # 1) Exact cache entry by job_id (supports subprojects/variants)
            for _, entry in self.cache_manager.cache_index.items():
                if entry.job_id == job_id and entry.docs_path and Path(entry.docs_path).exists():
                    cached_docs = entry.docs_path
                    potential_repo_url = entry.repo_url
                    matched_cache_entry = entry
                    break

            # 2) Backward-compatible lookup by repo full name
            if not cached_docs:
                repo_full_name = self._job_id_to_repo_full_name(job_id)

                potential_repo_url = f"https://github.com/{repo_full_name}"
                cached_docs = self.cache_manager.get_cached_docs(
                    potential_repo_url, cache_scope=self._job_cache_scope(job_id)
                )

                if not cached_docs:
                    potential_repo_url = f"https://gitlab.com/{repo_full_name}"
                    cached_docs = self.cache_manager.get_cached_docs(
                        potential_repo_url, cache_scope=self._job_cache_scope(job_id)
                    )

                if not cached_docs:
                    for _, entry in self.cache_manager.cache_index.items():
                        try:
                            entry_repo_info = GitHubRepoProcessor.get_repo_info(entry.repo_url)
                            if entry_repo_info['full_name'] == repo_full_name:
                                cached_docs = entry.docs_path
                                potential_repo_url = entry.repo_url
                                matched_cache_entry = entry
                                break
                        except Exception:
                            continue
            
            if cached_docs and Path(cached_docs).exists():
                docs_path = Path(cached_docs)
                repo_url = potential_repo_url
                
                # Recreate job status for consistency
                job = JobStatus(
                    job_id=job_id,
                    repo_url=potential_repo_url,
                    title=matched_cache_entry.title if matched_cache_entry and matched_cache_entry.title else "",
                    status='completed',
                    created_at=datetime.now(),
                    completed_at=datetime.now(),
                    docs_path=cached_docs,
                    progress="Loaded from cache",
                    commit_id=None  # No commit info available from cache
                )
                self.background_worker.set_job_status(job_id, job)
                self.background_worker.save_job_statuses()
            else:
                raise HTTPException(status_code=404, detail="Documentation not found")
        
        if not docs_path or not docs_path.exists():
            raise HTTPException(status_code=404, detail="Documentation files not found")

        docs_path, available_versions, selected_version = self._resolve_docs_version(
            job_id=job_id,
            fallback_docs_path=docs_path,
            requested_version=version
        )
        
        # Resolve language-specific docs directory
        docs_path, available_languages, selected_lang = self._resolve_docs_language(
            docs_root=docs_path,
            requested_lang=lang
        )

        # Load module tree
        module_tree = None
        module_tree_file = docs_path / "module_tree.json"
        if module_tree_file.exists():
            try:
                module_tree = file_manager.load_json(module_tree_file)
                if not isinstance(module_tree, dict):
                    module_tree = None
            except Exception:
                pass
        
        # Load metadata
        metadata = None
        metadata_file = docs_path / "metadata.json"
        if metadata_file.exists():
            try:
                metadata = file_manager.load_json(metadata_file)
            except Exception:
                pass
        
        # Serve the requested file (with traversal protection)
        resolved_docs_path = docs_path.resolve()
        file_path = (docs_path / filename).resolve()
        if not file_path.is_relative_to(resolved_docs_path):
            raise HTTPException(status_code=403, detail="Access denied")
        if not file_path.exists():
            fallback_file = self._resolve_existing_doc_file(docs_path, filename)
            if fallback_file is None:
                raise HTTPException(status_code=404, detail=f"File {filename} not found")
            file_path = fallback_file.resolve()
            if not file_path.is_relative_to(resolved_docs_path):
                raise HTTPException(status_code=403, detail="Access denied")
            filename = fallback_file.relative_to(docs_path).as_posix()
        
        try:
            content = file_manager.load_text(file_path)
            
            # Convert markdown to HTML (reuse from visualise_docs.py)
            from .visualise_docs import markdown_to_html, get_file_title
            from .templates import DOCS_VIEW_TEMPLATE, DOCS_CONTENT_TEMPLATE
            
            html_content = markdown_to_html(content)
            title = get_file_title(file_path)

            if content_only:
                content_context = {
                    "title": title,
                    "content": html_content,
                }
                return HTMLResponse(content=render_template(DOCS_CONTENT_TEMPLATE, content_context))
            
            navigation_fallback = self._build_fallback_navigation(docs_path)
            query_params = {}
            if selected_version:
                query_params["version"] = selected_version
            if selected_lang:
                query_params["lang"] = selected_lang
            query_suffix = f"?{urlencode(query_params)}" if query_params else ""
            variant_options = self._collect_repo_variant_options(job, job_id)
            view_options = variant_options.get("view_options", [])
            current_doc_type = variant_options.get("current_doc_type", "")
            content_frame_url = f"/static-docs-content/{job_id}/{filename}{query_suffix}"
            docs_display_title = ""
            try:
                repo_info = GitHubRepoProcessor.get_repo_info(repo_url or "")
                docs_display_title = repo_info.get("full_name", "") or ""
            except Exception:
                docs_display_title = (repo_url or "").strip()

            context = {
                "repo_name": repo_url.split("/")[-1],
                "docs_display_title": docs_display_title or (repo_url.split("/")[-1] if repo_url else job_id),
                "title": title,
                "content": html_content,
                "navigation": module_tree,
                "fallback_navigation": navigation_fallback,
                "current_page": filename,
                "job_id": job_id,
                "metadata": metadata,
                "versions": available_versions,
                "current_version": selected_version,
                "languages": available_languages,
                "current_lang": selected_lang,
                "query_suffix": query_suffix,
                "docs_home_url": "/",
                "view_options": view_options,
                "view_matrix": variant_options.get("view_matrix", {}),
                "subproject_options": variant_options.get("subproject_options", []),
                "current_subproject_key": variant_options.get("current_subproject_key", ""),
                "current_subproject_label": variant_options.get("current_subproject_label", ""),
                "current_view_job_id": variant_options.get("current_view_job_id", job_id),
                "current_doc_type": current_doc_type,
                "chat_api_url": f"/api/docs/{job_id}/chat",
                "chat_stream_api_url": f"/api/docs/{job_id}/chat/stream",
                "chat_protocol": "a2ui-0.1",
                "content_frame_url": content_frame_url,
                "content_nav_base": f"/static-docs-content/{job_id}",
                "shell_nav_base": f"/static-docs/{job_id}",
            }
            
            return HTMLResponse(content=render_template(DOCS_VIEW_TEMPLATE, context))
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading {filename}: {e}\n{format_exc()}")

    def _extract_chat_message_payload(self, payload: DocChatRequest) -> tuple[str, list[dict[str, str]]]:
        """Normalize incoming chat payload for JSON/SSE endpoints."""
        message_text = (payload.message or "").strip()
        message_items: list[dict[str, str]] = []
        if payload.messages:
            for item in payload.messages:
                if hasattr(item, "model_dump"):
                    obj = item.model_dump()
                else:
                    obj = {"role": getattr(item, "role", ""), "content": getattr(item, "content", "")}
                role = str(obj.get("role", "")).strip().lower() or "user"
                content = str(obj.get("content", "")).strip()
                if not content:
                    continue
                message_items.append({"role": role, "content": content})

        if not message_text:
            for item in reversed(message_items):
                if item["role"] == "user":
                    message_text = item["content"]
                    break

        if not message_text:
            raise HTTPException(status_code=400, detail="message is required")
        return message_text, message_items

    async def docs_chat(self, job_id: str, payload: DocChatRequest) -> JSONResponse:
        """Doc page chat endpoint backed by CodeWikiAgent."""
        message_text, message_items = self._extract_chat_message_payload(payload)

        try:
            response = await self._get_chat_service().chat(
                job_id=job_id,
                user_query=message_text,
                session_id=(payload.session_id or "").strip(),
                current_page=(payload.current_page or "overview.md").strip(),
                messages=message_items,
            )
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Chat failed: {e}")
        return JSONResponse(content=response)

    async def docs_chat_stream(self, job_id: str, payload: DocChatRequest) -> StreamingResponse:
        """Doc page chat endpoint using SSE streaming events."""
        message_text, message_items = self._extract_chat_message_payload(payload)

        async def _sse_iter():
            try:
                async for event in self._get_chat_service().chat_stream(
                    job_id=job_id,
                    user_query=message_text,
                    session_id=(payload.session_id or "").strip(),
                    current_page=(payload.current_page or "overview.md").strip(),
                    messages=message_items,
                ):
                    yield f"event: message\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"
            except FileNotFoundError as e:
                err = {"type": "error", "message": str(e)}
                yield f"event: message\ndata: {json.dumps(err, ensure_ascii=False)}\n\n"
            except Exception as e:
                err = {"type": "error", "message": f"Chat stream failed: {e}"}
                yield f"event: message\ndata: {json.dumps(err, ensure_ascii=False)}\n\n"
            finally:
                yield "event: done\ndata: [DONE]\n\n"

        return StreamingResponse(
            _sse_iter(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    
    def _normalize_github_url(self, url: str) -> str:
        """Normalize Git repository URL for consistent comparison."""
        try:
            # Get repo info to standardize the URL format
            repo_info = GitHubRepoProcessor.get_repo_info(url)
            # For SSH URLs, use the original URL; for HTTP URLs, use the standard format
            if url.startswith('ssh://') or ('@' in url and ':' in url and not url.startswith('http')):
                return url
            else:
                return f"https://{repo_info['domain']}/{repo_info['full_name']}"
        except Exception:
            # Fallback to basic normalization
            return url.rstrip('/').lower()

    def _normalize_subproject_path(self, subproject_path: str) -> str:
        """Normalize subproject path for stable job/cache keys."""
        if not subproject_path:
            return ""
        normalized = subproject_path.strip().replace("\\", "/")
        while normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized.strip("/")
        if normalized in {"", "."}:
            return ""
        return normalized

    def _sanitize_job_segment(self, value: str) -> str:
        """Sanitize arbitrary text into a URL-safe job id segment."""
        cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", (value or "").strip())
        cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
        return cleaned[:80] if cleaned else ""

    def _subproject_key(self, subproject_name: str = "", subproject_path: str = "") -> str:
        """Build a stable subproject key from name/path."""
        safe_name = self._sanitize_job_segment(subproject_name)
        normalized_path = self._normalize_subproject_path(subproject_path)
        safe_path = self._sanitize_job_segment(normalized_path.replace("/", "__"))
        return safe_name or safe_path

    def _subproject_label(self, subproject_name: str = "", subproject_path: str = "") -> str:
        """Human-readable subproject label."""
        if subproject_name and subproject_name.strip():
            return subproject_name.strip()
        normalized_path = self._normalize_subproject_path(subproject_path)
        return normalized_path or ""

    def _repo_full_name_to_job_id(
        self,
        full_name: str,
        subproject_name: str = "",
        subproject_path: str = "",
        doc_type: str = "",
    ) -> str:
        """Convert repo + optional subproject/doc_type into URL-safe job ID."""
        base_id = full_name.replace("/", "--")
        sub_key = self._subproject_key(subproject_name, subproject_path)
        doc_key = self._sanitize_job_segment(normalize_doc_type_name(doc_type))
        parts = [base_id]
        if sub_key:
            parts.append(f"__sp__{sub_key}")
        if doc_key:
            parts.append(f"__dt__{doc_key}")
        return "".join(parts)

    def _parse_job_id_variants(self, job_id: str):
        """Split job_id into base/subproject/doc_type segments."""
        base = job_id
        sub_key = ""
        doc_key = ""
        if "__sp__" in base:
            base, rest = base.split("__sp__", 1)
            if "__dt__" in rest:
                sub_key, doc_key = rest.split("__dt__", 1)
            else:
                sub_key = rest
            return base, sub_key, doc_key
        if "__dt__" in base:
            base, doc_key = base.split("__dt__", 1)
        return base, sub_key, doc_key

    def _job_id_to_repo_full_name(self, job_id: str) -> str:
        """Convert job ID back to repo full name."""
        base_id, _, _ = self._parse_job_id_variants(job_id)
        return base_id.replace('--', '/')

    def _extract_doc_type(self, job: JobStatus = None, job_id: str = "") -> str:
        """Get doc_type from job options or job_id suffix."""
        if job and job.options and job.options.doc_type:
            return normalize_doc_type_name(job.options.doc_type)
        _, _, doc_key = self._parse_job_id_variants(job_id)
        return normalize_doc_type_name(doc_key)

    def _job_cache_scope(self, job_id: str) -> str:
        """Cache scope for a job variant (repo root or subproject)."""
        return job_id

    def _build_regeneration_output(self, job_id: str):
        """Return a versioned output directory and version label for regeneration."""
        version = datetime.now().strftime("%y%m%d-%H%M%S")
        output = Path(WebAppConfig.OUTPUT_DIR) / "docs" / job_id / version
        return str(output), version

    def _list_available_doc_versions(self, job_id: str, fallback_docs_path: Path):
        """List available documentation versions for a job."""
        versions = []
        seen_paths = set()

        version_root = Path(WebAppConfig.OUTPUT_DIR) / "docs" / job_id
        if version_root.exists() and version_root.is_dir():
            for child in sorted(version_root.iterdir(), key=lambda p: p.name, reverse=True):
                if (
                    child.is_dir()
                    and self.VERSION_PATTERN.match(child.name)
                    and self._has_docs_content(child)
                ):
                    resolved = str(child.resolve())
                    seen_paths.add(resolved)
                    versions.append({
                        "id": child.name,
                        "label": child.name,
                        "path": child,
                    })

        legacy_path = Path(WebAppConfig.OUTPUT_DIR) / "docs" / f"{job_id}-docs"
        if legacy_path.exists() and self._has_docs_content(legacy_path):
            resolved = str(legacy_path.resolve())
            seen_paths.add(resolved)
            versions.append({
                "id": "legacy",
                "label": "legacy",
                "path": legacy_path,
            })

        if fallback_docs_path and fallback_docs_path.exists():
            resolved_fallback = str(fallback_docs_path.resolve())
            if resolved_fallback not in seen_paths:
                versions.insert(0, {
                    "id": "current",
                    "label": "current",
                    "path": fallback_docs_path,
                })

        return versions

    def _resolve_docs_version(self, job_id: str, fallback_docs_path: Path, requested_version: str):
        """Resolve docs path by requested version; return path, version list, selected version."""
        versions = self._list_available_doc_versions(job_id, fallback_docs_path)
        selected = None

        if requested_version:
            selected = next((v for v in versions if v["id"] == requested_version), None)
            if not selected:
                raise HTTPException(status_code=404, detail=f"Version '{requested_version}' not found")
        else:
            selected = next(
                (v for v in versions if str(v["path"].resolve()) == str(fallback_docs_path.resolve())),
                None
            )
            if not selected and versions:
                selected = versions[0]

        docs_path = selected["path"] if selected else fallback_docs_path
        selected_version = selected["id"] if selected else ""
        version_items = [{"id": v["id"], "label": v["label"]} for v in versions]
        return docs_path, version_items, selected_version

    def _has_docs_content(self, path: Path) -> bool:
        """Return True if path contains docs directly or in language sub-directories."""
        if not path.exists() or not path.is_dir():
            return False
        if (path / "overview.md").exists() or (path / "module_tree.json").exists():
            return True
        for child in path.iterdir():
            if not child.is_dir():
                continue
            if (child / "overview.md").exists() or (child / "module_tree.json").exists():
                return True
        return False

    def _resolve_docs_language(self, docs_root: Path, requested_lang: str):
        """Resolve docs path by requested language; return path, language list, selected language."""
        languages = self._list_available_languages(docs_root)
        if not languages:
            return docs_root, [{"id": "", "label": "默认"}], ""

        by_id = {item["id"]: item for item in languages}
        selected = None
        requested_lang = (requested_lang or "").strip()
        if requested_lang:
            selected = by_id.get(requested_lang)
            if not selected:
                raise HTTPException(status_code=404, detail=f"Language '{requested_lang}' not found")
        else:
            # Prefer Chinese by default, then root docs, then first available language.
            selected = by_id.get("zh") or by_id.get("") or languages[0]

        language_items = [{"id": item["id"], "label": item["label"]} for item in languages]
        return selected["path"], language_items, selected["id"]

    def _list_available_languages(self, docs_root: Path):
        """List available documentation languages from docs root and language sub-directories."""
        candidates = []
        label_map = {
            "": "默认",
            "zh": "中文",
            "en": "English",
            "ja": "日本語",
            "ko": "한국어",
            "fr": "Français",
            "de": "Deutsch",
            "es": "Español",
            "pt": "Português",
            "ru": "Русский",
        }

        def is_docs_dir(path: Path):
            return (path / "overview.md").exists() or (path / "module_tree.json").exists()

        if is_docs_dir(docs_root):
            candidates.append({"id": "", "label": label_map[""], "path": docs_root})

        for child in sorted(docs_root.iterdir(), key=lambda p: p.name):
            if not child.is_dir():
                continue
            lang_id = child.name.strip()
            if not re.match(r"^[a-z]{2}(?:-[a-z]{2})?$", lang_id):
                continue
            if not is_docs_dir(child):
                continue
            label = label_map.get(lang_id, lang_id)
            candidates.append({"id": lang_id, "label": label, "path": child})

        def lang_sort_key(item):
            if item["id"] == "zh":
                return (0, item["id"])
            if item["id"] == "":
                return (1, item["id"])
            if item["id"] == "en":
                return (2, item["id"])
            return (3, item["id"])

        candidates.sort(key=lang_sort_key)
        return candidates

    def _build_fallback_navigation(self, docs_path: Path):
        """Build fallback navigation from markdown files when module_tree is empty."""
        pages = []
        for path in docs_path.rglob("*.md"):
            if not path.is_file():
                continue
            rel = path.relative_to(docs_path).as_posix()
            pages.append(rel)

        # Remove duplicates and sort with overview first.
        unique_pages = sorted(set(pages), key=lambda p: (p != "overview.md", p.lower()))
        nav_items = []
        for rel_path in unique_pages:
            stem = Path(rel_path).stem
            if rel_path == "overview.md":
                title = "Overview"
            else:
                title = stem.replace("_", " ").replace("-", " ").title()
            nav_items.append({"path": rel_path, "title": title})
        return nav_items

    def _normalize_doc_filename(self, filename: str) -> str:
        """Normalize markdown filename for fuzzy matching."""
        stem = Path(filename).stem
        stem = stem.replace("\\", "/").split("/")[-1]
        stem = re.sub(r"[_\-]+", " ", stem)
        stem = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff ]+", " ", stem)
        stem = re.sub(r"\s+", " ", stem).strip().lower()
        return stem

    def _resolve_existing_doc_file(self, docs_path: Path, filename: str):
        """
        Resolve requested markdown file by trying naming variants and fuzzy match.

        Helps when links use title-like names (e.g. `API Layer.md`) while files are
        stored as snake_case (e.g. `api_layer.md`).
        """
        requested_name = Path(filename).name
        if not requested_name.lower().endswith(".md"):
            return None

        direct = docs_path / requested_name
        if direct.exists() and direct.is_file():
            return direct

        stem = Path(requested_name).stem
        variants = [
            requested_name,
            f"{stem.replace(' ', '_')}.md",
            f"{stem.replace(' ', '-')}.md",
            f"{stem.replace('_', ' ')}.md",
            f"{stem.replace('-', ' ')}.md",
            f"{stem.lower()}.md",
            f"{stem.lower().replace(' ', '_')}.md",
            f"{stem.lower().replace(' ', '-')}.md",
        ]
        for variant in variants:
            candidate = docs_path / variant
            if candidate.exists() and candidate.is_file():
                return candidate

        target_norm = self._normalize_doc_filename(requested_name)
        if not target_norm:
            return None

        target_tokens = [token for token in target_norm.split(" ") if token]
        best = None
        best_score = -1

        for candidate in docs_path.glob("*.md"):
            cand_norm = self._normalize_doc_filename(candidate.name)
            if not cand_norm:
                continue

            if cand_norm == target_norm:
                score = 1000
            else:
                cand_tokens = [token for token in cand_norm.split(" ") if token]
                if not cand_tokens:
                    continue
                overlap = len(set(target_tokens) & set(cand_tokens))
                if overlap == 0:
                    continue
                score = overlap * 100 - abs(len(cand_tokens) - len(target_tokens)) * 10
                if cand_norm.endswith(target_norm) or cand_norm.startswith(target_norm):
                    score += 15
                if target_norm.endswith(cand_norm) or target_norm.startswith(cand_norm):
                    score += 8

            if score > best_score:
                best = candidate
                best_score = score

        if best is not None and best_score >= 80:
            return best
        return None

    def _collect_doc_type_views(self, current_job: JobStatus, current_job_id: str):
        """Backward-compatible doc-view list for current subproject."""
        return self._collect_repo_variant_options(current_job, current_job_id).get("view_options", [])

    def _repo_full_name_from_job(self, job: JobStatus = None, job_id: str = "") -> str:
        """Resolve repo full name (group/repo) from job metadata with fallbacks."""
        if job and job.repo_url:
            try:
                repo_info = GitHubRepoProcessor.get_repo_info(job.repo_url)
                full_name = (repo_info.get("full_name") or "").strip()
                if full_name:
                    return full_name
            except Exception:
                pass
        if job_id:
            return self._job_id_to_repo_full_name(job_id)
        return ""

    def _job_subproject_identity(self, job: JobStatus = None, job_id: str = "") -> tuple[str, str]:
        """Return stable subproject key and display label for job."""
        sub_key = self._subproject_key(
            job.options.subproject_name if job and job.options else "",
            job.options.subproject_path if job and job.options else "",
        )
        sub_label = self._subproject_label(
            job.options.subproject_name if job and job.options else "",
            job.options.subproject_path if job and job.options else "",
        )
        _, parsed_sub_key, _ = self._parse_job_id_variants(job_id)
        if not sub_key:
            sub_key = parsed_sub_key
        if not sub_label and parsed_sub_key:
            sub_label = parsed_sub_key.replace("__", "/")
        if not sub_key:
            sub_key = "__root__"
        if not sub_label:
            sub_label = "仓库根目录"
        return sub_key, sub_label

    def _collect_repo_variant_options(self, current_job: JobStatus, current_job_id: str) -> dict:
        """Collect subproject/doc-view options for all completed variants of the same repo."""
        current_doc_type = self._extract_doc_type(current_job, current_job_id) or "default"
        target_repo_full_name = self._repo_full_name_from_job(current_job, current_job_id)
        target_repo_normalized = ""
        if current_job and current_job.repo_url:
            target_repo_normalized = self._normalize_github_url(current_job.repo_url)

        current_sub_key, current_sub_label = self._job_subproject_identity(current_job, current_job_id)

        buckets: dict[str, dict] = {}
        for candidate in self._collect_completed_docs():
            if candidate.status != "completed" or not candidate.docs_path:
                continue
            if not Path(candidate.docs_path).exists():
                continue

            candidate_repo_full = self._repo_full_name_from_job(candidate, candidate.job_id)
            if target_repo_full_name and candidate_repo_full != target_repo_full_name:
                continue
            if target_repo_normalized:
                if self._normalize_github_url(candidate.repo_url) != target_repo_normalized:
                    continue

            sub_key, sub_label = self._job_subproject_identity(candidate, candidate.job_id)
            doc_type = self._extract_doc_type(candidate, candidate.job_id) or "default"
            completed_at = candidate.completed_at or candidate.created_at

            bucket = buckets.setdefault(sub_key, {
                "key": sub_key,
                "label": sub_label,
                "latest_at": completed_at,
                "view_map": {},
            })
            if completed_at > bucket["latest_at"]:
                bucket["latest_at"] = completed_at
                bucket["label"] = sub_label

            existing_view = bucket["view_map"].get(doc_type)
            if (not existing_view) or completed_at > existing_view["completed_at"]:
                bucket["view_map"][doc_type] = {
                    "job_id": candidate.job_id,
                    "doc_type": doc_type,
                    "label": doc_type if doc_type else "default",
                    "completed_at": completed_at,
                }

        if current_sub_key not in buckets:
            buckets[current_sub_key] = {
                "key": current_sub_key,
                "label": current_sub_label or "仓库根目录",
                "latest_at": datetime.now(),
                "view_map": {},
            }
        if current_doc_type not in buckets[current_sub_key]["view_map"]:
            buckets[current_sub_key]["view_map"][current_doc_type] = {
                "job_id": current_job_id,
                "doc_type": current_doc_type,
                "label": current_doc_type if current_doc_type else "default",
                "completed_at": datetime.now(),
            }

        view_matrix: dict[str, list[dict]] = {}
        subproject_options: list[dict] = []
        for sub_key, bucket in buckets.items():
            views = list(bucket["view_map"].values())
            views.sort(
                key=lambda item: (
                    0 if item["job_id"] == current_job_id else 1,
                    0 if item["doc_type"] == "default" else 1,
                    item["doc_type"],
                )
            )
            simplified_views = [
                {"job_id": item["job_id"], "doc_type": item["doc_type"], "label": item["label"]}
                for item in views
            ]
            view_matrix[sub_key] = simplified_views
            subproject_options.append({
                "key": sub_key,
                "label": bucket["label"],
                "job_id": simplified_views[0]["job_id"] if simplified_views else current_job_id,
            })

        subproject_options.sort(
            key=lambda item: (
                0 if item["key"] == current_sub_key else 1,
                0 if item["label"] == "仓库根目录" else 1,
                item["label"],
            )
        )
        current_view_options = view_matrix.get(current_sub_key, [])
        current_view_job_id = current_job_id
        if current_view_options:
            available_job_ids = {item["job_id"] for item in current_view_options}
            if current_job_id not in available_job_ids:
                current_view_job_id = current_view_options[0]["job_id"]

        return {
            "subproject_options": subproject_options,
            "current_subproject_key": current_sub_key,
            "current_subproject_label": current_sub_label,
            "view_options": current_view_options,
            "current_view_job_id": current_view_job_id,
            "current_doc_type": current_doc_type,
            "view_matrix": view_matrix,
        }
    
    def cleanup_old_jobs(self):
        """Clean up old job status entries."""
        cutoff = datetime.now() - timedelta(hours=WebAppConfig.JOB_CLEANUP_HOURS)
        all_jobs = self.background_worker.get_all_jobs()
        expired_jobs = [
            job_id for job_id, job in all_jobs.items()
            if job.created_at < cutoff and job.status in ['completed', 'failed']
        ]
        
        for job_id in expired_jobs:
            self.background_worker.remove_job_status(job_id)

    def _collect_completed_docs(self):
        """Collect completed docs from job status and cache index."""
        completed = {}
        
        all_jobs = self.background_worker.get_all_jobs()
        for job in all_jobs.values():
            if job.status == 'completed' and job.docs_path:
                completed[job.job_id] = job
        
        # Add cached docs that aren't tracked in job status
        for entry in self.cache_manager.cache_index.values():
            if not entry.docs_path or not Path(entry.docs_path).exists():
                continue
            job_id = (entry.job_id or "").strip()
            if not job_id:
                try:
                    repo_info = GitHubRepoProcessor.get_repo_info(entry.repo_url)
                    job_id = self._repo_full_name_to_job_id(repo_info['full_name'])
                except Exception:
                    continue
            
            if job_id in completed:
                continue
            
            completed[job_id] = JobStatus(
                job_id=job_id,
                repo_url=entry.repo_url,
                title=entry.title or GitHubRepoProcessor.generate_title(entry.repo_url),
                status='completed',
                created_at=entry.created_at,
                completed_at=entry.created_at,
                docs_path=entry.docs_path,
                progress="Retrieved from cache",
                commit_id=None
            )
        
        return sorted(
            completed.values(),
            key=lambda x: x.completed_at or x.created_at,
            reverse=True
        )
    
    async def list_tasks(self, status_filter: str = None) -> JSONResponse:
        """API endpoint to list all tasks with optional status filter."""
        all_jobs = self.background_worker.get_all_jobs()
        jobs_list = []
        
        for job_id, job in all_jobs.items():
            if status_filter and job.status != status_filter:
                continue
            jobs_list.append(JobStatusResponse(
                job_id=job.job_id,
                repo_url=job.repo_url,
                title=self._format_task_display_title(job),
                status=job.status,
                created_at=job.created_at,
                started_at=job.started_at,
                completed_at=job.completed_at,
                error_message=job.error_message,
                progress=job.progress,
                docs_path=job.docs_path,
                main_model=job.main_model,
                commit_id=job.commit_id,
                priority=job.priority,
                options=job.options,
                log_path=job.log_path
            ))
        
        jobs_list.sort(key=lambda x: x.created_at, reverse=True)
        return JSONResponse(content=jsonable_encoder(jobs_list))

    async def get_docs_engagement(self, client_id: str = "") -> JSONResponse:
        """Return engagement metrics for all visible docs cards."""
        safe_client_id = self._sanitize_client_id(client_id)
        jobs = self._collect_completed_docs()
        metrics = self._build_engagement_map(jobs, safe_client_id)
        if not safe_client_id:
            safe_client_id = self._new_client_id()
        return JSONResponse(content={"client_id": safe_client_id, "metrics": metrics})

    async def update_docs_engagement(self, job_id: str, payload: dict) -> JSONResponse:
        """Update like/favorite state for one docs card."""
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="payload must be a JSON object")

        action = str(payload.get("type", "")).strip().lower()
        if action not in {"like", "favorite"}:
            raise HTTPException(status_code=400, detail="type must be like or favorite")

        safe_client_id = self._sanitize_client_id(str(payload.get("client_id", "")))
        if not safe_client_id:
            safe_client_id = self._new_client_id()

        enabled = bool(payload.get("enabled", True))
        bucket = "likes" if action == "like" else "favorites"

        with self._engagement_lock:
            store = self._load_engagement_store_unlocked()
            users = set(store.get(bucket, {}).get(job_id, []))
            if enabled:
                users.add(safe_client_id)
            else:
                users.discard(safe_client_id)
            store.setdefault(bucket, {})[job_id] = sorted(users)
            store["updated_at"] = datetime.now().isoformat()
            self._save_engagement_store_unlocked(store)

            likes_users = set(store.get("likes", {}).get(job_id, []))
            favorites_users = set(store.get("favorites", {}).get(job_id, []))
            views_count = int(store.get("views", {}).get(job_id, 0))

        score = len(likes_users) * 3 + len(favorites_users) * 4 + views_count
        return JSONResponse(content={
            "client_id": safe_client_id,
            "job_id": job_id,
            "metrics": {
                "likes": len(likes_users),
                "favorites": len(favorites_users),
                "views": views_count,
                "liked": safe_client_id in likes_users,
                "favorited": safe_client_id in favorites_users,
                "score": score,
            },
        })
    
    async def create_task_api(
        self,
        repo_url: str,
        commit_id: str = "",
        subproject_name: str = "",
        subproject_path: str = "",
        priority: int = 0,
        output: str = "docs/codewiki",
        create_branch: bool = False,
        github_pages: bool = False,
        no_cache: bool = False,
        include: str = "",
        exclude: str = "",
        focus: str = "",
        doc_type: str = "",
        instructions: str = "",
        skills: str = "",
        max_tokens: str = "",
        max_token_per_module: str = "",
        max_token_per_leaf_module: str = "",
        max_depth: str = "",
        output_lang: str = "",
        agent_cmd: str = "",
        custom_cli_args: str = "",
        concurrency: int = 4
    ) -> JSONResponse:
        """API endpoint to create a new task."""
        repo_url = repo_url.strip()
        commit_id = commit_id.strip() if commit_id else ""
        
        if not repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")
        
        if not GitHubRepoProcessor.is_valid_github_url(repo_url):
            raise HTTPException(status_code=400, detail="Invalid Git repository URL")
        
        normalized_repo_url = self._normalize_github_url(repo_url)
        repo_info = GitHubRepoProcessor.get_repo_info(normalized_repo_url)
        normalized_subproject_path = self._normalize_subproject_path(subproject_path)
        normalized_subproject_name = (subproject_name or "").strip()
        normalized_doc_type = normalize_doc_type_name(doc_type)
        if normalized_subproject_path and (
            normalized_subproject_path == ".."
            or normalized_subproject_path.startswith("../")
            or "/../" in normalized_subproject_path
        ):
            raise HTTPException(status_code=400, detail="Invalid subproject path")
        job_id = self._repo_full_name_to_job_id(
            repo_info['full_name'],
            subproject_name=normalized_subproject_name,
            subproject_path=normalized_subproject_path,
            doc_type=normalized_doc_type,
        )
        title = GitHubRepoProcessor.generate_title(normalized_repo_url)
        subproject_label = self._subproject_label(
            subproject_name=normalized_subproject_name,
            subproject_path=normalized_subproject_path,
        )
        if subproject_label:
            title = f"{title} [{subproject_label}]"
        if normalized_doc_type:
            title = f"{title} <{normalized_doc_type}>"
        
        options = GenerationOptions(
            subproject_name=normalized_subproject_name or None,
            subproject_path=normalized_subproject_path or None,
            output=output.strip() if output and output.strip() != "docs/codewiki" else None,
            create_branch=create_branch,
            github_pages=github_pages,
            no_cache=no_cache,
            include=include.strip() if include and include.strip() else None,
            exclude=exclude.strip() if exclude and exclude.strip() else None,
            focus=focus.strip() if focus and focus.strip() else None,
            doc_type=normalized_doc_type or None,
            instructions=instructions.strip() if instructions and instructions.strip() else None,
            skills=skills.strip() if skills and skills.strip() else None,
            max_tokens=int(max_tokens) if max_tokens and max_tokens.isdigit() else None,
            max_token_per_module=int(max_token_per_module) if max_token_per_module and max_token_per_module.isdigit() else None,
            max_token_per_leaf_module=int(max_token_per_leaf_module) if max_token_per_leaf_module and max_token_per_leaf_module.isdigit() else None,
            max_depth=int(max_depth) if max_depth and max_depth.isdigit() else None,
            output_lang=output_lang.strip() if output_lang and output_lang.strip() else None,
            agent_cmd=agent_cmd.strip() if agent_cmd and agent_cmd.strip() else None,
            custom_cli_args=custom_cli_args.strip() if custom_cli_args and custom_cli_args.strip() else None,
            concurrency=concurrency
        )
        
        existing_job = self.background_worker.get_job_status(job_id)
        if existing_job and existing_job.status in ['queued', 'processing']:
            raise HTTPException(status_code=409, detail="Task already exists and is in progress")
        
        job = JobStatus(
            job_id=job_id,
            repo_url=normalized_repo_url,
            title=title,
            status='queued',
            created_at=datetime.now(),
            progress="Waiting in queue...",
            commit_id=commit_id if commit_id else None,
            priority=priority,
            options=options
        )
        
        self.background_worker.add_job(job_id, job)
        
        return JSONResponse(content={
            "job_id": job_id,
            "title": title,
            "repo_url": normalized_repo_url,
            "subproject_name": normalized_subproject_name,
            "subproject_path": normalized_subproject_path,
            "doc_type": normalized_doc_type,
            "status": "queued",
            "message": "Task created successfully"
        })

    async def list_doc_types(self) -> JSONResponse:
        """API endpoint to list all available doc-type profiles."""
        profiles = list_doc_type_profiles()
        items = []
        for key, profile in profiles.items():
            item = dict(profile)
            item["name"] = key
            items.append(item)
        items.sort(key=lambda x: x["name"])
        return JSONResponse(content={"doc_types": items})

    async def upsert_doc_type(self, doc_type: str, payload: dict) -> JSONResponse:
        """API endpoint to create/update one doc-type profile."""
        if not isinstance(payload, dict):
            raise HTTPException(status_code=400, detail="JSON payload must be an object")
        try:
            updated = upsert_doc_type_profile(doc_type, payload)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return JSONResponse(content={
            "message": "Doc type profile saved",
            "doc_type": updated,
        })

    async def delete_doc_type(self, doc_type: str) -> JSONResponse:
        """API endpoint to delete one custom doc-type profile override."""
        key = normalize_doc_type_name(doc_type)
        if not key:
            raise HTTPException(status_code=400, detail="Invalid doc_type")
        try:
            deleted = delete_doc_type_profile(key)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Custom doc type profile not found (or already removed)",
            )
        return JSONResponse(content={
            "message": "Doc type profile removed",
            "doc_type": key,
        })
    
    async def delete_task(self, job_id: str) -> JSONResponse:
        """API endpoint to delete a task."""
        job = self.background_worker.get_job_status(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if job.status == 'processing':
            raise HTTPException(status_code=400, detail="Cannot delete a task that is currently processing")
        
        self.background_worker.remove_job_status(job_id)
        self.background_worker.save_job_statuses()
        
        return JSONResponse(content={"message": "Task deleted successfully"})

    async def regenerate_task(self, job_id: str) -> JSONResponse:
        """Regenerate documentation for an existing task with a new versioned output dir."""
        job = self.background_worker.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Task not found")

        if job.status in ['queued', 'processing']:
            raise HTTPException(status_code=400, detail="Task is already queued or processing")

        output_dir, version = self._build_regeneration_output(job_id)

        base_options = {}
        if job.options:
            if hasattr(job.options, "model_dump"):
                base_options = job.options.model_dump()
            else:
                base_options = asdict(job.options)

        options = GenerationOptions(**base_options)
        options.output = output_dir
        options.no_cache = True

        new_job = JobStatus(
            job_id=job_id,
            repo_url=job.repo_url,
            title=job.title or GitHubRepoProcessor.generate_title(job.repo_url),
            status='queued',
            created_at=datetime.now(),
            progress=f"Regeneration queued (version {version})",
            commit_id=job.commit_id,
            priority=job.priority,
            options=options
        )

        self.background_worker.set_job_status(job_id, new_job)
        self.background_worker.add_job(job_id, new_job)
        self.background_worker.save_job_statuses()

        return JSONResponse(content={
            "message": "Regeneration task queued successfully",
            "job_id": job_id,
            "version": version,
            "output": output_dir
        })

    async def stop_task(self, job_id: str) -> JSONResponse:
        """Stop a queued or processing task."""
        success, message = self.background_worker.stop_job(job_id)
        if not success:
            if message == "Task not found":
                raise HTTPException(status_code=404, detail=message)
            raise HTTPException(status_code=400, detail=message)

        job = self.background_worker.get_job_status(job_id)
        return JSONResponse(content={
            "message": message,
            "job_id": job_id,
            "status": job.status if job else "unknown",
            "progress": job.progress if job else ""
        })

    async def get_task_log(self, job_id: str, tail: int = 500) -> JSONResponse:
        """Return task log text for progress inspection."""
        job = self.background_worker.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Task not found")

        log_path = job.log_path or str(self.background_worker._job_log_path(job_id))
        path = Path(log_path)
        if not path.exists():
            return JSONResponse(content={
                "job_id": job_id,
                "status": job.status,
                "log": "",
                "message": "No log available yet"
            })

        try:
            content = file_manager.load_text(path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read log: {e}")

        lines = content.splitlines()
        if tail > 0:
            lines = lines[-tail:]

        return JSONResponse(content={
            "job_id": job_id,
            "status": job.status,
            "log": "\n".join(lines),
            "log_path": str(path),
            "updated_at": datetime.now().isoformat()
        })
    
    async def admin_get(self, request: Request) -> HTMLResponse:
        """Admin page for managing tasks."""
        context = self._build_admin_context()
        return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context))
    
    async def admin_post(self, request: Request, 
                         repo_url: str = Form(...), 
                         commit_id: str = Form(""), 
                         subproject_name: str = Form(""),
                         subproject_path: str = Form(""),
                         priority: int = Form(0),
                         output: str = Form("docs/codewiki"),
                         create_branch: bool = Form(False),
                         github_pages: bool = Form(False),
                         no_cache: bool = Form(False),
                         include: str = Form(""),
                         exclude: str = Form(""),
                         focus: str = Form(""),
                         doc_type: str = Form(""),
                         instructions: str = Form(""),
                         skills: str = Form(""),
                         max_tokens: str = Form(""),
                         max_token_per_module: str = Form(""),
                         max_token_per_leaf_module: str = Form(""),
                         max_depth: str = Form(""),
                         output_lang: str = Form(""),
                         agent_cmd: str = Form(""),
                         custom_cli_args: str = Form(""),
                         concurrency: int = Form(4)) -> HTMLResponse:
        """Handle task submission from admin page."""
        repo_url = repo_url.strip()
        commit_id = commit_id.strip() if commit_id else ""
        
        if not repo_url:
            context = self._build_admin_context(error="Repository URL is required")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)
        
        if not GitHubRepoProcessor.is_valid_github_url(repo_url):
            context = self._build_admin_context(error="Invalid Git repository URL")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)
        
        normalized_repo_url = self._normalize_github_url(repo_url)
        repo_info = GitHubRepoProcessor.get_repo_info(normalized_repo_url)
        normalized_subproject_path = self._normalize_subproject_path(subproject_path)
        normalized_subproject_name = (subproject_name or "").strip()
        normalized_doc_type = normalize_doc_type_name(doc_type)
        if normalized_subproject_path and (
            normalized_subproject_path == ".."
            or normalized_subproject_path.startswith("../")
            or "/../" in normalized_subproject_path
        ):
            context = self._build_admin_context(error="Invalid subproject path")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)
        job_id = self._repo_full_name_to_job_id(
            repo_info['full_name'],
            subproject_name=normalized_subproject_name,
            subproject_path=normalized_subproject_path,
            doc_type=normalized_doc_type,
        )
        title = GitHubRepoProcessor.generate_title(normalized_repo_url)
        subproject_label = self._subproject_label(
            subproject_name=normalized_subproject_name,
            subproject_path=normalized_subproject_path,
        )
        if subproject_label:
            title = f"{title} [{subproject_label}]"
        if normalized_doc_type:
            title = f"{title} <{normalized_doc_type}>"

        options = GenerationOptions(
            subproject_name=normalized_subproject_name or None,
            subproject_path=normalized_subproject_path or None,
            output=output.strip() if output and output.strip() != "docs/codewiki" else None,
            create_branch=create_branch,
            github_pages=github_pages,
            no_cache=no_cache,
            include=include.strip() if include and include.strip() else None,
            exclude=exclude.strip() if exclude and exclude.strip() else None,
            focus=focus.strip() if focus and focus.strip() else None,
            doc_type=normalized_doc_type or None,
            instructions=instructions.strip() if instructions and instructions.strip() else None,
            skills=skills.strip() if skills and skills.strip() else None,
            max_tokens=int(max_tokens) if max_tokens and max_tokens.isdigit() else None,
            max_token_per_module=int(max_token_per_module) if max_token_per_module and max_token_per_module.isdigit() else None,
            max_token_per_leaf_module=int(max_token_per_leaf_module) if max_token_per_leaf_module and max_token_per_leaf_module.isdigit() else None,
            max_depth=int(max_depth) if max_depth and max_depth.isdigit() else None,
            output_lang=output_lang.strip() if output_lang and output_lang.strip() else None,
            agent_cmd=agent_cmd.strip() if agent_cmd and agent_cmd.strip() else None,
            custom_cli_args=custom_cli_args.strip() if custom_cli_args and custom_cli_args.strip() else None,
            concurrency=concurrency
        )
        
        existing_job = self.background_worker.get_job_status(job_id)
        if existing_job and existing_job.status in ['queued', 'processing']:
            context = self._build_admin_context(
                error=f"Task already exists and is {existing_job.status}"
            )
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=409)
        
        custom_no_cache = bool(options.custom_cli_args and "--no-cache" in options.custom_cli_args)
        cached_docs = self.cache_manager.get_cached_docs(
            normalized_repo_url,
            cache_scope=self._job_cache_scope(job_id),
        )
        if cached_docs and Path(cached_docs).exists() and not options.no_cache and not custom_no_cache:
            job = JobStatus(
                job_id=job_id,
                repo_url=normalized_repo_url,
                title=title,
                status='completed',
                created_at=datetime.now(),
                completed_at=datetime.now(),
                docs_path=cached_docs,
                progress="Retrieved from cache",
                commit_id=commit_id if commit_id else None,
                priority=priority,
                options=options
            )
        else:
            job = JobStatus(
                job_id=job_id,
                repo_url=normalized_repo_url,
                title=title,
                status='queued',
                created_at=datetime.now(),
                progress="Waiting in queue...",
                commit_id=commit_id if commit_id else None,
                priority=priority,
                options=options
            )
            self.background_worker.add_job(job_id, job)
        
        self.background_worker.set_job_status(job_id, job)
        self.background_worker.save_job_statuses()

        context = self._build_admin_context(
            message="任务已创建并加入队列",
            message_type="success",
            active_panel="panel-stats",
        )
        return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context))

    async def admin_doc_type_post(
        self,
        request: Request,
        doc_type: str = Form(...),
        display_name: str = Form(""),
        description: str = Form(""),
        prompt: str = Form(""),
        include: str = Form(""),
        exclude: str = Form(""),
        focus: str = Form(""),
        skills: str = Form(""),
        max_tokens: str = Form(""),
        max_token_per_module: str = Form(""),
        max_token_per_leaf_module: str = Form(""),
        max_depth: str = Form(""),
        profile_concurrency: str = Form(""),
    ) -> HTMLResponse:
        """Handle doc-type profile create/update from admin page."""
        key = normalize_doc_type_name(doc_type)
        if not key:
            context = self._build_admin_context(error="文档类型不能为空", active_panel="panel-doc-types")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)

        payload = {
            "display_name": display_name,
            "description": description,
            "prompt": prompt,
            "include_patterns": self._csv_to_list(include),
            "exclude_patterns": self._csv_to_list(exclude),
            "focus_modules": self._csv_to_list(focus),
            "skills": self._csv_to_list(skills),
            "max_tokens": self._str_to_int(max_tokens),
            "max_token_per_module": self._str_to_int(max_token_per_module),
            "max_token_per_leaf_module": self._str_to_int(max_token_per_leaf_module),
            "max_depth": self._str_to_int(max_depth),
            "concurrency": self._str_to_int(profile_concurrency),
        }

        try:
            saved = upsert_doc_type_profile(key, payload)
        except ValueError as e:
            context = self._build_admin_context(error=str(e), active_panel="panel-doc-types")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)

        context = self._build_admin_context(
            message=f"文档类型模板已保存: {saved.get('name', key)}",
            message_type="success",
            active_panel="panel-doc-types",
        )
        return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context))

    async def admin_doc_type_delete(
        self,
        request: Request,
        doc_type: str = Form(...),
    ) -> HTMLResponse:
        """Handle doc-type profile delete from admin page."""
        key = normalize_doc_type_name(doc_type)
        if not key:
            context = self._build_admin_context(error="文档类型不能为空", active_panel="panel-doc-types")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)

        try:
            removed = delete_doc_type_profile(key)
        except ValueError as e:
            context = self._build_admin_context(error=str(e), active_panel="panel-doc-types")
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=400)

        if not removed:
            context = self._build_admin_context(
                error=f"未找到可删除的自定义模板: {key}",
                active_panel="panel-doc-types",
            )
            return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context), status_code=404)

        context = self._build_admin_context(
            message=f"文档类型模板已删除: {key}",
            message_type="success",
            active_panel="panel-doc-types",
        )
        return HTMLResponse(content=render_template(ADMIN_TEMPLATE, context))

    def _doc_type_options(self):
        profiles = list_doc_type_profiles()

        def _list_to_csv(value) -> str:
            if not value:
                return ""
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, (list, tuple, set)):
                return ",".join(str(item).strip() for item in value if str(item).strip())
            return str(value).strip()

        options = []
        for key in sorted(profiles):
            profile = profiles[key]
            options.append({
                "name": key,
                "display_name": profile.get("display_name", ""),
                "description": profile.get("description", ""),
                "prompt": profile.get("prompt", ""),
                "include": _list_to_csv(profile.get("include_patterns")),
                "exclude": _list_to_csv(profile.get("exclude_patterns")),
                "focus": _list_to_csv(profile.get("focus_modules")),
                "skills": _list_to_csv(profile.get("skills")),
                "max_tokens": profile.get("max_tokens"),
                "max_token_per_module": profile.get("max_token_per_module"),
                "max_token_per_leaf_module": profile.get("max_token_per_leaf_module"),
                "max_depth": profile.get("max_depth"),
                "concurrency": profile.get("concurrency"),
                "built_in": bool(profile.get("built_in")),
            })
        return options

    def _format_task_display_title(self, job: JobStatus) -> str:
        """Format task title as: group/repo | 子项目(可选) | 文档类型."""
        repo_short = self._repo_full_name_from_job(job, job.job_id)
        if not repo_short:
            repo_short = job.repo_url or job.job_id

        subproject_label = self._subproject_label(
            job.options.subproject_name if job.options else "",
            job.options.subproject_path if job.options else "",
        )
        if not subproject_label:
            _, sub_key, _ = self._parse_job_id_variants(job.job_id)
            if sub_key:
                subproject_label = sub_key.replace("__", "/")

        doc_type = self._extract_doc_type(job, job.job_id) or "default"
        parts = [repo_short]
        if subproject_label:
            parts.append(subproject_label)
        parts.append(doc_type)
        return " | ".join(parts)

    def _build_admin_context(
        self,
        error: str = None,
        message: str = None,
        message_type: str = None,
        active_panel: str = None,
    ):
        all_jobs = self.background_worker.get_all_jobs()
        jobs_list = sorted(all_jobs.values(), key=lambda x: x.created_at, reverse=True)
        for job in jobs_list:
            setattr(job, "display_title", self._format_task_display_title(job))
        queued_count = sum(1 for j in jobs_list if j.status == 'queued')
        processing_count = sum(1 for j in jobs_list if j.status == 'processing')
        completed_count = sum(1 for j in jobs_list if j.status == 'completed')
        failed_count = sum(1 for j in jobs_list if j.status == 'failed')
        return {
            "error": error,
            "message": message,
            "message_type": message_type,
            "jobs": jobs_list,
            "queued_count": queued_count,
            "processing_count": processing_count,
            "completed_count": completed_count,
            "failed_count": failed_count,
            "total_count": len(jobs_list),
            "doc_type_options": self._doc_type_options(),
            "task_concurrency": self.background_worker.worker_concurrency,
            "task_concurrency_max": WebAppConfig.MAX_TASK_CONCURRENCY,
            "agent_base_url": WebAppConfig.AGENT_MODEL_BASE_URL,
            "agent_models": ", ".join(WebAppConfig.AGENT_MODEL_NAMES),
            "agent_api_key_set": bool(WebAppConfig.AGENT_MODEL_API_KEY),
            "active_panel": active_panel or "",
        }

    def _new_client_id(self) -> str:
        return f"c{secrets.token_hex(8)}"

    def _sanitize_client_id(self, value: str) -> str:
        text = (value or "").strip()
        if not text:
            return ""
        text = re.sub(r"[^a-zA-Z0-9_-]", "", text)
        return text[:64]

    def _default_engagement_store(self) -> dict:
        return {
            "likes": {},
            "favorites": {},
            "views": {},
            "updated_at": "",
        }

    def _load_engagement_store_unlocked(self) -> dict:
        if not self._engagement_file.exists():
            return self._default_engagement_store()
        try:
            data = file_manager.load_json(self._engagement_file)
        except Exception:
            return self._default_engagement_store()
        if not isinstance(data, dict):
            return self._default_engagement_store()

        normalized = self._default_engagement_store()
        for key in ("likes", "favorites"):
            payload = data.get(key, {})
            if not isinstance(payload, dict):
                continue
            for job_id, users in payload.items():
                if not isinstance(job_id, str):
                    continue
                if not isinstance(users, list):
                    continue
                clean_users = set()
                for item in users:
                    safe = self._sanitize_client_id(str(item))
                    if safe:
                        clean_users.add(safe)
                normalized[key][job_id] = sorted(clean_users)

        views_payload = data.get("views", {})
        if isinstance(views_payload, dict):
            for job_id, views in views_payload.items():
                if not isinstance(job_id, str):
                    continue
                try:
                    normalized["views"][job_id] = max(0, int(views))
                except (TypeError, ValueError):
                    continue
        normalized["updated_at"] = str(data.get("updated_at", "") or "")
        return normalized

    def _save_engagement_store_unlocked(self, data: dict) -> None:
        self._engagement_file.parent.mkdir(parents=True, exist_ok=True)
        file_manager.save_json(data, self._engagement_file)

    def _record_doc_view(self, job_id: str) -> None:
        with self._engagement_lock:
            store = self._load_engagement_store_unlocked()
            views = int(store.get("views", {}).get(job_id, 0))
            store.setdefault("views", {})[job_id] = views + 1
            store["updated_at"] = datetime.now().isoformat()
            self._save_engagement_store_unlocked(store)

    def _build_engagement_map(self, jobs: list[JobStatus], client_id: str = "") -> dict[str, dict]:
        with self._engagement_lock:
            store = self._load_engagement_store_unlocked()

        client_id = self._sanitize_client_id(client_id)
        metrics = {}
        for job in jobs:
            job_id = job.job_id
            likes_users = set(store.get("likes", {}).get(job_id, []))
            favorites_users = set(store.get("favorites", {}).get(job_id, []))
            views_count = int(store.get("views", {}).get(job_id, 0))
            metrics[job_id] = {
                "likes": len(likes_users),
                "favorites": len(favorites_users),
                "views": views_count,
                "liked": bool(client_id and client_id in likes_users),
                "favorited": bool(client_id and client_id in favorites_users),
                "score": len(likes_users) * 3 + len(favorites_users) * 4 + views_count,
            }
        return metrics

    def _safe_doc_stats(self, docs_path_value: str | None) -> tuple[int, int]:
        if not docs_path_value:
            return 0, 0
        docs_path = Path(docs_path_value)
        if not docs_path.exists():
            return 0, 0

        components_count = 0
        metadata_file = docs_path / "metadata.json"
        if metadata_file.exists():
            try:
                metadata = file_manager.load_json(metadata_file)
                if isinstance(metadata, dict):
                    stats = metadata.get("statistics", {})
                    if isinstance(stats, dict):
                        components_count = int(stats.get("total_components", 0))
            except Exception:
                components_count = 0

        markdown_files = 0
        try:
            markdown_files = sum(1 for _ in docs_path.glob("*.md"))
            if markdown_files == 0:
                markdown_files = sum(1 for _ in docs_path.rglob("*.md"))
        except Exception:
            markdown_files = 0
        return components_count, markdown_files

    def _doc_type_icon(self, doc_type: str) -> str:
        """Map doc_type to compact icon for homepage cards."""
        key = normalize_doc_type_name(doc_type)
        if key in {"architecture", "arch"}:
            return "🏗"
        if key in {"developer", "dev"}:
            return "💻"
        if key in {"api"}:
            return "🔌"
        if key in {"overview", "summary"}:
            return "📘"
        if key in {"ops", "operation", "runbook"}:
            return "🛠"
        if key in {"product", "prd"}:
            return "🧭"
        return "📄"

    def _build_home_cards(self, jobs: list[JobStatus]) -> tuple[list[dict], list[dict], dict]:
        metrics_map = self._build_engagement_map(jobs)
        repo_groups: dict[str, dict] = {}
        for job in jobs:
            components_count, file_count = self._safe_doc_stats(job.docs_path)
            doc_type = self._extract_doc_type(job, job.job_id) or "default"
            subproject_key, subproject_label = self._job_subproject_identity(job, job.job_id)
            repo_short = self._repo_full_name_from_job(job, job.job_id) or self._job_id_to_repo_full_name(job.job_id)
            completed_at = job.completed_at or job.created_at
            metrics = metrics_map.get(job.job_id, {})
            group_key = repo_short.lower() or job.job_id.lower()
            group = repo_groups.setdefault(group_key, {
                "repo_short": repo_short,
                "repo_url": job.repo_url,
                "primary_job_id": job.job_id,
                "primary_doc_type": doc_type,
                "latest_at": completed_at,
                "created_at": job.created_at,
                "completed_at": completed_at,
                "status": "completed",
                "progress": "",
                "components_count": components_count,
                "file_count": file_count,
                "likes": int(metrics.get("likes", 0)),
                "favorites": int(metrics.get("favorites", 0)),
                "views": int(metrics.get("views", 0)),
                "doc_type_map": {},
                "subproject_map": {},
            })
            if completed_at >= group["latest_at"]:
                group["latest_at"] = completed_at
                group["primary_job_id"] = job.job_id
                group["primary_doc_type"] = doc_type
                group["repo_url"] = job.repo_url
                group["created_at"] = job.created_at
                group["completed_at"] = completed_at
                group["likes"] = int(metrics.get("likes", 0))
                group["favorites"] = int(metrics.get("favorites", 0))
                group["views"] = int(metrics.get("views", 0))

            group["components_count"] = max(group["components_count"], components_count)
            group["file_count"] = max(group["file_count"], file_count)

            existing_doc = group["doc_type_map"].get(doc_type)
            if (not existing_doc) or completed_at > existing_doc["completed_at"]:
                group["doc_type_map"][doc_type] = {
                    "name": doc_type,
                    "icon": self._doc_type_icon(doc_type),
                    "job_id": job.job_id,
                    "completed_at": completed_at,
                }

            existing_sub = group["subproject_map"].get(subproject_key)
            if (not existing_sub) or completed_at > existing_sub["completed_at"]:
                group["subproject_map"][subproject_key] = {
                    "key": subproject_key,
                    "label": subproject_label or "仓库根目录",
                    "completed_at": completed_at,
                }

        cards: list[dict] = []
        for group in repo_groups.values():
            doc_types = list(group["doc_type_map"].values())
            doc_types.sort(
                key=lambda item: (
                    0 if item["name"] == group["primary_doc_type"] else 1,
                    0 if item["name"] == "default" else 1,
                    item["name"],
                )
            )
            doc_type_names = [item["name"] for item in doc_types]

            subprojects = list(group["subproject_map"].values())
            subprojects.sort(
                key=lambda item: (
                    0 if item["label"] == "仓库根目录" else 1,
                    item["label"],
                )
            )
            subproject_labels = [item["label"] for item in subprojects]

            cards.append({
                "job_id": group["primary_job_id"],
                "title": group["repo_short"],
                "display_title": group["repo_short"],
                "repo_url": group["repo_url"],
                "created_at": group["created_at"].strftime("%Y-%m-%d %H:%M"),
                "completed_at": group["completed_at"].strftime("%Y-%m-%d %H:%M"),
                "doc_type": ", ".join(doc_type_names),
                "doc_type_icon": self._doc_type_icon(group["primary_doc_type"]),
                "doc_types": [{"name": item["name"], "icon": item["icon"], "job_id": item["job_id"]} for item in doc_types],
                "subproject": ", ".join(subproject_labels) if subproject_labels else "仓库根目录",
                "subprojects": subproject_labels or ["仓库根目录"],
                "status": group["status"],
                "progress": group["progress"],
                "components_count": group["components_count"],
                "file_count": group["file_count"],
                "likes": group["likes"],
                "favorites": group["favorites"],
                "views": group["views"],
                "score": group["likes"] * 3 + group["favorites"] * 4 + group["views"],
            })

        leaderboard = sorted(cards, key=lambda item: (item["score"], item["views"]), reverse=True)[:10]
        stats = {
            "total_docs": len(cards),
            "total_components": sum(item["components_count"] for item in cards),
            "total_files": sum(item["file_count"] for item in cards),
            "total_views": sum(item["views"] for item in cards),
        }
        return cards, leaderboard, stats

    def _csv_to_list(self, value: str):
        text = (value or "").strip()
        if not text:
            return None
        parts = [part.strip() for part in text.split(",")]
        result = [part for part in parts if part]
        return result or None

    def _str_to_int(self, value: str):
        text = (value or "").strip()
        if not text:
            return None
        try:
            parsed = int(text)
        except ValueError:
            return None
        return parsed if parsed > 0 else None
