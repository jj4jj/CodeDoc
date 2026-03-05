#!/usr/bin/env python3
"""
HTML templates for the CodeWiki web application.
"""

_SHARED_UI_TOKENS = """
        :root {
            --bg: #f3f5f8;
            --surface: #ffffff;
            --surface-soft: #eef2f7;
            --line: #d2d9e2;
            --line-strong: #bec8d4;
            --text: #162233;
            --muted: #5e6c7f;
            --primary: #2f5b87;
            --primary-strong: #244768;
            --primary-soft: #e7edf4;
            --success: #2f714f;
            --warning: #856020;
            --danger: #9a3d36;
            --shadow: 0 1px 2px rgba(22, 34, 51, 0.06);
            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 8px;
        }

        [data-theme="dark"] {
            --bg: #111823;
            --surface: #172334;
            --surface-soft: #1c2a3d;
            --line: #2b3e56;
            --line-strong: #385170;
            --text: #e6edf7;
            --muted: #9bacc4;
            --primary: #7cb0de;
            --primary-strong: #5d96c7;
            --primary-soft: #20334a;
            --success: #58b283;
            --warning: #d5a35d;
            --danger: #e0867e;
            --shadow: 0 1px 2px rgba(0, 0, 0, 0.22);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
"""

_SHARED_UI_LAYOUT = """
        body {
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.55;
        }

        .app {
            max-width: 1400px;
            margin: 0 auto;
            padding: 18px 20px 26px;
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            background: var(--surface);
            border: 1px solid var(--line);
            padding: 14px 16px;
            min-height: 72px;
            margin-bottom: 14px;
            box-shadow: var(--shadow);
        }

        .brand {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            font-size: 1.04rem;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: 0.02em;
        }

        .brand svg {
            width: 28px;
            height: 28px;
            flex: 0 0 28px;
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .nav a {
            text-decoration: none;
            color: var(--muted);
            border: 1px solid var(--line);
            background: var(--surface);
            width: 34px;
            height: 34px;
            padding: 0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.84rem;
            font-weight: 600;
            border-radius: var(--radius-sm);
        }

        .nav a svg {
            width: 16px;
            height: 16px;
        }

        .nav a.active {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .panel {
            background: var(--surface);
            border: 1px solid var(--line);
            padding: 14px;
            box-shadow: var(--shadow);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            text-decoration: none;
            cursor: pointer;
            padding: 7px 11px;
            font-size: 0.84rem;
            font-weight: 600;
            border-radius: var(--radius-sm);
            transition: 0.14s ease;
        }

        .icon-btn {
            width: 34px;
            height: 34px;
            padding: 0;
        }

        .icon-btn svg {
            width: 16px;
            height: 16px;
        }

        .theme-toggle-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        [data-theme="light"] .theme-icon-dark {
            display: none;
        }

        [data-theme="dark"] .theme-icon-light {
            display: none;
        }

        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            border: 0;
            white-space: nowrap;
        }

        .btn:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .btn-primary {
            color: #fff;
            background: var(--primary);
            border-color: var(--primary);
        }

        .btn-primary:hover {
            color: #fff;
            background: var(--primary-strong);
            border-color: var(--primary-strong);
        }

        .btn-danger {
            color: var(--danger);
            border-color: #dcb8b5;
        }

        .btn-danger:hover {
            color: var(--danger);
            background: #f9efee;
            border-color: #c79b97;
        }

        .field {
            margin-bottom: 10px;
        }

        .field label {
            display: block;
            margin-bottom: 4px;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 600;
        }

        .field input,
        .field select,
        .field textarea,
        .search {
            width: 100%;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            padding: 8px 10px;
            font-size: 0.86rem;
            border-radius: var(--radius-sm);
        }

        .field input:focus,
        .field select:focus,
        .field textarea:focus,
        .search:focus {
            outline: none;
            border-color: var(--line-strong);
        }

        .alert {
            margin-bottom: 12px;
            border: 1px solid #dfbebc;
            background: #fbf1f0;
            color: var(--danger);
            padding: 8px 10px;
            font-size: 0.87rem;
            border-radius: var(--radius-sm);
        }

        .alert-success {
            border-color: #bfdbc9;
            background: #eef8f1;
            color: var(--success);
        }

        .muted {
            color: var(--muted);
        }

        .empty {
            border: 1px dashed var(--line-strong);
            background: var(--surface-soft);
            color: var(--muted);
            text-align: center;
            padding: 24px 16px;
            font-size: 0.9rem;
            border-radius: var(--radius-sm);
        }

        @media (max-width: 940px) {
            .app {
                padding: 12px;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .topbar-right {
                width: 100%;
                justify-content: space-between;
            }
        }
"""


def _inject_shared_ui(template: str) -> str:
    """Inject shared design tokens and layout primitives into templates."""
    return (
        template
        .replace("__CW_SHARED_UI_TOKENS__", _SHARED_UI_TOKENS)
        .replace("__CW_SHARED_UI_LAYOUT__", _SHARED_UI_LAYOUT)
    )


def _inject_shared_tokens(template: str) -> str:
    """Inject only shared design tokens for standalone layouts."""
    return template.replace("__CW_SHARED_UI_TOKENS__", _SHARED_UI_TOKENS)

# Web interface HTML template
WEB_INTERFACE_TEMPLATE = _inject_shared_ui("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki 文档中心</title>
    <style>
__CW_SHARED_UI_TOKENS__
__CW_SHARED_UI_LAYOUT__
        .workspace {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 320px;
            gap: 14px;
        }

        .main-pane,
        .side-pane {
            min-width: 0;
        }

        .panel-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
        }

        .panel-head h2 {
            font-size: 1.03rem;
        }

        .panel-head span {
            color: var(--muted);
            font-size: 0.82rem;
        }

        .list-tools {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }

        .list-tools .search {
            flex: 1;
            min-width: 0;
        }

        .jobs {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            max-height: calc(100vh - 290px);
            overflow: auto;
            padding-right: 2px;
        }

        .job {
            border: 1px solid var(--line);
            background: var(--surface);
            padding: 10px;
            border-radius: var(--radius-sm);
        }

        .job-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
        }

        .job-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2px;
        }

        .job-url {
            font-size: 0.78rem;
            color: var(--muted);
            word-break: break-word;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            border: 1px solid transparent;
            border-radius: var(--radius-sm);
            padding: 2px 7px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .status-completed {
            color: var(--success);
            border-color: #bfd8c9;
            background: #ecf7f0;
        }

        .status-processing {
            color: var(--primary);
            border-color: #c6d4e5;
            background: #edf3fa;
        }

        .status-queued {
            color: var(--warning);
            border-color: #dfcfaf;
            background: #f9f4ea;
        }

        .status-failed {
            color: var(--danger);
            border-color: #dfc0bd;
            background: #fbf1f0;
        }

        .job-meta {
            margin-top: 8px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            color: var(--muted);
            font-size: 0.75rem;
        }

        .job-progress {
            margin-top: 8px;
            border-top: 1px dashed var(--line);
            padding-top: 8px;
            color: var(--muted);
            font-size: 0.79rem;
            word-break: break-word;
        }

        .job-actions {
            margin-top: 8px;
            display: flex;
            justify-content: flex-end;
        }

        .side-pane h3 {
            font-size: 0.95rem;
            margin-bottom: 10px;
        }

        .quick-note {
            margin-bottom: 10px;
            border: 1px solid var(--line);
            background: var(--surface-soft);
            padding: 8px 10px;
            font-size: 0.8rem;
            color: var(--muted);
            border-radius: var(--radius-sm);
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 12px;
        }

        .summary-card {
            border: 1px solid var(--line);
            background: var(--surface);
            padding: 8px;
            border-radius: var(--radius-sm);
        }

        .summary-value {
            font-size: 1.12rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2px;
        }

        .summary-label {
            color: var(--muted);
            font-size: 0.72rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .mini-list {
            display: grid;
            gap: 8px;
        }

        .mini-item {
            border: 1px solid var(--line);
            padding: 8px;
            border-radius: var(--radius-sm);
            background: var(--surface);
        }

        .mini-item a {
            text-decoration: none;
            color: var(--primary);
            font-weight: 600;
            font-size: 0.82rem;
        }

        .mini-item p {
            margin-top: 3px;
            color: var(--muted);
            font-size: 0.75rem;
            word-break: break-word;
        }

        @media (max-width: 1180px) {
            .jobs {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 940px) {
            .workspace {
                grid-template-columns: 1fr;
            }

            .jobs {
                max-height: none;
            }

            .panel-head {
                flex-direction: column;
                align-items: flex-start;
            }

            .job-head {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <header class="topbar">
            <a class="brand" href="/" aria-label="CodeWiki 文档中心">
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <rect x="2.5" y="3" width="8.2" height="8.2" rx="1.4" fill="#2f5b87"/>
                    <rect x="13.3" y="3" width="8.2" height="8.2" rx="1.4" fill="#6c8fb0"/>
                    <rect x="2.5" y="12.8" width="8.2" height="8.2" rx="1.4" fill="#7aa1c6"/>
                    <rect x="13.3" y="12.8" width="8.2" height="8.2" rx="1.4" fill="#244768"/>
                </svg>
                <span>CodeWiki 文档中心</span>
            </a>
            <div class="topbar-right">
                <nav class="nav">
                    <a class="active" href="/" title="首页" aria-label="首页">
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M4 10.6L12 4l8 6.6V20H4v-9.4z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                            <path d="M9.5 20v-5.4h5V20" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                        </svg>
                    </a>
                    <a href="/admin" title="控制台" aria-label="控制台">
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <rect x="3.5" y="3.5" width="17" height="17" rx="2" stroke="currentColor" stroke-width="1.8"/>
                            <path d="M8 9h8M8 12h8M8 15h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                        </svg>
                    </a>
                </nav>
                <button id="themeToggle" class="btn icon-btn" type="button" title="切换主题" aria-label="切换主题">
                    <span class="theme-toggle-icon theme-icon-light" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M12 4.2v2.1M12 17.7v2.1M4.2 12h2.1M17.7 12h2.1M6.4 6.4l1.5 1.5M16.1 16.1l1.5 1.5M17.6 6.4l-1.5 1.5M7.9 16.1l-1.5 1.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                            <circle cx="12" cy="12" r="3.7" stroke="currentColor" stroke-width="1.7"/>
                        </svg>
                    </span>
                    <span class="theme-toggle-icon theme-icon-dark" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M14.8 4.4a7.9 7.9 0 1 0 4.8 14.2 8.2 8.2 0 0 1-4.8-14.2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                        </svg>
                    </span>
                    <span class="sr-only">切换主题</span>
                </button>
            </div>
        </header>

        {% if message %}
        <div class="alert alert-{{ message_type }}">{{ message }}</div>
        {% endif %}

        <section class="workspace">
            <div class="panel main-pane">
                <div class="panel-head">
                    <h2>可访问文档</h2>
                    <span>{{ recent_jobs|length }} 项</span>
                </div>

                {% if recent_jobs %}
                <div class="list-tools">
                    <input id="jobFilter" class="search" type="text" placeholder="按仓库、任务 ID、进度搜索...">
                    <button class="btn" type="button" id="refreshBtn">刷新</button>
                </div>

                <div class="jobs" id="jobsContainer">
                    {% for job in recent_jobs %}
                    <article class="job" data-search="{{ (job.title or '') ~ ' ' ~ job.repo_url ~ ' ' ~ job.job_id ~ ' ' ~ (job.progress or '') ~ ' ' ~ ((job.options.subproject_name if job.options and job.options.subproject_name else '') ) ~ ' ' ~ ((job.options.subproject_path if job.options and job.options.subproject_path else '') ) }}">
                        <div class="job-head">
                            <div>
                                <div class="job-title">{{ job.title or job.repo_url.split('/')[-1] }}</div>
                                <div class="job-url">{{ job.repo_url }}</div>
                                {% if job.options and (job.options.subproject_name or job.options.subproject_path) %}
                                <div class="job-url">子项目: {{ job.options.subproject_name or job.options.subproject_path }}</div>
                                {% endif %}
                            </div>
                            <span class="badge status-{{ job.status }}">{{ job.status|upper }}</span>
                        </div>

                        <div class="job-meta">
                            <span>任务 ID: {{ job.job_id }}</span>
                            {% if job.commit_id %}
                            <span>Commit: {{ job.commit_id[:10] }}</span>
                            {% endif %}
                            <span>{{ (job.completed_at or job.created_at).strftime('%Y-%m-%d %H:%M') }}</span>
                        </div>

                        {% if job.progress %}
                        <div class="job-progress">{{ job.progress }}</div>
                        {% endif %}

                        <div class="job-actions">
                            <a href="/docs/{{ job.job_id }}" class="btn">查看文档</a>
                        </div>
                    </article>
                    {% endfor %}
                </div>
                {% else %}
                <div class="empty">暂无可访问文档，请先到控制台创建任务。</div>
                {% endif %}
            </div>

            <aside class="panel side-pane">
                <h3>快速浏览</h3>
                <div class="quick-note">支持按关键词快速筛选文档任务，右侧展示近期访问仓库入口。</div>

                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-value">{{ recent_jobs|length }}</div>
                        <div class="summary-label">文档总数</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value">{{ recent_jobs|selectattr("status", "equalto", "completed")|list|length }}</div>
                        <div class="summary-label">已完成</div>
                    </div>
                </div>

                <div class="mini-list">
                    {% for job in recent_jobs[:8] %}
                    <div class="mini-item">
                        <a href="/docs/{{ job.job_id }}">{{ job.title or job.repo_url.split('/')[-1] }}</a>
                        <p>{{ (job.options.subproject_name if job.options and job.options.subproject_name else (job.options.subproject_path if job.options and job.options.subproject_path else "仓库根目录")) }}</p>
                    </div>
                    {% endfor %}
                    {% if not recent_jobs %}
                    <div class="empty">暂无可展示条目</div>
                    {% endif %}
                </div>
            </aside>
        </section>
    </div>

    <script>
        const THEME_KEY = "codewiki_theme";

        function applyTheme(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            const btn = document.getElementById("themeToggle");
            if (btn) {
                const nextLabel = theme === "dark" ? "切换到浅色模式" : "切换到深色模式";
                btn.setAttribute("title", nextLabel);
                btn.setAttribute("aria-label", nextLabel);
            }
        }

        function initTheme() {
            const stored = localStorage.getItem(THEME_KEY) || "light";
            applyTheme(stored);
        }

        function toggleTheme() {
            const current = document.documentElement.getAttribute("data-theme") || "light";
            const next = current === "dark" ? "light" : "dark";
            localStorage.setItem(THEME_KEY, next);
            applyTheme(next);
        }

        document.addEventListener("DOMContentLoaded", function() {
            initTheme();

            const themeToggle = document.getElementById("themeToggle");
            if (themeToggle) {
                themeToggle.addEventListener("click", toggleTheme);
            }

            const refreshBtn = document.getElementById("refreshBtn");
            if (refreshBtn) {
                refreshBtn.addEventListener("click", function() {
                    window.location.reload();
                });
            }

            const filterInput = document.getElementById("jobFilter");
            const jobsContainer = document.getElementById("jobsContainer");
            if (filterInput && jobsContainer) {
                filterInput.addEventListener("input", function() {
                    const keyword = filterInput.value.trim().toLowerCase();
                    jobsContainer.querySelectorAll(".job").forEach(function(item) {
                        const source = (item.getAttribute("data-search") || "").toLowerCase();
                        item.style.display = source.includes(keyword) ? "" : "none";
                    });
                });
            }
        });
    </script>
</body>
</html>
""")

# HTML template for the documentation pages
DOCS_VIEW_TEMPLATE = _inject_shared_tokens("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.9.0/dist/mermaid.min.js"></script>
    <style>
__CW_SHARED_UI_TOKENS__
        :root {
            --chat-panel-width: min(1080px, 86vw);
        }

        body {
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.55;
        }

        .docs-shell {
            display: flex;
            min-height: 100vh;
        }

        .sidebar {
            width: 308px;
            background: var(--surface-soft);
            border-right: 1px solid var(--line);
            padding: 18px;
            overflow-y: auto;
            position: fixed;
            inset: 0 auto 0 0;
        }

        .content {
            flex: 1;
            margin-left: 308px;
            margin-right: 0;
            padding: 24px 28px;
            min-width: 0;
            transition: margin-right 0.22s ease;
        }

        body.chat-open .content {
            margin-right: var(--chat-panel-width);
        }

        .docs-content-frame {
            width: 100%;
            min-height: 640px;
            height: calc(100vh - 48px);
            border: 1px solid var(--line);
            background: var(--surface);
        }

        .chat-panel {
            width: var(--chat-panel-width);
            border-left: 1px solid var(--line);
            background: var(--surface);
            position: fixed;
            inset: 0 0 0 auto;
            display: flex;
            flex-direction: column;
            transform: translateX(100%);
            transition: transform 0.22s ease;
            z-index: 120;
        }

        body.chat-open .chat-panel {
            transform: translateX(0);
        }

        .chat-drawer-toggle {
            position: fixed;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            width: 44px;
            height: 44px;
            border: 1px solid var(--line-strong);
            background: var(--surface);
            color: var(--primary);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
            box-shadow: var(--shadow);
            cursor: pointer;
            z-index: 125;
            transition: right 0.22s ease, background 0.14s ease, color 0.14s ease, border-color 0.14s ease;
        }

        .chat-drawer-toggle:hover {
            background: var(--primary-soft);
            border-color: var(--primary);
        }

        .chat-drawer-toggle svg {
            width: 20px;
            height: 20px;
        }

        body.chat-open .chat-drawer-toggle {
            right: calc(var(--chat-panel-width) + 12px);
        }

        .chat-header {
            padding: 12px;
            border-bottom: 1px solid var(--line);
            background: var(--surface-soft);
        }

        .chat-header-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 6px;
        }

        .chat-title {
            font-size: 0.92rem;
            font-weight: 700;
            flex: 0 0 auto;
        }

        .chat-session-controls {
            display: flex;
            align-items: center;
            gap: 6px;
            min-width: 0;
            flex: 1 1 auto;
            justify-content: flex-end;
        }

        .chat-session-select {
            max-width: 320px;
            min-width: 180px;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            padding: 5px 7px;
            font-size: 0.76rem;
        }

        .chat-new-session {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            font-size: 0.76rem;
            padding: 5px 8px;
            cursor: pointer;
        }

        .chat-new-session:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .chat-subtitle {
            font-size: 0.74rem;
            color: var(--muted);
            line-height: 1.45;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
        }

        .chat-bubble {
            margin-bottom: 10px;
            border: 1px solid var(--line);
            background: var(--surface-soft);
            padding: 8px 9px;
            border-radius: var(--radius-sm);
            font-size: 0.8rem;
            line-height: 1.45;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .chat-bubble.user {
            background: #eaf1f8;
            border-color: #d7e2ee;
        }

        .chat-bubble.assistant {
            background: #f8fafc;
        }

        .chat-input-wrap {
            padding: 10px 12px 12px;
            border-top: 1px solid var(--line);
            background: var(--surface);
        }

        .chat-input {
            width: 100%;
            min-height: 86px;
            resize: vertical;
            border: 1px solid var(--line);
            background: #fff;
            color: var(--text);
            border-radius: var(--radius-sm);
            padding: 8px;
            font-size: 0.82rem;
            line-height: 1.45;
            margin-bottom: 8px;
        }

        .chat-actions {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }

        .chat-hint {
            font-size: 0.72rem;
            color: var(--muted);
            line-height: 1.35;
        }

        .chat-send {
            border: 1px solid var(--primary);
            background: var(--primary);
            color: #fff;
            font-weight: 600;
            font-size: 0.78rem;
            padding: 7px 12px;
            cursor: pointer;
            border-radius: var(--radius-sm);
        }

        .chat-send:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .logo {
            display: block;
            text-decoration: none;
            color: var(--primary);
            font-size: 1.95rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 10px;
        }

        .home-link {
            display: inline-flex;
            align-items: center;
            text-decoration: none;
            border: 1px solid var(--line);
            color: var(--muted);
            background: var(--surface);
            padding: 5px 9px;
            font-size: 0.78rem;
            margin-bottom: 14px;
            border-radius: var(--radius-sm);
        }

        .home-link:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .sidebar-info {
            margin-bottom: 14px;
            padding: 10px;
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--radius-sm);
        }

        .sidebar-info h4 {
            margin-bottom: 7px;
            font-size: 0.72rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .sidebar-info-row {
            font-size: 0.76rem;
            color: var(--muted);
            margin-bottom: 4px;
            line-height: 1.45;
        }

        .sidebar-info-row strong {
            color: var(--text);
            font-weight: 600;
        }

        .sidebar-control {
            margin-bottom: 12px;
        }

        .sidebar-control-label {
            display: block;
            margin-bottom: 5px;
            color: var(--muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .sidebar-control-input,
        .sidebar-control-readonly {
            width: 100%;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            padding: 8px 9px;
            font-size: 0.8rem;
            border-radius: var(--radius-sm);
        }

        .sidebar-control-readonly {
            min-height: 34px;
            display: flex;
            align-items: center;
        }

        .nav-section {
            margin-bottom: 10px;
        }

        .nav-item {
            display: block;
            text-decoration: none;
            color: var(--text);
            padding: 7px 10px;
            margin-bottom: 4px;
            border: 1px solid transparent;
            border-radius: var(--radius-sm);
            font-size: 0.86rem;
        }

        .nav-item:hover {
            color: var(--primary);
            background: var(--primary-soft);
            border-color: var(--line);
        }

        .nav-item.active {
            color: #fff;
            background: var(--primary);
            border-color: var(--primary);
        }

        .nav-subsection {
            margin-left: 12px;
        }

        .nav-subsection .nav-item {
            font-size: 0.82rem;
        }

        .nav-section-header {
            padding: 6px 10px;
            margin-bottom: 4px;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 600;
            border-left: 2px solid var(--line);
        }

        .markdown-content {
            max-width: 1200px;
        }

        .markdown-content h1 {
            font-size: 2.28rem;
            margin-bottom: 0.9rem;
            padding-bottom: 0.45rem;
            border-bottom: 1px solid var(--line);
        }

        .markdown-content h2 {
            font-size: 1.84rem;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
            color: var(--text);
        }

        .markdown-content h3 {
            font-size: 1.34rem;
            margin-top: 1.5rem;
            margin-bottom: 0.7rem;
        }

        .markdown-content p,
        .markdown-content li {
            color: var(--text);
            margin-bottom: 0.75rem;
        }

        .markdown-content ul,
        .markdown-content ol {
            padding-left: 1.35rem;
            margin-bottom: 1rem;
        }

        .markdown-content code {
            background: var(--surface-soft);
            border: 1px solid var(--line);
            padding: 0.14rem 0.38rem;
            border-radius: var(--radius-sm);
            font-family: "Courier New", Consolas, monospace;
            font-size: 0.86em;
        }

        .markdown-content pre {
            background: var(--surface);
            border: 1px solid var(--line);
            padding: 12px;
            margin-bottom: 1rem;
            overflow-x: auto;
            border-radius: var(--radius-sm);
        }

        .markdown-content pre code {
            border: none;
            background: transparent;
            padding: 0;
        }

        .markdown-content blockquote {
            margin: 1rem 0;
            padding: 0.7rem 0.95rem;
            border-left: 3px solid var(--line-strong);
            background: var(--surface-soft);
            color: var(--muted);
        }

        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            font-size: 0.88rem;
        }

        .markdown-content th,
        .markdown-content td {
            border: 1px solid var(--line);
            padding: 0.58rem 0.68rem;
            text-align: left;
            vertical-align: top;
        }

        .markdown-content th {
            background: var(--surface-soft);
            font-weight: 700;
        }

        .markdown-content a {
            color: var(--primary);
            text-decoration: underline;
            text-decoration-color: #9cb4ce;
        }

        .mermaid {
            margin: 1rem 0;
            padding: 10px;
            background: var(--surface);
            border: 1px solid var(--line);
            overflow-x: auto;
        }

        @media (max-width: 1580px) {
            :root {
                --chat-panel-width: min(920px, 84vw);
            }
        }

        @media (max-width: 1320px) {
            :root {
                --chat-panel-width: min(760px, 88vw);
            }

            .content {
                padding: 20px 20px;
            }
        }

        @media (max-width: 980px) {
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
            }

            .content {
                margin-left: 0;
                margin-right: 0;
                padding: 14px;
            }

            body.chat-open .content {
                margin-right: 0;
            }

            .docs-content-frame {
                height: 65vh;
                min-height: 400px;
            }

            .chat-panel {
                width: min(100vw, 100%);
                border-left: 1px solid var(--line);
                transform: translateX(100%);
                z-index: 130;
            }

            body.chat-open .chat-panel {
                transform: translateX(0);
            }

            .chat-messages {
                max-height: 260px;
            }

            .chat-drawer-toggle {
                top: auto;
                bottom: 14px;
                transform: none;
                right: 12px;
            }

            body.chat-open .chat-drawer-toggle {
                right: 12px;
                bottom: 14px;
            }

            .chat-header-top {
                align-items: flex-start;
                flex-direction: column;
            }

            .chat-session-controls {
                width: 100%;
                justify-content: flex-start;
            }

            .chat-session-select {
                max-width: none;
                width: 100%;
            }

            .docs-shell {
                display: block;
            }
        }
    </style>
</head>
<body>
    <div class="docs-shell">
        <nav class="sidebar">
            <a
                href="{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}/overview.md{{ query_suffix or '' }}"
                class="logo nav-link {% if current_page == 'overview.md' %}active{% endif %}"
                data-page="overview.md"
                data-shell-href="{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}/overview.md{{ query_suffix or '' }}"
                target="{% if content_frame_url %}docsContentFrame{% endif %}"
            >{{ repo_name }}</a>
            <a href="{{ docs_home_url or '/' }}" class="home-link">← 返回文档中心</a>

            {% if metadata and metadata.generation_info %}
            <div class="sidebar-info">
                <h4>Generation Info</h4>
                <div class="sidebar-info-row"><strong>Model:</strong> {{ metadata.generation_info.main_model }}</div>
                <div class="sidebar-info-row"><strong>Generated:</strong> {{ metadata.generation_info.timestamp[:16] }}</div>
                    {% if metadata.generation_info.commit_id %}
                    <div class="sidebar-info-row"><strong>Commit:</strong> {{ metadata.generation_info.commit_id[:8] }}</div>
                    {% endif %}
                    {% if metadata.statistics %}
                    <div class="sidebar-info-row"><strong>Components:</strong> {{ metadata.statistics.total_components }}</div>
                    {% endif %}
            </div>
            {% endif %}

            {% if versions and versions|length > 1 %}
            <div class="sidebar-control">
                <label for="versionSelect" class="sidebar-control-label">Version</label>
                <select id="versionSelect" class="sidebar-control-input">
                    {% for v in versions %}
                    <option value="{{ v.id }}" {% if current_version == v.id %}selected{% endif %}>{{ v.label }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endif %}

            {% if languages and languages|length > 1 %}
            <div class="sidebar-control">
                <label for="languageSelect" class="sidebar-control-label">语言</label>
                <select id="languageSelect" class="sidebar-control-input">
                    {% for lang_item in languages %}
                    <option value="{{ lang_item.id }}" {% if current_lang == lang_item.id %}selected{% endif %}>{{ lang_item.label }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endif %}

            {% if view_options and view_options|length > 1 %}
            <div class="sidebar-control">
                <label for="viewSelect" class="sidebar-control-label">视图</label>
                <select id="viewSelect" class="sidebar-control-input">
                    {% for v in view_options %}
                    <option value="{{ v.job_id }}" {% if current_view_job_id == v.job_id %}selected{% endif %}>{{ v.label }}</option>
                    {% endfor %}
                </select>
            </div>
            {% elif current_doc_type %}
            <div class="sidebar-control">
                <label class="sidebar-control-label">视图</label>
                <div class="sidebar-control-readonly">{{ current_doc_type }}</div>
            </div>
            {% endif %}

            {% if navigation and navigation|length > 0 %}
            <div class="nav-section">
                <a
                    href="{{ content_nav_base or (shell_nav_base or ('/static-docs/' ~ (job_id or ''))) }}/overview.md{{ query_suffix or '' }}"
                    class="nav-item nav-link {% if current_page == 'overview.md' %}active{% endif %}"
                    data-page="overview.md"
                    data-shell-href="{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}/overview.md{{ query_suffix or '' }}"
                    target="{% if content_frame_url %}docsContentFrame{% endif %}"
                >
                    Overview
                </a>
            </div>

            {% macro render_nav_item(key, data, depth=0) %}
                {% set indent_class = 'nav-subsection' if depth > 0 else '' %}
                {% set indent_style = 'margin-left: ' + (depth * 15)|string + 'px;' if depth > 0 else '' %}
                <div class="{{ indent_class }}" {% if indent_style %}style="{{ indent_style }}"{% endif %}>
                    {% if data.components %}
                        <a
                            href="{{ content_nav_base or (shell_nav_base or ('/static-docs/' ~ (job_id or ''))) }}/{{ key }}.md{{ query_suffix or '' }}"
                            class="nav-item nav-link {% if current_page == key + '.md' %}active{% endif %}"
                            data-page="{{ key }}.md"
                            data-shell-href="{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}/{{ key }}.md{{ query_suffix or '' }}"
                            target="{% if content_frame_url %}docsContentFrame{% endif %}"
                        >
                            {{ key.replace('_', ' ').title() }}
                        </a>
                    {% else %}
                        <div class="nav-section-header" {% if depth > 0 %}style="font-size: {{ 14 - (depth * 1) }}px; text-transform: none;"{% endif %}>
                            {{ key.replace('_', ' ').title() }}
                        </div>
                    {% endif %}

                    {% if data.children %}
                        {% for child_key, child_data in data.children.items() %}
                            {{ render_nav_item(child_key, child_data, depth + 1) }}
                        {% endfor %}
                    {% endif %}
                </div>
            {% endmacro %}

            {% for section_key, section_data in navigation.items() %}
            <div class="nav-section">
                {{ render_nav_item(section_key, section_data) }}
            </div>
            {% endfor %}
            {% elif fallback_navigation and fallback_navigation|length > 0 %}
            <div class="nav-section">
                {% for nav_item in fallback_navigation %}
                <a
                    href="{{ content_nav_base or (shell_nav_base or ('/static-docs/' ~ (job_id or ''))) }}/{{ nav_item.path }}{{ query_suffix or '' }}"
                    class="nav-item nav-link {% if current_page == nav_item.path %}active{% endif %}"
                    data-page="{{ nav_item.path }}"
                    data-shell-href="{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}/{{ nav_item.path }}{{ query_suffix or '' }}"
                    target="{% if content_frame_url %}docsContentFrame{% endif %}"
                >
                    {{ nav_item.title }}
                </a>
                {% endfor %}
            </div>
            {% else %}
            <div class="nav-section">
                <div class="nav-section-header">No navigation data</div>
            </div>
            {% endif %}
        </nav>

        <main class="content">
            {% if content_frame_url %}
            <iframe id="docsContentFrame" name="docsContentFrame" class="docs-content-frame" src="{{ content_frame_url }}"></iframe>
            {% else %}
            <div id="docsInlineContent" class="markdown-content">
                {{ content | safe }}
            </div>
            {% endif %}
        </main>

        {% if chat_api_url %}
        <button
            id="chatDrawerToggle"
            class="chat-drawer-toggle"
            type="button"
            title="打开聊天助手"
            aria-label="打开聊天助手"
            aria-expanded="false"
        >
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <rect x="5" y="3.8" width="14" height="11.8" rx="2.2" stroke="currentColor" stroke-width="1.7"/>
                <path d="M8.4 8.4h7.2M8.4 11.2h5.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                <path d="M9 16.2l-2.6 3 .6-2.9h-.8a1.2 1.2 0 0 1-1.2-1.2v-1" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </button>

        <aside class="chat-panel" data-chat-api="{{ chat_api_url }}" data-chat-protocol="{{ chat_protocol }}">
            <div class="chat-header">
                <div class="chat-header-top">
                    <div class="chat-title">CodeWikiAgent</div>
                    <div class="chat-session-controls">
                        <select id="chatSessionSelect" class="chat-session-select"></select>
                        <button id="chatNewSessionBtn" class="chat-new-session" type="button">新建会话</button>
                    </div>
                </div>
                <div class="chat-subtitle">
                    仅可读取文档与代码目录，禁止修改代码。会话会保存在本地浏览器并自动恢复。
                </div>
            </div>
            <div id="chatMessages" class="chat-messages"></div>
            <div class="chat-input-wrap">
                <textarea
                    id="chatInput"
                    class="chat-input"
                    placeholder="输入你想了解的实现细节、模块关系、调用链..."
                ></textarea>
                <div class="chat-actions">
                    <div class="chat-hint">当前文档导航不会重置 Chat。按 Ctrl/Cmd + Enter 发送。</div>
                    <button id="chatSendBtn" class="chat-send" type="button">发送</button>
                </div>
            </div>
        </aside>
        {% endif %}
    </div>

    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: "default",
            themeVariables: {
                primaryColor: "#e7edf4",
                primaryTextColor: "#162233",
                primaryBorderColor: "#d2d9e2",
                lineColor: "#5e6c7f",
                sectionBkgColor: "#eef2f7",
                altSectionBkgColor: "#ffffff",
                gridColor: "#d2d9e2",
                secondaryColor: "#eef2f7",
                tertiaryColor: "#ffffff"
            },
            flowchart: {
                htmlLabels: true,
                curve: "basis"
            },
            sequence: {
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true,
                bottomMarginAdj: 1,
                useMaxWidth: true,
                rightAngles: false,
                showSequenceNumbers: false
            }
        });

        document.addEventListener("DOMContentLoaded", function() {
            const docsFrame = document.getElementById("docsContentFrame");
            const frameMode = Boolean(docsFrame);
            const shellNavBase = "{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}";
            const contentNavBase = "{{ content_nav_base or (shell_nav_base or ('/static-docs/' ~ (job_id or ''))) }}";
            let currentPagePath = {{ (current_page or "overview.md")|tojson }};
            const navLinks = Array.from(document.querySelectorAll(".nav-link[data-page]"));

            const encodePagePath = (path) => {
                return String(path || "overview.md").split("/").map(function(segment) {
                    return encodeURIComponent(segment);
                }).join("/");
            };

            const decodePagePath = (path) => {
                const normalized = String(path || "").replace(/^\\/+/, "");
                if (!normalized) return "overview.md";
                try {
                    return normalized.split("/").map(function(segment) {
                        return decodeURIComponent(segment);
                    }).join("/");
                } catch (e) {
                    return normalized;
                }
            };

            const setActiveNav = (page) => {
                navLinks.forEach(function(link) {
                    link.classList.toggle("active", (link.dataset.page || "") === page);
                });
            };

            const buildQuery = () => {
                const params = new URLSearchParams(window.location.search);
                const versionSelect = document.getElementById("versionSelect");
                const languageSelect = document.getElementById("languageSelect");
                if (versionSelect) {
                    const version = versionSelect.value || "";
                    if (version) params.set("version", version);
                    else params.delete("version");
                }
                if (languageSelect) {
                    const lang = languageSelect.value || "";
                    if (lang) params.set("lang", lang);
                    else params.delete("lang");
                }
                const query = params.toString();
                return query ? ("?" + query) : "";
            };

            const syncFrameByCurrentPage = (pushHistory) => {
                const query = buildQuery();
                const shellHref = shellNavBase + "/" + encodePagePath(currentPagePath) + query;
                const contentHref = contentNavBase + "/" + encodePagePath(currentPagePath) + query;
                if (frameMode && docsFrame) {
                    docsFrame.src = contentHref;
                    if (pushHistory) {
                        window.history.pushState({ page: currentPagePath }, "", shellHref);
                    }
                } else {
                    window.location.href = shellHref;
                }
                setActiveNav(currentPagePath);
            };

            const resolveCurrentPageFromLocation = () => {
                const currentPath = window.location.pathname || "";
                const shellPrefix = shellNavBase + "/";
                if (currentPath === shellNavBase || currentPath === shellPrefix.slice(0, -1)) {
                    return "overview.md";
                }
                if (currentPath.startsWith(shellPrefix)) {
                    return decodePagePath(currentPath.slice(shellPrefix.length));
                }
                return currentPagePath || "overview.md";
            };

            navLinks.forEach(function(link) {
                link.addEventListener("click", function(event) {
                    if (!frameMode) return;
                    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) {
                        return;
                    }
                    event.preventDefault();
                    const page = link.dataset.page || "overview.md";
                    const shellHref = shellNavBase + "/" + encodePagePath(page) + buildQuery();
                    currentPagePath = page;
                    setActiveNav(page);
                    if (docsFrame) {
                        docsFrame.src = link.href;
                    }
                    window.history.pushState({ page: page }, "", shellHref);
                });
            });

            window.addEventListener("popstate", function() {
                if (!frameMode || !docsFrame) return;
                currentPagePath = resolveCurrentPageFromLocation();
                setActiveNav(currentPagePath);
                docsFrame.src = contentNavBase + "/" + encodePagePath(currentPagePath) + (window.location.search || "");
            });

            const versionSelect = document.getElementById("versionSelect");
            if (versionSelect) {
                versionSelect.addEventListener("change", function() {
                    syncFrameByCurrentPage(true);
                });
            }

            const languageSelect = document.getElementById("languageSelect");
            if (languageSelect) {
                languageSelect.addEventListener("change", function() {
                    syncFrameByCurrentPage(true);
                });
            }

            const viewSelect = document.getElementById("viewSelect");
            if (viewSelect) {
                viewSelect.addEventListener("change", function() {
                    const targetJobId = viewSelect.value || "{{ job_id or '' }}";
                    const params = new URLSearchParams(window.location.search);
                    params.delete("version");
                    const query = params.toString();
                    window.location.href = "/static-docs/" + targetJobId + "/overview.md" + (query ? ("?" + query) : "");
                });
            }

            setActiveNav(currentPagePath);

            if (!frameMode) {
                mermaid.init(undefined, document.querySelectorAll(".mermaid"));
            }

            const chatPanel = document.querySelector(".chat-panel");
            const chatDrawerToggle = document.getElementById("chatDrawerToggle");
            const chatMessagesEl = document.getElementById("chatMessages");
            const chatInputEl = document.getElementById("chatInput");
            const chatSendBtn = document.getElementById("chatSendBtn");
            const chatSessionSelectEl = document.getElementById("chatSessionSelect");
            const chatNewSessionBtn = document.getElementById("chatNewSessionBtn");
            const chatDrawerKey = "cw_chat_drawer_{{ job_id or 'default' }}";
            const chatStoreKey = "cw_chat_store_{{ job_id or 'default' }}";

            if (!chatPanel || !chatMessagesEl || !chatInputEl || !chatSendBtn || !chatSessionSelectEl || !chatNewSessionBtn) {
                return;
            }

            const greetingText = "你好，我是 CodeWikiAgent。你可以问我当前模块实现、调用链、关键函数逻辑。";
            const apiUrl = chatPanel.getAttribute("data-chat-api") || "";
            const protocol = chatPanel.getAttribute("data-chat-protocol") || "a2ui-0.1";
            let chatStore = { activeSessionId: "", sessions: [] };

            const setDrawerState = (isOpen) => {
                document.body.classList.toggle("chat-open", Boolean(isOpen));
                if (chatDrawerToggle) {
                    chatDrawerToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
                    chatDrawerToggle.setAttribute("title", isOpen ? "收起聊天助手" : "打开聊天助手");
                    chatDrawerToggle.setAttribute("aria-label", isOpen ? "收起聊天助手" : "打开聊天助手");
                }
                try {
                    window.localStorage.setItem(chatDrawerKey, isOpen ? "1" : "0");
                } catch (e) {
                    // ignore storage errors
                }
            };

            if (chatDrawerToggle) {
                chatDrawerToggle.addEventListener("click", function() {
                    const isOpen = document.body.classList.contains("chat-open");
                    setDrawerState(!isOpen);
                });
            }
            try {
                setDrawerState(window.localStorage.getItem(chatDrawerKey) === "1");
            } catch (e) {
                setDrawerState(false);
            }

            const nowText = () => {
                const d = new Date();
                const pad = (n) => String(n).padStart(2, "0");
                return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()) + " " + pad(d.getHours()) + ":" + pad(d.getMinutes());
            };

            const truncateText = (text, maxLen) => {
                const normalized = String(text || "").replace(/\\s+/g, " ").trim();
                if (!normalized) return "";
                if (normalized.length <= maxLen) return normalized;
                return normalized.slice(0, maxLen);
            };

            const buildSessionTitle = (createdAt, firstQuestion) => {
                const stem = truncateText(firstQuestion || "新会话", 30) || "新会话";
                return createdAt + "-" + stem;
            };

            const persistChatStore = () => {
                try {
                    window.localStorage.setItem(chatStoreKey, JSON.stringify(chatStore));
                } catch (e) {
                    // ignore storage errors
                }
            };

            const createSession = () => {
                const createdAt = nowText();
                const id = "local-" + Date.now() + "-" + Math.random().toString(16).slice(2, 10);
                return {
                    id: id,
                    serverSessionId: "",
                    createdAt: createdAt,
                    updatedAt: createdAt,
                    title: buildSessionTitle(createdAt, ""),
                    firstQuestion: "",
                    messages: [{ role: "assistant", content: greetingText }]
                };
            };

            const ensureValidStore = () => {
                if (!chatStore || !Array.isArray(chatStore.sessions)) {
                    chatStore = { activeSessionId: "", sessions: [] };
                }
                if (!chatStore.sessions.length) {
                    const initial = createSession();
                    chatStore.sessions = [initial];
                    chatStore.activeSessionId = initial.id;
                }
                if (!chatStore.activeSessionId || !chatStore.sessions.find(function(item) { return item.id === chatStore.activeSessionId; })) {
                    chatStore.activeSessionId = chatStore.sessions[0].id;
                }
            };

            const loadChatStore = () => {
                try {
                    const raw = window.localStorage.getItem(chatStoreKey);
                    if (raw) {
                        const parsed = JSON.parse(raw);
                        if (parsed && Array.isArray(parsed.sessions)) {
                            chatStore = parsed;
                        }
                    }
                } catch (e) {
                    chatStore = { activeSessionId: "", sessions: [] };
                }
                ensureValidStore();
                persistChatStore();
            };

            const getActiveSession = () => {
                return chatStore.sessions.find(function(item) { return item.id === chatStore.activeSessionId; }) || null;
            };

            const renderSessionOptions = () => {
                chatSessionSelectEl.innerHTML = "";
                chatStore.sessions.forEach(function(session) {
                    const option = document.createElement("option");
                    option.value = session.id;
                    option.textContent = session.title || buildSessionTitle(session.createdAt || nowText(), session.firstQuestion || "");
                    chatSessionSelectEl.appendChild(option);
                });
                chatSessionSelectEl.value = chatStore.activeSessionId;
            };

            const renderActiveMessages = () => {
                const session = getActiveSession();
                chatMessagesEl.innerHTML = "";
                if (!session || !Array.isArray(session.messages)) return;
                session.messages.forEach(function(msg) {
                    const bubble = document.createElement("div");
                    bubble.className = "chat-bubble " + (msg.role === "user" ? "user" : "assistant");
                    bubble.textContent = String(msg.content || "");
                    chatMessagesEl.appendChild(bubble);
                });
                chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
            };

            const activateSession = (sessionId) => {
                const target = chatStore.sessions.find(function(item) { return item.id === sessionId; });
                if (!target) return;
                chatStore.activeSessionId = target.id;
                renderSessionOptions();
                renderActiveMessages();
                persistChatStore();
            };

            const appendMessage = (role, text) => {
                const session = getActiveSession();
                if (!session) return;
                if (!Array.isArray(session.messages)) {
                    session.messages = [];
                }
                session.messages.push({ role: role, content: text || "" });
                session.updatedAt = nowText();
                if (role === "user" && !session.firstQuestion) {
                    session.firstQuestion = truncateText(text || "", 30);
                    session.title = buildSessionTitle(session.createdAt || nowText(), session.firstQuestion);
                    renderSessionOptions();
                }
                renderActiveMessages();
                persistChatStore();
            };

            loadChatStore();
            renderSessionOptions();
            renderActiveMessages();

            chatSessionSelectEl.addEventListener("change", function() {
                activateSession(chatSessionSelectEl.value || "");
            });

            chatNewSessionBtn.addEventListener("click", function() {
                const session = createSession();
                chatStore.sessions.unshift(session);
                chatStore.activeSessionId = session.id;
                renderSessionOptions();
                renderActiveMessages();
                persistChatStore();
            });

            const sendChat = async () => {
                if (!apiUrl) return;
                const session = getActiveSession();
                if (!session) return;

                const question = (chatInputEl.value || "").trim();
                if (!question) return;

                appendMessage("user", question);
                chatInputEl.value = "";
                chatSendBtn.disabled = true;

                const payload = {
                    protocol: protocol,
                    session_id: session.serverSessionId || session.id,
                    message: question,
                    messages: (session.messages || []).slice(-12),
                    current_page: currentPagePath || "overview.md",
                    version: "{{ current_version or '' }}",
                    lang: "{{ current_lang or '' }}"
                };

                try {
                    const response = await fetch(apiUrl, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    if (!response.ok) {
                        const text = await response.text();
                        throw new Error("HTTP " + response.status + ": " + text);
                    }
                    const data = await response.json();
                    const answer = (data && (data.output || (data.messages && data.messages[0] && data.messages[0].content))) || "No response";
                    if (data && data.session_id) {
                        session.serverSessionId = data.session_id;
                    }
                    appendMessage("assistant", answer);
                    persistChatStore();
                } catch (error) {
                    appendMessage("assistant", "请求失败: " + (error && error.message ? error.message : String(error)));
                } finally {
                    chatSendBtn.disabled = false;
                }
            };

            chatSendBtn.addEventListener("click", sendChat);
            chatInputEl.addEventListener("keydown", function(event) {
                if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
                    event.preventDefault();
                    sendChat();
                }
            });
        });
    </script>
</body>
</html>
""")

DOCS_CONTENT_TEMPLATE = _inject_shared_tokens("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.9.0/dist/mermaid.min.js"></script>
    <style>
__CW_SHARED_UI_TOKENS__
        body {
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background: var(--surface);
            line-height: 1.55;
            padding: 24px 30px;
        }

        .markdown-content {
            max-width: 1200px;
        }

        .markdown-content h1 {
            font-size: 2.28rem;
            margin-bottom: 0.9rem;
            padding-bottom: 0.45rem;
            border-bottom: 1px solid var(--line);
        }

        .markdown-content h2 {
            font-size: 1.84rem;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
            color: var(--text);
        }

        .markdown-content h3 {
            font-size: 1.34rem;
            margin-top: 1.5rem;
            margin-bottom: 0.7rem;
        }

        .markdown-content p,
        .markdown-content li {
            color: var(--text);
            margin-bottom: 0.75rem;
        }

        .markdown-content ul,
        .markdown-content ol {
            padding-left: 1.35rem;
            margin-bottom: 1rem;
        }

        .markdown-content code {
            background: var(--surface-soft);
            border: 1px solid var(--line);
            padding: 0.14rem 0.38rem;
            border-radius: var(--radius-sm);
            font-family: "Courier New", Consolas, monospace;
            font-size: 0.86em;
        }

        .markdown-content pre {
            background: var(--surface);
            border: 1px solid var(--line);
            padding: 12px;
            margin-bottom: 1rem;
            overflow-x: auto;
            border-radius: var(--radius-sm);
        }

        .markdown-content pre code {
            border: none;
            background: transparent;
            padding: 0;
        }

        .markdown-content blockquote {
            margin: 1rem 0;
            padding: 0.7rem 0.95rem;
            border-left: 3px solid var(--line-strong);
            background: var(--surface-soft);
            color: var(--muted);
        }

        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            font-size: 0.88rem;
            table-layout: auto;
        }

        .markdown-content th,
        .markdown-content td {
            border: 1px solid var(--line);
            padding: 0.58rem 0.68rem;
            text-align: left;
            vertical-align: top;
            word-break: break-word;
        }

        .markdown-content th {
            background: var(--surface-soft);
            font-weight: 700;
        }

        .markdown-content a {
            color: var(--primary);
            text-decoration: underline;
            text-decoration-color: #9cb4ce;
        }

        .mermaid {
            margin: 1rem 0;
            padding: 10px;
            background: var(--surface);
            border: 1px solid var(--line);
            overflow-x: auto;
        }

        @media (max-width: 980px) {
            body {
                padding: 16px;
            }
        }
    </style>
</head>
<body>
    <main class="markdown-content">
        {{ content | safe }}
    </main>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: "default",
            themeVariables: {
                primaryColor: "#e7edf4",
                primaryTextColor: "#162233",
                primaryBorderColor: "#d2d9e2",
                lineColor: "#5e6c7f",
                sectionBkgColor: "#eef2f7",
                altSectionBkgColor: "#ffffff",
                gridColor: "#d2d9e2",
                secondaryColor: "#eef2f7",
                tertiaryColor: "#ffffff"
            },
            flowchart: {
                htmlLabels: true,
                curve: "basis"
            }
        });
        document.addEventListener("DOMContentLoaded", function() {
            mermaid.init(undefined, document.querySelectorAll(".mermaid"));
        });
    </script>
</body>
</html>
""")

ADMIN_TEMPLATE = _inject_shared_ui("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki 控制台</title>
    <style>
__CW_SHARED_UI_TOKENS__
__CW_SHARED_UI_LAYOUT__
        .app {
            max-width: 1460px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }

        .admin-workspace {
            display: grid;
            grid-template-columns: 220px minmax(0, 1fr);
            gap: 12px;
            align-items: stretch;
            flex: 1;
            min-height: 0;
        }

        .admin-sidenav {
            padding: 8px;
            height: 100%;
            min-height: 0;
            overflow: auto;
            margin-bottom: 0;
        }

        .admin-sidenav-head {
            font-size: 0.78rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
            margin-bottom: 8px;
            padding: 6px 6px 4px;
        }

        .admin-nav-btn {
            width: 100%;
            border: 1px solid transparent;
            background: transparent;
            color: var(--text);
            text-align: left;
            padding: 8px 10px;
            font-size: 0.84rem;
            font-weight: 600;
            border-radius: var(--radius-sm);
            cursor: pointer;
            margin-bottom: 6px;
        }

        .admin-nav-btn:hover {
            color: var(--primary);
            border-color: var(--line);
            background: var(--surface-soft);
        }

        .admin-nav-btn.active {
            color: #fff;
            border-color: var(--primary);
            background: var(--primary);
        }

        .admin-content {
            min-width: 0;
            height: 100%;
            min-height: 0;
            display: flex;
            flex-direction: column;
        }

        .admin-panel {
            display: none;
            margin-bottom: 0;
            height: 100%;
            min-height: 0;
            overflow: auto;
        }

        .admin-panel.active {
            display: block;
        }

        .stat {
            border: 1px solid var(--line);
            background: var(--surface);
            padding: 10px;
            border-radius: var(--radius-sm);
        }

        .stat .value {
            font-size: 1.28rem;
            font-weight: 700;
            margin-bottom: 2px;
        }

        .stat .label {
            color: var(--muted);
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .stat.queued .value { color: var(--warning); }
        .stat.processing .value { color: var(--primary); }
        .stat.completed .value { color: var(--success); }
        .stat.failed .value { color: var(--danger); }

        .panel {
            margin-bottom: 12px;
        }

        .panel h2 {
            font-size: 1.06rem;
            margin-bottom: 10px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 220px 140px;
            gap: 10px;
        }

        .actions-row {
            display: flex;
            justify-content: flex-end;
            gap: 8px;
        }

        .options-details {
            margin-bottom: 10px;
            border: 1px solid var(--line);
            background: var(--surface);
            padding: 6px;
            border-radius: var(--radius-sm);
        }

        .options-details summary {
            cursor: pointer;
            color: var(--muted);
            font-weight: 600;
            list-style: none;
            padding: 6px 8px;
        }

        .options-details summary::-webkit-details-marker { display: none; }
        .options-details summary::before { content: "+ "; }
        .options-details[open] summary::before { content: "- "; }

        .options-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            padding: 8px;
        }

        .check-field {
            display: flex;
            align-items: center;
            gap: 8px;
            padding-top: 24px;
        }

        .check-field input[type="checkbox"] {
            width: 16px;
            height: 16px;
        }

        .check-field label {
            font-size: 0.84rem;
            color: var(--muted);
        }

        .task-toolbar {
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
        }

        .task-toolbar input,
        .task-toolbar select {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            padding: 8px 10px;
            font-size: 0.84rem;
            border-radius: var(--radius-sm);
        }

        .task-toolbar input {
            flex: 1;
            min-width: 0;
        }

        .table-wrap {
            overflow: auto;
            border: 1px solid var(--line);
            border-radius: var(--radius-sm);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 920px;
            font-size: 0.84rem;
        }

        th,
        td {
            border-bottom: 1px solid var(--line);
            text-align: left;
            padding: 9px 10px;
            vertical-align: top;
        }

        th {
            color: var(--muted);
            background: var(--surface-soft);
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
        }

        tr:last-child td {
            border-bottom: none;
        }

        .task-title {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2px;
        }

        .task-url {
            color: var(--muted);
            font-size: 0.75rem;
            word-break: break-word;
        }

        .status {
            display: inline-flex;
            align-items: center;
            padding: 2px 7px;
            border-radius: var(--radius-sm);
            border: 1px solid transparent;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .status.queued { color: var(--warning); border-color: #d8c7a4; background: #f9f3e8; }
        .status.processing { color: var(--primary); border-color: #c4d3e4; background: #ecf3fb; }
        .status.completed { color: var(--success); border-color: #bfd8c8; background: #ebf7ef; }
        .status.failed { color: var(--danger); border-color: #dfbebb; background: #fbf1f0; }
        .status.stopped { color: var(--muted); border-color: #c9d2dd; background: #f0f3f7; }

        .task-progress {
            color: var(--muted);
            word-break: break-word;
        }

        .task-actions {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        details.error {
            margin-top: 6px;
        }

        details.error summary {
            cursor: pointer;
            color: var(--danger);
            font-weight: 600;
            font-size: 0.8rem;
        }

        details.error pre {
            margin-top: 6px;
            border: 1px solid #e4c5c2;
            background: #fbf1f0;
            color: var(--danger);
            padding: 8px;
            font-size: 0.76rem;
            line-height: 1.4;
            white-space: pre-wrap;
            border-radius: var(--radius-sm);
        }

        .log-modal {
            position: fixed;
            inset: 0;
            background: rgba(16, 25, 38, 0.42);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 20px;
        }

        .log-modal.show {
            display: flex;
        }

        .log-panel {
            width: min(1020px, 100%);
            max-height: 82vh;
            background: var(--surface);
            border: 1px solid var(--line);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border-radius: var(--radius-md);
        }

        .log-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--line);
            padding: 10px 12px;
        }

        .log-head strong {
            color: var(--primary);
            font-size: 0.9rem;
        }

        .log-body {
            background: var(--surface-soft);
            padding: 10px 12px;
            overflow: auto;
        }

        .log-body pre {
            margin: 0;
            color: var(--text);
            font-size: 0.78rem;
            line-height: 1.46;
            white-space: pre-wrap;
            word-break: break-word;
        }

        @media (max-width: 1160px) {
            .stats {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .options-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 940px) {
            .app {
                min-height: auto;
            }

            .admin-workspace {
                grid-template-columns: 1fr;
                flex: none;
                min-height: auto;
            }

            .admin-sidenav {
                position: static;
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                padding: 10px;
                height: auto;
                overflow: visible;
            }

            .admin-sidenav-head {
                width: 100%;
                margin-bottom: 2px;
            }

            .admin-nav-btn {
                width: auto;
                min-width: 110px;
                margin-bottom: 0;
            }

            .admin-content {
                height: auto;
            }

            .admin-panel {
                height: auto;
                overflow: visible;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .options-grid {
                grid-template-columns: 1fr;
            }

            .stats {
                grid-template-columns: 1fr;
            }

            .task-toolbar {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="app">
        <header class="topbar">
            <a class="brand" href="/" aria-label="CodeWiki 文档中心">
                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <rect x="2.5" y="3" width="8.2" height="8.2" rx="1.4" fill="#2f5b87"/>
                    <rect x="13.3" y="3" width="8.2" height="8.2" rx="1.4" fill="#6c8fb0"/>
                    <rect x="2.5" y="12.8" width="8.2" height="8.2" rx="1.4" fill="#7aa1c6"/>
                    <rect x="13.3" y="12.8" width="8.2" height="8.2" rx="1.4" fill="#244768"/>
                </svg>
                <span>CodeWiki 文档中心</span>
            </a>
            <div class="topbar-right">
                <nav class="nav">
                    <a href="/" title="首页" aria-label="首页">
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M4 10.6L12 4l8 6.6V20H4v-9.4z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                            <path d="M9.5 20v-5.4h5V20" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                        </svg>
                    </a>
                    <a class="active" href="/admin" title="控制台" aria-label="控制台">
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <rect x="3.5" y="3.5" width="17" height="17" rx="2" stroke="currentColor" stroke-width="1.8"/>
                            <path d="M8 9h8M8 12h8M8 15h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                        </svg>
                    </a>
                    <a href="/api/tasks" target="_blank" title="任务 API" aria-label="任务 API">
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M8.4 7.5h7.2M8.4 12h7.2M8.4 16.5h4.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                            <path d="M5.5 3.8h13a1.7 1.7 0 0 1 1.7 1.7v13a1.7 1.7 0 0 1-1.7 1.7h-13a1.7 1.7 0 0 1-1.7-1.7v-13a1.7 1.7 0 0 1 1.7-1.7z" stroke="currentColor" stroke-width="1.8"/>
                        </svg>
                    </a>
                </nav>
                <button id="themeToggle" class="btn icon-btn" type="button" title="切换主题" aria-label="切换主题">
                    <span class="theme-toggle-icon theme-icon-light" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M12 4.2v2.1M12 17.7v2.1M4.2 12h2.1M17.7 12h2.1M6.4 6.4l1.5 1.5M16.1 16.1l1.5 1.5M17.6 6.4l-1.5 1.5M7.9 16.1l-1.5 1.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                            <circle cx="12" cy="12" r="3.7" stroke="currentColor" stroke-width="1.7"/>
                        </svg>
                    </span>
                    <span class="theme-toggle-icon theme-icon-dark" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M14.8 4.4a7.9 7.9 0 1 0 4.8 14.2 8.2 8.2 0 0 1-4.8-14.2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                        </svg>
                    </span>
                    <span class="sr-only">切换主题</span>
                </button>
            </div>
        </header>

        {% if error %}
        <div class="alert">{{ error }}</div>
        {% endif %}
        {% if message %}
        <div class="alert {% if message_type == 'success' %}alert-success{% endif %}">{{ message }}</div>
        {% endif %}

        <section class="admin-workspace">
            <aside class="panel admin-sidenav">
                <div class="admin-sidenav-head">控制台导航</div>
                <button type="button" class="admin-nav-btn active" data-admin-panel="panel-create">创建新任务</button>
                <button type="button" class="admin-nav-btn" data-admin-panel="panel-stats">任务概览</button>
                <button type="button" class="admin-nav-btn" data-admin-panel="panel-doc-types">文档类型模板</button>
                <button type="button" class="admin-nav-btn" data-admin-panel="panel-tasks">全部任务 ({{ total_count }})</button>
            </aside>

            <div class="admin-content">
        <section class="panel admin-panel active" id="panel-create">
            <h2>创建新任务</h2>

            <form method="POST" action="/admin">
                <div class="form-grid">
                    <div class="field">
                        <label for="repo_url">仓库地址</label>
                        <input type="url" id="repo_url" name="repo_url" required placeholder="https://github.com/owner/repository">
                    </div>
                    <div class="field">
                        <label for="subproject_path">子项目目录</label>
                        <input type="text" id="subproject_path" name="subproject_path" placeholder="例如: services/auth (空表示仓库根目录)">
                        <small style="display:block; margin-top:6px; color:var(--muted);">同一仓库可反复提交不同子项目目录，形成多个独立文档任务。</small>
                    </div>
                    <div class="field">
                        <label for="subproject_name">子项目名称</label>
                        <input type="text" id="subproject_name" name="subproject_name" placeholder="例如: auth-service (可选)">
                    </div>
                    <div class="field">
                        <label for="commit_id">Commit ID</label>
                        <input type="text" id="commit_id" name="commit_id" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="priority">优先级</label>
                        <select id="priority" name="priority">
                            <option value="0">普通</option>
                            <option value="1">高</option>
                            <option value="2">紧急</option>
                        </select>
                    </div>
                </div>

                <details class="options-details">
                    <summary>高级选项</summary>
                    <div class="options-grid">
                        <div class="field">
                            <label for="agent_cmd">Agent 命令</label>
                            <input type="text" id="agent_cmd" name="agent_cmd" placeholder="claude -p 或 opencode">
                        </div>

                        <div class="field">
                            <label for="output">输出目录</label>
                            <input type="text" id="output" name="output" placeholder="docs/codewiki">
                        </div>

                        <div class="field">
                            <label for="max_depth">最大深度</label>
                            <input type="number" id="max_depth" name="max_depth" min="1" max="10" placeholder="可选">
                        </div>

                        <div class="field">
                            <label for="concurrency">并发数</label>
                            <input type="number" id="concurrency" name="concurrency" value="4" min="1" max="16">
                        </div>

                        <div class="field">
                            <label for="output_lang">输出语言</label>
                            <input type="text" id="output_lang" name="output_lang" placeholder="zh, ja, en">
                        </div>

                        <div class="field">
                            <label for="max_tokens">最大 Tokens</label>
                            <input type="number" id="max_tokens" name="max_tokens" placeholder="响应 token 上限">
                        </div>

                        <div class="field">
                            <label for="max_token_per_module">每模块最大 Tokens</label>
                            <input type="number" id="max_token_per_module" name="max_token_per_module" placeholder="每模块 token 上限">
                        </div>

                        <div class="field">
                            <label for="max_token_per_leaf_module">叶子模块最大 Tokens</label>
                            <input type="number" id="max_token_per_leaf_module" name="max_token_per_leaf_module" placeholder="叶子模块 token 上限">
                        </div>

                        <div class="field">
                            <label for="include">包含模式</label>
                            <input type="text" id="include" name="include" placeholder="*.py,*.js">
                        </div>

                        <div class="field">
                            <label for="exclude">排除模式</label>
                            <input type="text" id="exclude" name="exclude" placeholder="*test*,*node_modules*">
                        </div>

                        <div class="field">
                            <label for="focus">聚焦路径</label>
                            <input type="text" id="focus" name="focus" placeholder="src/core,src/api">
                        </div>

                        <div class="field">
                            <label for="doc_type">文档类型</label>
                            <select id="doc_type" name="doc_type">
                                <option value="">默认（不指定）</option>
                                {% for item in doc_type_options %}
                                <option value="{{ item.name }}">
                                    {{ item.name }}{% if item.display_name %} - {{ item.display_name }}{% endif %}
                                </option>
                                {% endfor %}
                            </select>
                            <small style="display:block; margin-top:6px; color:var(--muted);">
                                文档类型可通过 API `/api/doc-types` 在后台管理（新增/覆盖模板指令与参数）。
                            </small>
                        </div>

                        <div class="field">
                            <label for="custom_cli_args">自定义命令参数</label>
                            <input type="text" id="custom_cli_args" name="custom_cli_args" placeholder="例如: -v --index-page --max-depth 5">
                            <small style="display:block; margin-top:6px; color:var(--muted);">填写后会追加到 `codewiki generate` 命令参数末尾。</small>
                        </div>

                        <div class="check-field">
                            <input type="checkbox" id="github_pages" name="github_pages" value="true">
                            <label for="github_pages">生成 GitHub Pages (index.html)</label>
                        </div>

                        <div class="check-field">
                            <input type="checkbox" id="no_cache" name="no_cache" value="true">
                            <label for="no_cache">忽略缓存并强制重建</label>
                        </div>

                        <div class="check-field">
                            <input type="checkbox" id="create_branch" name="create_branch" value="true">
                            <label for="create_branch">创建 Git 分支</label>
                        </div>
                    </div>
                </details>

                <div class="actions-row">
                    <button type="submit" class="btn btn-primary">提交任务</button>
                </div>
            </form>
        </section>

        <section class="panel admin-panel" id="panel-stats">
            <h2>任务概览</h2>
            <p style="margin-bottom:10px;color:var(--muted);font-size:13px;">
                任务并行执行: {{ task_concurrency }} / {{ task_concurrency_max }}（可通过启动参数 `--task-concurrency` 配置）
            </p>
            <div class="stats">
                <article class="stat queued">
                    <div class="value" id="statQueued">{{ queued_count }}</div>
                    <div class="label">Queued</div>
                </article>
                <article class="stat processing">
                    <div class="value" id="statProcessing">{{ processing_count }}</div>
                    <div class="label">Processing</div>
                </article>
                <article class="stat completed">
                    <div class="value" id="statCompleted">{{ completed_count }}</div>
                    <div class="label">Completed</div>
                </article>
                <article class="stat failed">
                    <div class="value" id="statFailed">{{ failed_count }}</div>
                    <div class="label">Failed</div>
                </article>
            </div>
        </section>

        <section class="panel admin-panel" id="panel-doc-types">
            <h2>文档类型模板管理</h2>
            <p style="color:var(--muted);font-size:0.86rem;margin-bottom:10px;">
                用于定义 `doc_type` 对应的默认提示词与参数模板。任务里选择该类型后会自动套用。
            </p>

            <form method="POST" action="/admin/doc-types">
                <div class="options-grid">
                    <div class="field">
                        <label for="profile_doc_type">文档类型 Key</label>
                        <input id="profile_doc_type" name="doc_type" type="text" required placeholder="例如: architecture">
                    </div>
                    <div class="field">
                        <label for="profile_display_name">显示名</label>
                        <input id="profile_display_name" name="display_name" type="text" placeholder="例如: Architecture Documentation">
                    </div>
                    <div class="field">
                        <label for="profile_description">说明</label>
                        <input id="profile_description" name="description" type="text" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="profile_prompt">模板指令（Prompt）</label>
                        <textarea id="profile_prompt" name="prompt" rows="4" placeholder="Focus on architecture documentation: ..."></textarea>
                    </div>
                    <div class="field">
                        <label for="profile_include">include_patterns</label>
                        <input id="profile_include" name="include" type="text" placeholder="*.go,*.proto">
                    </div>
                    <div class="field">
                        <label for="profile_exclude">exclude_patterns</label>
                        <input id="profile_exclude" name="exclude" type="text" placeholder="*test*,vendor/*">
                    </div>
                    <div class="field">
                        <label for="profile_focus">focus_modules</label>
                        <input id="profile_focus" name="focus" type="text" placeholder="services/auth,libs/common">
                    </div>
                    <div class="field">
                        <label for="profile_skills">skills</label>
                        <input id="profile_skills" name="skills" type="text" placeholder="mermaid-validator">
                    </div>
                    <div class="field">
                        <label for="profile_max_tokens">max_tokens</label>
                        <input id="profile_max_tokens" name="max_tokens" type="number" min="1" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="profile_max_token_per_module">max_token_per_module</label>
                        <input id="profile_max_token_per_module" name="max_token_per_module" type="number" min="1" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="profile_max_token_per_leaf_module">max_token_per_leaf_module</label>
                        <input id="profile_max_token_per_leaf_module" name="max_token_per_leaf_module" type="number" min="1" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="profile_max_depth">max_depth</label>
                        <input id="profile_max_depth" name="max_depth" type="number" min="1" max="10" placeholder="可选">
                    </div>
                    <div class="field">
                        <label for="profile_concurrency">concurrency</label>
                        <input id="profile_concurrency" name="profile_concurrency" type="number" min="1" max="64" placeholder="可选">
                    </div>
                </div>
                <div class="actions-row">
                    <button type="submit" class="btn btn-primary">保存/更新模板</button>
                </div>
            </form>

            <form method="POST" action="/admin/doc-types/delete" style="margin-top:10px;">
                <div class="form-grid">
                    <div class="field">
                        <label for="delete_doc_type">删除自定义模板（仅删除 override）</label>
                        <input id="delete_doc_type" name="doc_type" type="text" required placeholder="输入 doc_type key">
                    </div>
                </div>
                <div class="actions-row">
                    <button type="submit" class="btn btn-danger">删除模板</button>
                </div>
            </form>

            <details class="options-details" style="margin-top:10px;">
                <summary>当前模板列表 ({{ doc_type_options|length }})</summary>
                <div style="margin-top:10px;display:grid;gap:8px;">
                    {% for item in doc_type_options %}
                    <div style="padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--surface-soft);">
                        <strong>{{ item.name }}</strong>
                        {% if item.display_name %} · {{ item.display_name }}{% endif %}
                        {% if item.built_in %}<span style="color:var(--muted);font-size:12px;">(built-in)</span>{% endif %}
                        {% if item.description %}
                        <div style="margin-top:4px;color:var(--muted);font-size:12px;">{{ item.description }}</div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </details>
        </section>

        <section class="panel admin-panel" id="panel-tasks">
            <h2>全部任务 ({{ total_count }})</h2>

            {% if jobs %}
            <div class="task-toolbar">
                <input id="taskSearch" type="text" placeholder="按标题、URL、进度、任务 ID 搜索...">
                <select id="taskStatusFilter">
                    <option value="all">全部状态</option>
                    <option value="queued">Queued</option>
                    <option value="processing">Processing</option>
                    <option value="completed">Completed</option>
                    <option value="failed">Failed</option>
                    <option value="stopped">Stopped</option>
                </select>
                <button class="btn" type="button" id="adminRefresh">刷新</button>
            </div>

            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>任务</th>
                            <th>状态</th>
                            <th>进度</th>
                            <th>创建时间</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="tasksBody">
                        {% for job in jobs %}
                        <tr
                            data-job-id="{{ job.job_id }}"
                            data-status="{{ job.status }}"
                            data-search="{{ (job.title or '') ~ ' ' ~ job.repo_url ~ ' ' ~ job.job_id ~ ' ' ~ (job.progress or '') ~ ' ' ~ ((job.options.subproject_name if job.options and job.options.subproject_name else '') ) ~ ' ' ~ ((job.options.subproject_path if job.options and job.options.subproject_path else '') ) }}"
                            data-repo-url="{{ job.repo_url }}"
                            data-commit-id="{{ job.commit_id or '' }}"
                            data-priority="{{ job.priority }}"
                            data-subproject-name="{{ job.options.subproject_name if job.options and job.options.subproject_name else '' }}"
                            data-subproject-path="{{ job.options.subproject_path if job.options and job.options.subproject_path else '' }}"
                            data-output="{{ job.options.output if job.options and job.options.output else 'docs/codewiki' }}"
                            data-create-branch="{{ 'true' if job.options and job.options.create_branch else 'false' }}"
                            data-github-pages="{{ 'true' if job.options and job.options.github_pages else 'false' }}"
                            data-no-cache="{{ 'true' if job.options and job.options.no_cache else 'false' }}"
                            data-include="{{ job.options.include if job.options and job.options.include else '' }}"
                            data-exclude="{{ job.options.exclude if job.options and job.options.exclude else '' }}"
                            data-focus="{{ job.options.focus if job.options and job.options.focus else '' }}"
                            data-doc-type="{{ job.options.doc_type if job.options and job.options.doc_type else '' }}"
                            data-instructions="{{ job.options.instructions if job.options and job.options.instructions else '' }}"
                            data-skills="{{ job.options.skills if job.options and job.options.skills else '' }}"
                            data-max-tokens="{{ job.options.max_tokens if job.options and job.options.max_tokens is not none else '' }}"
                            data-max-token-per-module="{{ job.options.max_token_per_module if job.options and job.options.max_token_per_module is not none else '' }}"
                            data-max-token-per-leaf-module="{{ job.options.max_token_per_leaf_module if job.options and job.options.max_token_per_leaf_module is not none else '' }}"
                            data-max-depth="{{ job.options.max_depth if job.options and job.options.max_depth is not none else '' }}"
                            data-output-lang="{{ job.options.output_lang if job.options and job.options.output_lang else '' }}"
                            data-agent-cmd="{{ job.options.agent_cmd if job.options and job.options.agent_cmd else '' }}"
                            data-custom-cli-args="{{ job.options.custom_cli_args if job.options and job.options.custom_cli_args else '' }}"
                            data-concurrency="{{ job.options.concurrency if job.options and job.options.concurrency is not none else 4 }}"
                        >
                            <td>
                                <div class="task-title">{{ job.title or job.repo_url }}</div>
                                <div class="task-url">{{ job.repo_url }}</div>
                                {% if job.options and (job.options.subproject_name or job.options.subproject_path) %}
                                <div class="task-url">子项目: {{ job.options.subproject_name or job.options.subproject_path }}</div>
                                {% endif %}
                            </td>
                            <td>
                                <span class="status {{ job.status }}">{{ job.status }}</span>
                            </td>
                            <td>
                                <div class="task-progress">{{ job.progress }}</div>
                                {% if job.status == 'failed' and job.error_message %}
                                <details class="error">
                                    <summary>查看错误</summary>
                                    <pre>{{ job.error_message }}</pre>
                                </details>
                                {% endif %}
                            </td>
                            <td>{{ job.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                            <td>
                                <div class="task-actions">
                                    {% if job.status == 'completed' %}
                                    <a href="/docs/{{ job.job_id }}" class="btn" title="查看文档">查看</a>
                                    {% endif %}
                                    {% if job.status == 'processing' %}
                                    <button class="btn" onclick="openTaskLog('{{ job.job_id }}', true)" title="查看实时日志">日志</button>
                                    <button class="btn btn-danger" onclick="stopTask('{{ job.job_id }}')" title="停止任务">停止</button>
                                    {% endif %}
                                    {% if job.status == 'queued' %}
                                    <button class="btn btn-danger" onclick="stopTask('{{ job.job_id }}')" title="停止任务">停止</button>
                                    {% endif %}
                                    {% if job.status in ['completed', 'failed', 'stopped'] %}
                                    <button class="btn" onclick="openTaskLog('{{ job.job_id }}', false)" title="查看日志">日志</button>
                                    <button class="btn" onclick="regenerateTask('{{ job.job_id }}')" title="载入原参数到创建任务">重新生成</button>
                                    {% endif %}
                                    {% if job.status != 'processing' %}
                                    <button class="btn btn-danger" onclick="deleteTask('{{ job.job_id }}')" title="删除">删除</button>
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty">暂无任务，请先创建。</div>
            {% endif %}
        </section>
            </div>
        </section>

        <div id="logModal" class="log-modal">
            <div class="log-panel">
                <div class="log-head">
                    <strong id="logTitle">任务日志</strong>
                    <div style="display:flex; gap:8px;">
                        <button class="btn" type="button" id="logRefreshBtn">刷新</button>
                        <button class="btn" type="button" id="logCloseBtn">关闭</button>
                    </div>
                </div>
                <div class="log-body">
                    <pre id="logContent">暂无日志</pre>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ADVANCED_STORAGE_KEY = "codewiki_admin_advanced_options";
        const ADMIN_PANEL_STORAGE_KEY = "codewiki_admin_active_panel";
        const THEME_KEY = "codewiki_theme";
        let currentLogJobId = "";
        let logAutoRefreshTimer = null;
        let logAutoRefreshEnabled = false;

        function applyTheme(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            const btn = document.getElementById("themeToggle");
            if (btn) {
                const nextLabel = theme === "dark" ? "切换到浅色模式" : "切换到深色模式";
                btn.setAttribute("title", nextLabel);
                btn.setAttribute("aria-label", nextLabel);
            }
        }

        function initTheme() {
            const stored = localStorage.getItem(THEME_KEY) || "light";
            applyTheme(stored);
        }

        function toggleTheme() {
            const current = document.documentElement.getAttribute("data-theme") || "light";
            const next = current === "dark" ? "light" : "dark";
            localStorage.setItem(THEME_KEY, next);
            applyTheme(next);
        }

        function loadAdvancedOptions() {
            try {
                const raw = localStorage.getItem(ADVANCED_STORAGE_KEY);
                if (!raw) return;
                const data = JSON.parse(raw);
                for (const [name, value] of Object.entries(data)) {
                    const el = document.querySelector(`[name="${name}"]`);
                    if (!el) continue;
                    if (el.type === "checkbox") {
                        el.checked = Boolean(value);
                    } else {
                        el.value = value;
                    }
                }
            } catch (err) {
                console.warn("Failed to load advanced options", err);
            }
        }

        function saveAdvancedOptions() {
            const form = document.querySelector('form[action="/admin"]');
            if (!form) return;
            const data = {};
            form.querySelectorAll("input, select, textarea").forEach((el) => {
                if (!el.name) return;
                if (el.type === "checkbox") {
                    data[el.name] = el.checked;
                } else {
                    data[el.name] = el.value;
                }
            });
            try {
                localStorage.setItem(ADVANCED_STORAGE_KEY, JSON.stringify(data));
            } catch (err) {
                console.warn("Failed to save advanced options", err);
            }
        }

        function wireAdvancedOptionsPersistence() {
            const form = document.querySelector('form[action="/admin"]');
            if (!form) return;
            form.addEventListener("input", (e) => {
                if (e.target && e.target.name) saveAdvancedOptions();
            });
            form.addEventListener("change", (e) => {
                if (e.target && e.target.name) saveAdvancedOptions();
            });
        }

        function wireAdminPanels() {
            const navButtons = Array.from(document.querySelectorAll(".admin-nav-btn[data-admin-panel]"));
            const panels = Array.from(document.querySelectorAll(".admin-panel[id]"));
            if (!navButtons.length || !panels.length) return;

            const panelIds = new Set(panels.map((panel) => panel.id));

            const setActivePanel = (panelId, options = {}) => {
                const { persist = true, updateHash = true } = options;
                const targetId = panelIds.has(panelId) ? panelId : panels[0].id;

                panels.forEach((panel) => {
                    panel.classList.toggle("active", panel.id === targetId);
                });
                navButtons.forEach((button) => {
                    button.classList.toggle("active", button.dataset.adminPanel === targetId);
                });

                if (persist) {
                    localStorage.setItem(ADMIN_PANEL_STORAGE_KEY, targetId);
                }

                if (updateHash) {
                    const hashValue = targetId.startsWith("panel-") ? targetId.slice(6) : targetId;
                    history.replaceState(null, "", `#${hashValue}`);
                }
            };

            let initialPanelId = "";
            const hash = window.location.hash.replace("#", "").trim();
            if (hash) {
                if (panelIds.has(hash)) {
                    initialPanelId = hash;
                } else {
                    const prefixed = `panel-${hash}`;
                    if (panelIds.has(prefixed)) {
                        initialPanelId = prefixed;
                    }
                }
            }
            if (!initialPanelId) {
                const saved = localStorage.getItem(ADMIN_PANEL_STORAGE_KEY) || "";
                if (panelIds.has(saved)) {
                    initialPanelId = saved;
                }
            }

            setActivePanel(initialPanelId || "panel-create", { persist: false, updateHash: Boolean(hash) });
            window.setAdminPanel = (panelId) => setActivePanel(panelId, { persist: true, updateHash: true });

            navButtons.forEach((button) => {
                button.addEventListener("click", () => {
                    const panelId = button.dataset.adminPanel || "";
                    setActivePanel(panelId);
                });
            });

            window.addEventListener("hashchange", () => {
                const nextHash = window.location.hash.replace("#", "").trim();
                const nextId = panelIds.has(nextHash) ? nextHash : `panel-${nextHash}`;
                if (panelIds.has(nextId)) {
                    setActivePanel(nextId, { persist: true, updateHash: false });
                }
            });
        }

        function wireTaskFilters() {
            const search = document.getElementById("taskSearch");
            const status = document.getElementById("taskStatusFilter");
            const body = document.getElementById("tasksBody");
            if (!search || !status || !body) return;

            const apply = () => {
                const q = search.value.trim().toLowerCase();
                const s = status.value;
                body.querySelectorAll("tr").forEach((row) => {
                    const hay = (row.getAttribute("data-search") || "").toLowerCase();
                    const st = row.getAttribute("data-status") || "";
                    const okQ = !q || hay.includes(q);
                    const okS = s === "all" || st === s;
                    row.style.display = okQ && okS ? "" : "none";
                });
            };

            search.addEventListener("input", apply);
            status.addEventListener("change", apply);
        }

        async function fetchTaskLog(jobId) {
            const content = document.getElementById("logContent");
            if (!content) return;

            try {
                const response = await fetch(`/api/tasks/${jobId}/log?tail=800`);
                if (!response.ok) {
                    const err = await response.json();
                    content.textContent = `读取日志失败: ${err.detail || response.status}`;
                    return;
                }
                const data = await response.json();
                content.textContent = data.log || data.message || "暂无日志";
            } catch (error) {
                content.textContent = `读取日志异常: ${error.message}`;
            }
        }

        async function pollTaskStatuses() {
            const body = document.getElementById("tasksBody");
            if (!body) return;

            try {
                const response = await fetch("/api/tasks");
                if (!response.ok) return;
                const tasks = await response.json();
                if (!Array.isArray(tasks)) return;

                const byId = new Map(tasks.map((item) => [item.job_id, item]));
                let queuedCount = 0;
                let processingCount = 0;
                let completedCount = 0;
                let failedCount = 0;
                let hasActive = false;

                tasks.forEach((task) => {
                    const st = String(task.status || "").toLowerCase();
                    if (st === "queued") queuedCount += 1;
                    else if (st === "processing") processingCount += 1;
                    else if (st === "completed") completedCount += 1;
                    else if (st === "failed") failedCount += 1;
                    if (st === "queued" || st === "processing") hasActive = true;
                });

                body.querySelectorAll("tr[data-job-id]").forEach((row) => {
                    const jobId = row.dataset.jobId || "";
                    const task = byId.get(jobId);
                    if (!task) return;

                    const statusText = String(task.status || "");
                    const statusKey = statusText.toLowerCase();
                    row.setAttribute("data-status", statusKey);

                    const statusEl = row.querySelector(".status");
                    if (statusEl) {
                        statusEl.className = `status ${statusKey}`;
                        statusEl.textContent = statusText;
                    }

                    const progressEl = row.querySelector(".task-progress");
                    if (progressEl) {
                        progressEl.textContent = task.progress || "";
                    }
                });

                const statQueued = document.getElementById("statQueued");
                const statProcessing = document.getElementById("statProcessing");
                const statCompleted = document.getElementById("statCompleted");
                const statFailed = document.getElementById("statFailed");
                if (statQueued) statQueued.textContent = String(queuedCount);
                if (statProcessing) statProcessing.textContent = String(processingCount);
                if (statCompleted) statCompleted.textContent = String(completedCount);
                if (statFailed) statFailed.textContent = String(failedCount);

                if (!hasActive && pollTaskStatuses._timer) {
                    clearInterval(pollTaskStatuses._timer);
                    pollTaskStatuses._timer = null;
                }
            } catch (error) {
                // polling failure is non-fatal
            }
        }

        function closeTaskLog() {
            const modal = document.getElementById("logModal");
            if (modal) modal.classList.remove("show");
            currentLogJobId = "";
            if (logAutoRefreshTimer) {
                clearInterval(logAutoRefreshTimer);
                logAutoRefreshTimer = null;
            }
            logAutoRefreshEnabled = false;
        }

        async function openTaskLog(jobId, autoRefresh) {
            currentLogJobId = jobId;
            logAutoRefreshEnabled = Boolean(autoRefresh);

            const modal = document.getElementById("logModal");
            const title = document.getElementById("logTitle");
            if (title) {
                title.textContent = autoRefresh ? `任务日志（实时）: ${jobId}` : `任务日志: ${jobId}`;
            }
            if (modal) modal.classList.add("show");

            await fetchTaskLog(jobId);

            if (logAutoRefreshTimer) {
                clearInterval(logAutoRefreshTimer);
                logAutoRefreshTimer = null;
            }
            if (logAutoRefreshEnabled) {
                logAutoRefreshTimer = setInterval(() => {
                    if (currentLogJobId) fetchTaskLog(currentLogJobId);
                }, 2500);
            }
        }

        function _setFormValue(form, name, value) {
            const input = form.querySelector(`[name="${name}"]`);
            if (!input) return;
            input.value = value ?? "";
        }

        function _setFormCheckbox(form, name, value) {
            const input = form.querySelector(`[name="${name}"]`);
            if (!input) return;
            const normalized = String(value || "").toLowerCase();
            input.checked = normalized === "true" || normalized === "1" || normalized === "yes";
        }

        function regenerateTask(jobId) {
            const row = document.querySelector(`#tasksBody tr[data-job-id="${jobId}"]`);
            const form = document.querySelector('form[action="/admin"]');
            if (!row || !form) {
                alert("无法载入任务参数，请刷新页面后重试。");
                return;
            }

            const data = row.dataset || {};
            _setFormValue(form, "repo_url", data.repoUrl || "");
            _setFormValue(form, "commit_id", data.commitId || "");
            _setFormValue(form, "subproject_name", data.subprojectName || "");
            _setFormValue(form, "subproject_path", data.subprojectPath || "");
            _setFormValue(form, "priority", data.priority || "0");
            _setFormValue(form, "output", data.output || "docs/codewiki");
            _setFormValue(form, "include", data.include || "");
            _setFormValue(form, "exclude", data.exclude || "");
            _setFormValue(form, "focus", data.focus || "");
            _setFormValue(form, "doc_type", data.docType || "");
            _setFormValue(form, "instructions", data.instructions || "");
            _setFormValue(form, "skills", data.skills || "");
            _setFormValue(form, "max_tokens", data.maxTokens || "");
            _setFormValue(form, "max_token_per_module", data.maxTokenPerModule || "");
            _setFormValue(form, "max_token_per_leaf_module", data.maxTokenPerLeafModule || "");
            _setFormValue(form, "max_depth", data.maxDepth || "");
            _setFormValue(form, "output_lang", data.outputLang || "");
            _setFormValue(form, "agent_cmd", data.agentCmd || "");
            _setFormValue(form, "custom_cli_args", data.customCliArgs || "");
            _setFormValue(form, "concurrency", data.concurrency || "4");

            _setFormCheckbox(form, "create_branch", data.createBranch);
            _setFormCheckbox(form, "github_pages", data.githubPages);
            _setFormCheckbox(form, "no_cache", data.noCache);

            const advanced = form.querySelector(".options-details");
            if (advanced) advanced.open = true;

            if (typeof window.setAdminPanel === "function") {
                window.setAdminPanel("panel-create");
            } else {
                window.location.hash = "#create";
            }

            const repoInput = form.querySelector('[name="repo_url"]');
            if (repoInput) {
                repoInput.focus();
                repoInput.scrollIntoView({ behavior: "smooth", block: "center" });
            }

            saveAdvancedOptions();
            alert("已载入原任务参数，请确认后手动提交任务。");
        }

        async function stopTask(jobId) {
            if (!confirm("确定停止该任务吗？")) {
                return;
            }
            try {
                const response = await fetch(`/api/tasks/${jobId}/stop`, { method: "POST" });
                if (response.ok) {
                    window.location.reload();
                } else {
                    const data = await response.json();
                    alert("停止任务失败: " + (data.detail || "未知错误"));
                }
            } catch (error) {
                alert("停止任务出错: " + error.message);
            }
        }

        document.addEventListener("DOMContentLoaded", () => {
            initTheme();

            const themeToggle = document.getElementById("themeToggle");
            if (themeToggle) {
                themeToggle.addEventListener("click", toggleTheme);
            }

            loadAdvancedOptions();
            wireAdvancedOptionsPersistence();
            wireAdminPanels();
            wireTaskFilters();

            const refreshBtn = document.getElementById("adminRefresh");
            if (refreshBtn) {
                refreshBtn.addEventListener("click", () => window.location.reload());
            }

            const logRefreshBtn = document.getElementById("logRefreshBtn");
            if (logRefreshBtn) {
                logRefreshBtn.addEventListener("click", () => {
                    if (currentLogJobId) fetchTaskLog(currentLogJobId);
                });
            }

            const logCloseBtn = document.getElementById("logCloseBtn");
            if (logCloseBtn) {
                logCloseBtn.addEventListener("click", closeTaskLog);
            }

            const logModal = document.getElementById("logModal");
            if (logModal) {
                logModal.addEventListener("click", (e) => {
                    if (e.target === logModal) closeTaskLog();
                });
            }

            const hasTasksTable = Boolean(document.getElementById("tasksBody"));
            if (hasTasksTable) {
                pollTaskStatuses();
                pollTaskStatuses._timer = setInterval(pollTaskStatuses, 3000);
            }
        });

        async function deleteTask(jobId) {
            if (!confirm("确定删除该任务吗？")) {
                return;
            }

            try {
                const response = await fetch('/api/tasks/' + jobId, { method: 'DELETE' });
                if (response.ok) {
                    window.location.reload();
                } else {
                    const data = await response.json();
                    alert('删除失败: ' + data.detail);
                }
            } catch (error) {
                alert('删除出错: ' + error.message);
            }
        }
    </script>
</body>
</html>
""")
