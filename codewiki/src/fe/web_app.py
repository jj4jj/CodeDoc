#!/usr/bin/env python3
"""
CodeWiki Web Application

A web interface for users to submit Git repositories for documentation generation.
Features:
- Simple web form for Git repo URL input
- Background processing queue
- Cache system for generated documentation
- Job status tracking
- Admin panel for task management
"""

import argparse
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .cache_manager import CacheManager
from .background_worker import BackgroundWorker
from .routes import WebRoutes
from .config import WebAppConfig


# Initialize FastAPI app
app = FastAPI(
    title="CodeDoc", 
    description="Generate comprehensive documentation for any Git repository"
)

# Initialize components
cache_manager = CacheManager(
    cache_dir=WebAppConfig.CACHE_DIR, 
    cache_expiry_days=WebAppConfig.CACHE_EXPIRY_DAYS
)
background_worker = BackgroundWorker(
    cache_manager=cache_manager, 
    temp_dir=WebAppConfig.TEMP_DIR
)
web_routes = WebRoutes(background_worker=background_worker, cache_manager=cache_manager)


# Register routes
@app.get("/", response_class=HTMLResponse)
async def index_get(request: Request):
    """Main page with form for submitting Git repositories."""
    return await web_routes.index_get(request)


@app.post("/", response_class=HTMLResponse)
async def index_post(
    request: Request,
    repo_url: str = Form(...),
    commit_id: str = Form(""),
):
    """Handle repository submission."""
    return await web_routes.index_post(request, repo_url, commit_id)


@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str):
    """API endpoint to get job status."""
    return await web_routes.get_job_status(job_id)


@app.get("/api/tasks")
async def list_tasks(status_filter: str = None):
    """API endpoint to list all tasks."""
    return await web_routes.list_tasks(status_filter)


@app.post("/api/tasks")
async def create_task(
    repo_url: str,
    commit_id: str = "",
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
    max_tokens: str = "",
    max_token_per_module: str = "",
    max_token_per_leaf_module: str = "",
    max_depth: str = "",
    output_lang: str = "",
    agent_cmd: str = "",
    custom_cli_args: str = "",
    concurrency: int = 4,
):
    """API endpoint to create a new documentation generation task."""
    return await web_routes.create_task_api(
        repo_url,
        commit_id,
        priority,
        output,
        create_branch,
        github_pages,
        no_cache,
        include,
        exclude,
        focus,
        doc_type,
        instructions,
        max_tokens,
        max_token_per_module,
        max_token_per_leaf_module,
        max_depth,
        output_lang,
        agent_cmd,
        custom_cli_args,
        concurrency,
    )


@app.delete("/api/tasks/{job_id}")
async def delete_task(job_id: str):
    """API endpoint to delete a task."""
    return await web_routes.delete_task(job_id)


@app.post("/api/tasks/{job_id}/regenerate")
async def regenerate_task(job_id: str):
    """API endpoint to regenerate docs for an existing task."""
    return await web_routes.regenerate_task(job_id)


@app.post("/api/tasks/{job_id}/stop")
async def stop_task(job_id: str):
    """API endpoint to stop a queued/processing task."""
    return await web_routes.stop_task(job_id)


@app.get("/api/tasks/{job_id}/log")
async def get_task_log(job_id: str, tail: int = 500):
    """API endpoint to view a task's runtime log."""
    return await web_routes.get_task_log(job_id, tail)


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Admin page for managing tasks."""
    return await web_routes.admin_get(request)


@app.post("/admin", response_class=HTMLResponse)
async def admin_post(
    request: Request,
    repo_url: str = Form(...),
    commit_id: str = Form(""),
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
    max_tokens: str = Form(""),
    max_token_per_module: str = Form(""),
    max_token_per_leaf_module: str = Form(""),
    max_depth: str = Form(""),
    output_lang: str = Form(""),
    agent_cmd: str = Form(""),
    custom_cli_args: str = Form(""),
    concurrency: int = Form(4),
):
    """Handle task submission from admin page."""
    return await web_routes.admin_post(
        request,
        repo_url,
        commit_id,
        priority,
        output,
        create_branch,
        github_pages,
        no_cache,
        include,
        exclude,
        focus,
        doc_type,
        instructions,
        max_tokens,
        max_token_per_module,
        max_token_per_leaf_module,
        max_depth,
        output_lang,
        agent_cmd,
        custom_cli_args,
        concurrency,
    )


@app.get("/docs/{job_id}")
async def view_docs(job_id: str, version: str = "", lang: str = ""):
    """View generated documentation."""
    return await web_routes.view_docs(job_id, version, lang)


@app.get("/static-docs/{job_id}/")
@app.get("/static-docs/{job_id}/{filename:path}")
async def serve_generated_docs(job_id: str, filename: str = "overview.md", version: str = "", lang: str = ""):
    """Serve generated documentation files."""
    if not filename: 
        filename = "overview.md"
    return await web_routes.serve_generated_docs(job_id, filename, version, lang)


def main():
    """Main function to run the web application."""
    import uvicorn
    
    parser = argparse.ArgumentParser(
        description="CodeWiki Web Application - Generate documentation for Git repositories"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=WebAppConfig.DEFAULT_HOST,
        help=f"Host to bind the server to (default: {WebAppConfig.DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=WebAppConfig.DEFAULT_PORT,
        help=f"Port to run the server on (default: {WebAppConfig.DEFAULT_PORT})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run the server in debug mode"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    # Ensure required directories exist
    WebAppConfig.ensure_directories()
    
    # Start background worker
    background_worker.start()
    
    print(f"🚀 CodeWiki Web Application starting...")
    print(f"🌐 Server running at: http://{args.host}:{args.port}")
    print(f"📁 Cache directory: {WebAppConfig.get_absolute_path(WebAppConfig.CACHE_DIR)}")
    print(f"🗂️  Temp directory: {WebAppConfig.get_absolute_path(WebAppConfig.TEMP_DIR)}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "fe.web_app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="debug" if args.debug else "info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        background_worker.stop()


if __name__ == "__main__":
    main()
