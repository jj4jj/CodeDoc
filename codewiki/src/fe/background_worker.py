#!/usr/bin/env python3
"""
Background worker for processing documentation generation jobs.
"""

import os
import json
import time
import threading
import subprocess
import asyncio
import traceback
import shlex
import argparse
from datetime import datetime
from pathlib import Path
from queue import Queue
from typing import Dict, Tuple, List, Set
from dataclasses import asdict

from codewiki.src.be.documentation_generator import DocumentationGenerator
from codewiki.src.config import Config, MAIN_MODEL
from .models import JobStatus, GenerationOptions
from .cache_manager import CacheManager
from .github_processor import GitHubRepoProcessor
from .config import WebAppConfig
from codewiki.src.utils import file_manager
from codewiki.cli.html_generator import HTMLGenerator


CUSTOM_CLI_ARG_PARSER = argparse.ArgumentParser(add_help=False)
CUSTOM_CLI_ARG_PARSER.add_argument("--output", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--max-depth", type=int)
CUSTOM_CLI_ARG_PARSER.add_argument("--max-tokens", type=int)
CUSTOM_CLI_ARG_PARSER.add_argument("--max-token-per-module", type=int)
CUSTOM_CLI_ARG_PARSER.add_argument("--max-token-per-leaf-module", type=int)
CUSTOM_CLI_ARG_PARSER.add_argument("--output-lang", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--with-agent-cmd", "--agent-cmd", dest="agent_cmd", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--include", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--exclude", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--focus", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--doc-type", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--instructions", type=str)
CUSTOM_CLI_ARG_PARSER.add_argument("--concurrency", type=int)
CUSTOM_CLI_ARG_PARSER.add_argument("--github-pages", action="store_true")
CUSTOM_CLI_ARG_PARSER.add_argument("--no-cache", action="store_true")


class JobStoppedError(Exception):
    """Raised when a running job is stopped by user request."""


class BackgroundWorker:
    """Background worker for processing documentation generation jobs."""
    
    def __init__(self, cache_manager: CacheManager, temp_dir: str = None):
        self.cache_manager = cache_manager
        self.temp_dir = temp_dir or WebAppConfig.TEMP_DIR
        self.running = False
        self.processing_queue = Queue(maxsize=WebAppConfig.QUEUE_SIZE)
        self.job_status: Dict[str, JobStatus] = {}
        self.stop_requests: Set[str] = set()
        self._stop_lock = threading.Lock()
        self._active_async_tasks: Dict[str, Tuple[asyncio.AbstractEventLoop, asyncio.Task]] = {}
        self.jobs_file = Path(WebAppConfig.CACHE_DIR) / "jobs.json"
        self.load_job_statuses()

    def _job_log_path(self, job_id: str) -> Path:
        logs_dir = Path(WebAppConfig.CACHE_DIR) / "job_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir / f"{job_id}.log"

    def _append_job_log(self, job: JobStatus, message: str):
        try:
            if not job.log_path:
                job.log_path = str(self._job_log_path(job.job_id))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(job.log_path, "a", encoding="utf-8") as fh:
                fh.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def _set_progress(self, job: JobStatus, progress: str):
        job.progress = progress
        self._append_job_log(job, progress)

    def _is_stop_requested(self, job_id: str) -> bool:
        with self._stop_lock:
            return job_id in self.stop_requests

    def _request_stop(self, job_id: str):
        with self._stop_lock:
            self.stop_requests.add(job_id)

    def _clear_stop_request(self, job_id: str):
        with self._stop_lock:
            self.stop_requests.discard(job_id)
            self._active_async_tasks.pop(job_id, None)

    def _check_stop_requested(self, job: JobStatus):
        if self._is_stop_requested(job.job_id):
            raise JobStoppedError("Task stopped by user")

    def stop_job(self, job_id: str) -> Tuple[bool, str]:
        """Request stop for a queued/processing job."""
        job = self.job_status.get(job_id)
        if not job:
            return False, "Task not found"

        if job.status == "queued":
            self._request_stop(job_id)
            job.status = "stopped"
            job.completed_at = datetime.now()
            self._set_progress(job, "Task stopped before processing started")
            self.save_job_statuses()
            return True, "Task stopped"

        if job.status == "processing":
            self._request_stop(job_id)
            self._set_progress(job, "Stop requested by user, attempting to cancel...")
            with self._stop_lock:
                task_info = self._active_async_tasks.get(job_id)
            if task_info:
                loop, task = task_info
                try:
                    loop.call_soon_threadsafe(task.cancel)
                except Exception:
                    pass
            self.save_job_statuses()
            return True, "Stop request sent"

        return False, f"Task cannot be stopped in status: {job.status}"

    def _parse_custom_cli_args(self, custom_cli_args: str) -> Tuple[argparse.Namespace, List[str]]:
        tokens = shlex.split(custom_cli_args)
        return CUSTOM_CLI_ARG_PARSER.parse_known_args(tokens)

    def _apply_custom_cli_args_to_config(self, config: Config, parsed_args: argparse.Namespace):
        if parsed_args.output:
            config.docs_dir = parsed_args.output
        if parsed_args.max_depth is not None:
            config.max_depth = parsed_args.max_depth
        if parsed_args.max_tokens is not None:
            config.max_tokens = parsed_args.max_tokens
        if parsed_args.max_token_per_module is not None:
            config.max_token_per_module = parsed_args.max_token_per_module
        if parsed_args.max_token_per_leaf_module is not None:
            config.max_token_per_leaf_module = parsed_args.max_token_per_leaf_module
        if parsed_args.agent_cmd:
            config.agent_cmd = parsed_args.agent_cmd
        if parsed_args.concurrency is not None:
            config.concurrency = max(1, parsed_args.concurrency)

        if (
            parsed_args.include
            or parsed_args.exclude
            or parsed_args.focus
            or parsed_args.doc_type
            or parsed_args.instructions
        ):
            config.agent_instructions = config.agent_instructions or {}
            if parsed_args.include:
                config.agent_instructions["include_patterns"] = [
                    part.strip() for part in parsed_args.include.split(",") if part.strip()
                ]
            if parsed_args.exclude:
                config.agent_instructions["exclude_patterns"] = [
                    part.strip() for part in parsed_args.exclude.split(",") if part.strip()
                ]
            if parsed_args.focus:
                config.agent_instructions["focus_modules"] = [
                    part.strip() for part in parsed_args.focus.split(",") if part.strip()
                ]
            if parsed_args.doc_type:
                config.agent_instructions["doc_type"] = parsed_args.doc_type
            if parsed_args.instructions:
                config.agent_instructions["custom_instructions"] = parsed_args.instructions
    
    def start(self):
        """Start the background worker thread."""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._worker_loop, daemon=True)
            thread.start()
            print("Background worker started")
    
    def stop(self):
        """Stop the background worker."""
        self.running = False
    
    def add_job(self, job_id: str, job: JobStatus):
        """Add a job to the processing queue."""
        self.job_status[job_id] = job
        self.processing_queue.put(job_id)
    
    def get_job_status(self, job_id: str) -> JobStatus:
        """Get job status by ID."""
        return self.job_status.get(job_id)
    
    def get_all_jobs(self) -> Dict[str, JobStatus]:
        """Get all job statuses."""
        return self.job_status
    
    def load_job_statuses(self):
        """Load job statuses from disk."""
        if not self.jobs_file.exists():
            # Try to reconstruct from cache if no job file exists
            self._reconstruct_jobs_from_cache()
            return
        
        try:
            data = file_manager.load_json(self.jobs_file)
                
            for job_id, job_data in data.items():
                # Only load completed jobs to avoid inconsistent state
                if job_data.get('status') == 'completed':
                    options = None
                    if job_data.get('options'):
                        try:
                            options = GenerationOptions(**job_data['options'])
                        except Exception:
                            pass
                    self.job_status[job_id] = JobStatus(
                        job_id=job_data['job_id'],
                        repo_url=job_data['repo_url'],
                        title=job_data.get('title', GitHubRepoProcessor.generate_title(job_data['repo_url']) if job_data.get('repo_url') else ""),
                        status=job_data['status'],
                        created_at=datetime.fromisoformat(job_data['created_at']),
                        started_at=datetime.fromisoformat(job_data['started_at']) if job_data.get('started_at') else None,
                        completed_at=datetime.fromisoformat(job_data['completed_at']) if job_data.get('completed_at') else None,
                        error_message=job_data.get('error_message'),
                        progress=job_data.get('progress', ''),
                        docs_path=job_data.get('docs_path'),
                        main_model=job_data.get('main_model'),
                        commit_id=job_data.get('commit_id'),
                        priority=job_data.get('priority', 0),
                        options=options,
                        log_path=job_data.get('log_path')
                    )
            print(f"Loaded {len([j for j in self.job_status.values() if j.status == 'completed'])} completed jobs from disk")
        except Exception as e:
            print(f"Error loading job statuses: {e}")
    
    def _reconstruct_jobs_from_cache(self):
        """Reconstruct job statuses from cache entries for backward compatibility."""
        try:
            cache_entries = self.cache_manager.cache_index
            reconstructed_count = 0
            
            for repo_hash, cache_entry in cache_entries.items():
                # Extract repo info to create job_id
                from .github_processor import GitHubRepoProcessor
                try:
                    repo_info = GitHubRepoProcessor.get_repo_info(cache_entry.repo_url)
                    job_id = repo_info['full_name'].replace('/', '--')
                    
                    # Only add if job doesn't already exist
                    if job_id not in self.job_status:
                        self.job_status[job_id] = JobStatus(
                            job_id=job_id,
                            repo_url=cache_entry.repo_url,
                            title=GitHubRepoProcessor.generate_title(cache_entry.repo_url),
                            status='completed',
                            created_at=cache_entry.created_at,
                            completed_at=cache_entry.created_at,
                            docs_path=cache_entry.docs_path,
                            progress="Reconstructed from cache",
                            priority=0
                        )
                        reconstructed_count += 1
                except Exception as e:
                    print(f"Failed to reconstruct job for {cache_entry.repo_url}: {e}")
            
            if reconstructed_count > 0:
                print(f"Reconstructed {reconstructed_count} job statuses from cache")
                self.save_job_statuses()
                
        except Exception as e:
            print(f"Error reconstructing jobs from cache: {e}")
    
    def save_job_statuses(self):
        """Save job statuses to disk."""
        try:
            # Ensure cache directory exists
            self.jobs_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {}
            for job_id, job in self.job_status.items():
                job_dict = {
                    'job_id': job.job_id,
                    'repo_url': job.repo_url,
                    'title': job.title,
                    'status': job.status,
                    'created_at': job.created_at.isoformat(),
                    'started_at': job.started_at.isoformat() if job.started_at else None,
                    'completed_at': job.completed_at.isoformat() if job.completed_at else None,
                    'error_message': job.error_message,
                    'progress': job.progress,
                    'docs_path': job.docs_path,
                    'main_model': job.main_model,
                    'commit_id': job.commit_id,
                    'priority': job.priority,
                    'log_path': job.log_path
                }
                if job.options:
                    job_dict['options'] = job.options.model_dump() if hasattr(job.options, 'model_dump') else {}
                data[job_id] = job_dict
            
            file_manager.save_json(data, self.jobs_file)
        except Exception as e:
            print(f"Error saving job statuses: {e}")
    
    def _worker_loop(self):
        """Main worker loop."""
        while self.running:
            try:
                if not self.processing_queue.empty():
                    job_id = self.processing_queue.get(timeout=1)
                    self._process_job(job_id)
                else:
                    time.sleep(1)
            except Exception as e:
                print(f"Worker error: {e}")
                time.sleep(1)
    
    def _process_job(self, job_id: str):
        """Process a single documentation generation job."""
        if job_id not in self.job_status:
            return
        
        job = self.job_status[job_id]
        if job.status == "stopped":
            self._clear_stop_request(job_id)
            return

        temp_repo_dir = None
        custom_args = None
        custom_unknown_args: List[str] = []
        
        try:
            # Initialize/clear per-job log file for this run
            job.log_path = str(self._job_log_path(job_id))
            with open(job.log_path, "w", encoding="utf-8") as fh:
                fh.write("")
            self._append_job_log(job, f"Job {job_id} started")

            custom_cli_args_text = ""
            if job.options and job.options.custom_cli_args:
                custom_cli_args_text = job.options.custom_cli_args.strip()
                if custom_cli_args_text:
                    try:
                        custom_args, custom_unknown_args = self._parse_custom_cli_args(custom_cli_args_text)
                        self._append_job_log(job, f"Custom CLI args: {custom_cli_args_text}")
                        if custom_unknown_args:
                            self._append_job_log(
                                job,
                                f"Ignored unsupported custom args: {' '.join(custom_unknown_args)}"
                            )
                    except Exception as e:
                        raise Exception(f"Invalid custom CLI args: {e}")

            # Update job status
            job.status = 'processing'
            job.started_at = datetime.now()
            self._set_progress(job, "Starting repository clone...")
            job.main_model = MAIN_MODEL
            self.save_job_statuses()
            self._check_stop_requested(job)
            
            # Check cache first
            use_cache = not (
                (job.options and job.options.no_cache) or
                (custom_args and getattr(custom_args, "no_cache", False))
            )
            cached_docs = self.cache_manager.get_cached_docs(job.repo_url) if use_cache else None
            if cached_docs and Path(cached_docs).exists():
                job.status = 'completed'
                job.completed_at = datetime.now()
                job.docs_path = cached_docs
                self._set_progress(job, "Documentation retrieved from cache")
                if not job.main_model:  # Only set if not already set
                    job.main_model = MAIN_MODEL
                
                # Save job status to disk
                self.save_job_statuses()
                
                print(f"Job {job_id}: Using cached documentation")
                self._append_job_log(job, f"Cache hit: {cached_docs}")
                return
            
            # Clone repository
            repo_info = GitHubRepoProcessor.get_repo_info(job.repo_url)
            # Use repo full name for temp directory (already URL-safe since job_id is URL-safe)
            temp_repo_dir = os.path.join(self.temp_dir, job_id)
            
            self._set_progress(job, f"Cloning repository {repo_info['full_name']}...")
            
            if not GitHubRepoProcessor.clone_repository(repo_info['clone_url'], temp_repo_dir, job.commit_id):
                raise Exception("Failed to clone repository")
            self._check_stop_requested(job)
            
            # Generate documentation
            self._set_progress(job, "Analyzing repository structure...")
            
            # Create config for documentation generation (using env vars)
            args = argparse.Namespace(repo_path=temp_repo_dir)
            config = Config.from_args(args)
            # Override docs_dir with job-specific directory
            default_docs_dir = os.path.join("output", "docs", f"{job_id}-docs")
            config.docs_dir = default_docs_dir
            
            # Apply generation options if provided
            if job.options:
                if job.options.output:
                    config.docs_dir = job.options.output
                if job.options.max_depth is not None:
                    config.max_depth = job.options.max_depth
                if job.options.agent_cmd:
                    config.agent_cmd = job.options.agent_cmd
                if job.options.max_tokens is not None:
                    config.max_tokens = job.options.max_tokens
                if job.options.max_token_per_module is not None:
                    config.max_token_per_module = job.options.max_token_per_module
                if job.options.max_token_per_leaf_module is not None:
                    config.max_token_per_leaf_module = job.options.max_token_per_leaf_module
                if job.options.concurrency is not None:
                    config.concurrency = max(1, job.options.concurrency)
                if job.options.include or job.options.exclude or job.options.focus or job.options.doc_type or job.options.instructions:
                    config.agent_instructions = config.agent_instructions or {}
                    if job.options.include:
                        config.agent_instructions['include_patterns'] = [
                            part.strip() for part in job.options.include.split(',') if part.strip()
                        ]
                    if job.options.exclude:
                        config.agent_instructions['exclude_patterns'] = [
                            part.strip() for part in job.options.exclude.split(',') if part.strip()
                        ]
                    if job.options.focus:
                        config.agent_instructions['focus_modules'] = [
                            part.strip() for part in job.options.focus.split(',') if part.strip()
                        ]
                    if job.options.doc_type:
                        config.agent_instructions['doc_type'] = job.options.doc_type
                    if job.options.instructions:
                        config.agent_instructions['custom_instructions'] = job.options.instructions

            # Custom CLI args override regular options where relevant.
            if custom_args:
                self._apply_custom_cli_args_to_config(config, custom_args)
            
            self._append_job_log(job, f"Effective docs output: {config.docs_dir}")
            self._set_progress(job, "Generating documentation...")
            self._check_stop_requested(job)
            
            # Generate documentation
            doc_generator = DocumentationGenerator(config, job.commit_id)
            
            # Run the async documentation generation in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                doc_task = loop.create_task(doc_generator.run())
                with self._stop_lock:
                    self._active_async_tasks[job_id] = (loop, doc_task)

                while not doc_task.done():
                    if self._is_stop_requested(job_id):
                        doc_task.cancel()
                    try:
                        loop.run_until_complete(
                            asyncio.wait_for(asyncio.shield(doc_task), timeout=0.5)
                        )
                    except asyncio.TimeoutError:
                        continue
                    except asyncio.CancelledError:
                        break

                if doc_task.cancelled() or self._is_stop_requested(job_id):
                    raise JobStoppedError("Task stopped by user")
                doc_exc = doc_task.exception()
                if doc_exc:
                    raise doc_exc
            finally:
                with self._stop_lock:
                    self._active_async_tasks.pop(job_id, None)
                loop.close()
            self._check_stop_requested(job)
            
            # Cache the results
            docs_path = os.path.abspath(config.docs_dir)
            self.cache_manager.add_to_cache(job.repo_url, docs_path)

            # Generate GitHub Pages HTML viewer (optional)
            should_generate_github_pages = (
                (job.options and job.options.github_pages) or
                (custom_args and getattr(custom_args, "github_pages", False))
            )
            if should_generate_github_pages:
                try:
                    html_generator = HTMLGenerator()
                    output_path = Path(docs_path) / "index.html"
                    html_generator.generate(
                        output_path=output_path,
                        title=job.title or GitHubRepoProcessor.generate_title(job.repo_url),
                        repository_url=job.repo_url,
                        docs_dir=Path(docs_path)
                    )
                except Exception as e:
                    print(f"Job {job_id}: Failed to generate GitHub Pages HTML: {e}")
            
            output_lang = None
            if job.options and job.options.output_lang:
                output_lang = job.options.output_lang
            if custom_args and getattr(custom_args, "output_lang", None):
                output_lang = custom_args.output_lang

            translate_concurrency = config.concurrency
            if job.options and job.options.concurrency:
                translate_concurrency = max(1, job.options.concurrency)
            if custom_args and getattr(custom_args, "concurrency", None):
                translate_concurrency = max(1, custom_args.concurrency)

            if output_lang:
                from pathlib import Path as _Path
                from codewiki.cli.adapters.translator import DocTranslator
                translator = DocTranslator(config={
                    'base_url': config.llm_base_url,
                    'api_key': config.llm_api_key,
                    'main_model': config.main_model,
                    'cluster_model': config.cluster_model,
                    'fallback_model': config.fallback_model,
                    'fallback_models': config.fallback_models,
                    'max_tokens': config.max_tokens,
                    'max_token_per_module': config.max_token_per_module,
                    'max_token_per_leaf_module': config.max_token_per_leaf_module,
                    'max_depth': config.max_depth,
                    'agent_cmd': config.agent_cmd,
                })
                def _translation_progress(current, total, filename):
                    self._set_progress(job, f"Translating ({current}/{total}): {filename}")
                    self._check_stop_requested(job)

                translator.translate_docs(
                    output_dir=_Path(docs_path),
                    lang_code=output_lang,
                    progress_callback=_translation_progress,
                    concurrency=translate_concurrency
                )
            self._check_stop_requested(job)
            
            # Update job status
            job.status = 'completed'
            job.completed_at = datetime.now()
            job.docs_path = docs_path
            self._set_progress(job, "Documentation generation completed")
            
            # Save job status to disk
            self.save_job_statuses()
            
            print(f"Job {job_id}: Documentation generated successfully")
            self._append_job_log(job, f"Job completed. Docs path: {docs_path}")
            
        except JobStoppedError as e:
            job.status = 'stopped'
            job.completed_at = datetime.now()
            job.error_message = None
            self._set_progress(job, str(e))
            print(f"Job {job_id}: Stopped by user")
            self._append_job_log(job, "Job stopped by user")
            self.save_job_statuses()

        except Exception as e:
            # Update job status with error
            job.status = 'failed'
            job.completed_at = datetime.now()
            job.error_message = traceback.format_exc()
            self._set_progress(job, f"Failed: {str(e)}")
            
            print(f"Job {job_id}: Failed with error: {e}")
            self._append_job_log(job, f"Job failed: {e}")
            self._append_job_log(job, traceback.format_exc())
            # Save job status to disk
            self.save_job_statuses()
        
        finally:
            self._clear_stop_request(job_id)
            # Cleanup temporary repository
            if temp_repo_dir and os.path.exists(temp_repo_dir):
                try:
                    subprocess.run(['rm', '-rf', temp_repo_dir], check=True)
                    self._append_job_log(job, f"Temp directory cleaned: {temp_repo_dir}")
                except Exception as e:
                    print(f"Failed to cleanup temp directory: {e}")
                    self._append_job_log(job, f"Failed to cleanup temp directory: {e}")
