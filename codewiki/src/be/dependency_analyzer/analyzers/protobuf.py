"""
Google Protobuf (.proto) analyzer.

This analyzer extracts key protobuf components:
- message
- enum
- service
- rpc

And builds dependency-like relationships:
- message field type references
- rpc request/response type references
- service -> rpc containment
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from codewiki.src.be.dependency_analyzer.models.core import CallRelationship, Node

logger = logging.getLogger(__name__)


PROTO_SCALAR_TYPES = {
    "double",
    "float",
    "int32",
    "int64",
    "uint32",
    "uint64",
    "sint32",
    "sint64",
    "fixed32",
    "fixed64",
    "sfixed32",
    "sfixed64",
    "bool",
    "string",
    "bytes",
}

BLOCK_START_RE = re.compile(r"^\s*(message|enum|service)\s+([A-Za-z_]\w*)\b")
PACKAGE_RE = re.compile(r"^\s*package\s+([A-Za-z_][\w.]*)\s*;")
RPC_RE = re.compile(
    r"^\s*rpc\s+([A-Za-z_]\w*)\s*\(\s*(?:stream\s+)?([.\w]+)\s*\)\s*returns\s*\(\s*(?:stream\s+)?([.\w]+)\s*\)"
)
MAP_FIELD_RE = re.compile(r"\bmap\s*<\s*([.\w]+)\s*,\s*([.\w]+)\s*>\s+\w+\s*=")
FIELD_RE = re.compile(r"^\s*(?:repeated|required|optional)?\s*([.\w]+)\s+\w+\s*=")


class ProtobufAnalyzer:
    """Line-based analyzer for protobuf files."""

    def __init__(self, file_path: str, content: str, repo_path: Optional[str] = None):
        self.file_path = Path(file_path)
        self.content = content
        self.repo_path = repo_path or ""
        self.lines = content.splitlines()
        self.package_name = ""

        self.nodes: List[Node] = []
        self.relationships: List[CallRelationship] = []

        self._definitions: List[Dict] = []
        self._node_id_by_full_name: Dict[str, str] = {}
        self._full_names_by_simple_name: Dict[str, set[str]] = {}
        self._type_refs: List[Dict] = []
        self._direct_relations: List[CallRelationship] = []

    def _get_relative_path(self) -> str:
        if self.repo_path:
            try:
                return os.path.relpath(str(self.file_path), self.repo_path)
            except ValueError:
                pass
        return str(self.file_path)

    def _get_module_path(self) -> str:
        rel_path = self._get_relative_path()
        if rel_path.endswith(".proto"):
            rel_path = rel_path[:-6]
        return rel_path.replace("/", ".").replace("\\", ".")

    def _get_component_id(self, full_name: str) -> str:
        return f"{self._get_module_path()}.{full_name}"

    def _strip_comments(self, line: str, in_block_comment: bool) -> Tuple[str, bool]:
        out = []
        i = 0
        n = len(line)
        while i < n:
            if in_block_comment:
                end = line.find("*/", i)
                if end == -1:
                    return "".join(out), True
                i = end + 2
                in_block_comment = False
                continue

            ch = line[i]
            if ch == "/" and i + 1 < n:
                nxt = line[i + 1]
                if nxt == "/":
                    break
                if nxt == "*":
                    in_block_comment = True
                    i += 2
                    continue

            out.append(ch)
            i += 1
        return "".join(out), in_block_comment

    def _find_nearest(self, stack: List[Dict], kinds: set[str]) -> Optional[Dict]:
        for item in reversed(stack):
            if item["kind"] in kinds:
                return item
        return None

    def _register_name(self, full_name: str, component_id: str):
        self._node_id_by_full_name[full_name] = component_id
        simple = full_name.split(".")[-1]
        self._full_names_by_simple_name.setdefault(simple, set()).add(full_name)

    def _scan(self):
        stack: List[Dict] = []
        brace_depth = 0
        in_block_comment = False

        for lineno, raw in enumerate(self.lines, start=1):
            line, in_block_comment = self._strip_comments(raw, in_block_comment)
            stripped = line.strip()
            depth_before = brace_depth

            if stripped and not self.package_name:
                m_pkg = PACKAGE_RE.match(stripped)
                if m_pkg:
                    self.package_name = m_pkg.group(1)

            # Detect block definitions (message/enum/service)
            m_block = BLOCK_START_RE.match(stripped)
            if m_block:
                kind, name = m_block.groups()
                parent = self._find_nearest(stack, {"message", "enum", "service"})
                parent_full = parent["full_name"] if parent else ""
                full_name = f"{parent_full}.{name}" if parent_full else name

                self._definitions.append(
                    {
                        "kind": kind,
                        "name": name,
                        "full_name": full_name,
                        "parent_full_name": parent_full,
                        "start_line": lineno,
                        "end_line": lineno,
                    }
                )
                def_idx = len(self._definitions) - 1

                if "{" in stripped[m_block.end() :]:
                    stack.append(
                        {
                            "kind": kind,
                            "full_name": full_name,
                            "start_depth": depth_before,
                            "def_idx": def_idx,
                        }
                    )

            current_service = self._find_nearest(stack, {"service"})
            current_message = self._find_nearest(stack, {"message"})

            # Extract RPCs inside services
            if current_service:
                m_rpc = RPC_RE.match(stripped)
                if m_rpc:
                    rpc_name, req_type, resp_type = m_rpc.groups()
                    service_full = current_service["full_name"]
                    rpc_full = f"{service_full}.{rpc_name}"
                    self._definitions.append(
                        {
                            "kind": "rpc",
                            "name": rpc_name,
                            "full_name": rpc_full,
                            "parent_full_name": service_full,
                            "start_line": lineno,
                            "end_line": lineno,
                            "request_type": req_type,
                            "response_type": resp_type,
                        }
                    )
                    self._type_refs.append(
                        {
                            "caller_full_name": rpc_full,
                            "scope_full_name": rpc_full,
                            "type_name": req_type,
                            "line": lineno,
                        }
                    )
                    self._type_refs.append(
                        {
                            "caller_full_name": rpc_full,
                            "scope_full_name": rpc_full,
                            "type_name": resp_type,
                            "line": lineno,
                        }
                    )
                    self._direct_relations.append(
                        CallRelationship(
                            caller=self._get_component_id(service_full),
                            callee=self._get_component_id(rpc_full),
                            call_line=lineno,
                            is_resolved=True,
                        )
                    )

            # Extract field type references inside messages
            if current_message:
                for mt in MAP_FIELD_RE.finditer(stripped):
                    for type_name in (mt.group(1), mt.group(2)):
                        self._type_refs.append(
                            {
                                "caller_full_name": current_message["full_name"],
                                "scope_full_name": current_message["full_name"],
                                "type_name": type_name,
                                "line": lineno,
                            }
                        )

                m_field = FIELD_RE.match(stripped)
                if m_field:
                    self._type_refs.append(
                        {
                            "caller_full_name": current_message["full_name"],
                            "scope_full_name": current_message["full_name"],
                            "type_name": m_field.group(1),
                            "line": lineno,
                        }
                    )

            opens = line.count("{")
            closes = line.count("}")
            brace_depth += opens - closes

            # Close any finished blocks.
            while stack and brace_depth <= stack[-1]["start_depth"]:
                top = stack.pop()
                self._definitions[top["def_idx"]]["end_line"] = lineno

        # Ensure any unclosed blocks still get a useful range.
        max_line = max(1, len(self.lines))
        while stack:
            top = stack.pop()
            self._definitions[top["def_idx"]]["end_line"] = max_line

    def _resolve_type_name(self, type_name: str, scope_full_name: str) -> Optional[str]:
        cleaned = (type_name or "").strip()
        if not cleaned:
            return None
        cleaned = cleaned.lstrip(".")

        scalar = cleaned.lower()
        if scalar in PROTO_SCALAR_TYPES:
            return None

        if self.package_name and cleaned.startswith(f"{self.package_name}."):
            cleaned = cleaned[len(self.package_name) + 1 :]

        candidates: List[str] = [cleaned]
        scope_parts = [p for p in scope_full_name.split(".") if p]
        for i in range(len(scope_parts), 0, -1):
            candidates.append(".".join(scope_parts[:i] + [cleaned]))

        # Direct full-name matches first.
        seen = set()
        for cand in candidates:
            if cand in seen:
                continue
            seen.add(cand)
            if cand in self._node_id_by_full_name:
                return self._node_id_by_full_name[cand]

        # Fallback to unique simple-name match.
        simple = cleaned.split(".")[-1]
        full_set = self._full_names_by_simple_name.get(simple, set())
        if len(full_set) == 1:
            full = next(iter(full_set))
            return self._node_id_by_full_name.get(full)

        # Keep unresolved reference readable.
        return cleaned

    def analyze(self):
        self._scan()
        module_path = self._get_module_path()

        # Build nodes and definition index.
        for definition in self._definitions:
            kind = definition["kind"]
            full_name = definition["full_name"]
            component_id = self._get_component_id(full_name)
            self._register_name(full_name, component_id)

            component_type = "function"
            if kind == "service":
                component_type = "interface"
            elif kind in {"message", "enum"}:
                component_type = "struct"

            start = definition["start_line"]
            end = max(start, definition["end_line"])
            code_snippet = "\n".join(self.lines[start - 1 : end])

            node = Node(
                id=component_id,
                name=definition["name"],
                component_type=component_type,
                file_path=str(self.file_path),
                relative_path=self._get_relative_path(),
                source_code=code_snippet,
                start_line=start,
                end_line=end,
                has_docstring=False,
                docstring="",
                parameters=None,
                node_type=kind,
                base_classes=None,
                class_name=definition.get("parent_full_name") or None,
                display_name=f"{kind} {full_name}",
                component_id=component_id,
            )
            self.nodes.append(node)

        # Add explicit direct relations (service -> rpc).
        self.relationships.extend(self._direct_relations)

        # Resolve collected type references.
        for ref in self._type_refs:
            caller_id = self._node_id_by_full_name.get(ref["caller_full_name"])
            if not caller_id:
                continue
            resolved = self._resolve_type_name(ref["type_name"], ref["scope_full_name"])
            if not resolved:
                continue
            self.relationships.append(
                CallRelationship(
                    caller=caller_id,
                    callee=resolved,
                    call_line=ref["line"],
                    is_resolved=resolved in self._node_id_by_full_name.values(),
                )
            )

        logger.debug(
            "Protobuf analysis complete for %s: %d nodes, %d relationships",
            self.file_path,
            len(self.nodes),
            len(self.relationships),
        )


def analyze_protobuf_file(
    file_path: str,
    content: str,
    repo_path: Optional[str] = None,
) -> Tuple[List[Node], List[CallRelationship]]:
    analyzer = ProtobufAnalyzer(file_path=file_path, content=content, repo_path=repo_path)
    analyzer.analyze()
    return analyzer.nodes, analyzer.relationships
