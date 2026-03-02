#!/usr/bin/env python3
"""
Data models and classes for the CodeWiki web application.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
import shlex
from pydantic import BaseModel, HttpUrl


class GenerationOptions(BaseModel):
    """Options for documentation generation."""
    output: Optional[str] = "docs/codewiki"
    create_branch: bool = False
    github_pages: bool = False
    no_cache: bool = False
    include: Optional[str] = None
    exclude: Optional[str] = None
    focus: Optional[str] = None
    doc_type: Optional[str] = None
    instructions: Optional[str] = None
    max_tokens: Optional[int] = None
    max_token_per_module: Optional[int] = None
    max_token_per_leaf_module: Optional[int] = None
    max_depth: Optional[int] = None
    output_lang: Optional[str] = None
    agent_cmd: Optional[str] = None
    custom_cli_args: Optional[str] = None
    concurrency: int = 4

    def to_cli_args(self) -> list:
        """Convert options to CLI arguments list."""
        args = []
        if self.output and self.output != "docs/codewiki":
            args.extend(["--output", self.output])
        if self.create_branch:
            args.append("--create-branch")
        if self.github_pages:
            args.append("--github-pages")
        if self.no_cache:
            args.append("--no-cache")
        if self.include:
            args.extend(["--include", self.include])
        if self.exclude:
            args.extend(["--exclude", self.exclude])
        if self.focus:
            args.extend(["--focus", self.focus])
        if self.doc_type:
            args.extend(["--doc-type", self.doc_type])
        if self.instructions:
            args.extend(["--instructions", self.instructions])
        if self.max_tokens is not None:
            args.extend(["--max-tokens", str(self.max_tokens)])
        if self.max_token_per_module is not None:
            args.extend(["--max-token-per-module", str(self.max_token_per_module)])
        if self.max_token_per_leaf_module is not None:
            args.extend(["--max-token-per-leaf-module", str(self.max_token_per_leaf_module)])
        if self.max_depth is not None:
            args.extend(["--max-depth", str(self.max_depth)])
        if self.output_lang:
            args.extend(["--output-lang", self.output_lang])
        if self.agent_cmd:
            args.extend(["--with-agent-cmd", self.agent_cmd])
        if self.custom_cli_args:
            args.extend(shlex.split(self.custom_cli_args))
        if self.concurrency != 4:
            args.extend(["--concurrency", str(self.concurrency)])
        return args


class RepositorySubmission(BaseModel):
    """Pydantic model for repository submission form."""
    repo_url: HttpUrl


class JobStatusResponse(BaseModel):
    """Pydantic model for job status API response."""
    job_id: str
    repo_url: str
    title: str = ""
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    progress: str = ""
    docs_path: Optional[str] = None
    main_model: Optional[str] = None
    commit_id: Optional[str] = None
    priority: int = 0
    options: Optional[GenerationOptions] = None
    log_path: Optional[str] = None


@dataclass
class JobStatus:
    """Tracks the status of a documentation generation job."""
    job_id: str
    repo_url: str
    status: str  # 'queued', 'processing', 'completed', 'failed', 'stopped'
    created_at: datetime
    title: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    progress: str = ""
    docs_path: Optional[str] = None
    main_model: Optional[str] = None
    commit_id: Optional[str] = None
    priority: int = 0
    options: Optional[GenerationOptions] = None
    log_path: Optional[str] = None


@dataclass
class CacheEntry:
    """Represents a cached documentation result."""
    repo_url: str
    repo_url_hash: str
    docs_path: str
    created_at: datetime
    last_accessed: datetime
