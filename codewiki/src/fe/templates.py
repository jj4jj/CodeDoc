#!/usr/bin/env python3
"""
HTML templates for the CodeWiki web application.
"""

# Web interface HTML template
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki 文档中心</title>
    <style>
        :root {
            --bg: #f4f6f8;
            --panel: #ffffff;
            --line: #dbe1e8;
            --text: #132033;
            --muted: #5f6f82;
            --primary: #1f4d7a;
            --primary-soft: #e8f0f7;
            --success: #177245;
            --warning: #9a5e00;
            --danger: #b42318;
        }

        [data-theme="dark"] {
            --bg: #0f1722;
            --panel: #162131;
            --line: #263a52;
            --text: #e6edf7;
            --muted: #99abc2;
            --primary: #63a5df;
            --primary-soft: #1b2d44;
            --success: #46bf83;
            --warning: #e2a341;
            --danger: #f08980;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.5;
            padding: 20px;
        }

        .app { max-width: 1200px; margin: 0 auto; }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 14px;
        }

        .brand {
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: var(--primary);
        }

        .topbar-right { display: flex; align-items: center; gap: 8px; }

        .nav { display: flex; gap: 8px; }

        .nav a {
            text-decoration: none;
            color: var(--muted);
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 0.88rem;
            font-weight: 600;
            background: var(--panel);
        }

        .nav a.active {
            color: var(--primary);
            background: var(--primary-soft);
            border-color: var(--line);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.86rem;
            font-weight: 600;
            cursor: pointer;
            background: var(--panel);
            color: var(--muted);
        }

        .btn:hover { background: var(--primary-soft); color: var(--primary); }

        .hero {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }

        .hero h1 { font-size: 1.3rem; margin-bottom: 4px; }
        .hero p { color: var(--muted); font-size: 0.9rem; margin-bottom: 10px; }

        .hero-actions { display: flex; gap: 8px; flex-wrap: wrap; }

        .alert {
            margin-bottom: 12px;
            border-radius: 8px;
            border: 1px solid transparent;
            padding: 8px 10px;
            font-size: 0.88rem;
            background: var(--panel);
        }

        .alert-success {
            background: color-mix(in srgb, var(--success) 13%, var(--panel));
            color: var(--success);
            border-color: color-mix(in srgb, var(--success) 45%, var(--line));
        }

        .alert-error {
            background: color-mix(in srgb, var(--danger) 12%, var(--panel));
            color: var(--danger);
            border-color: color-mix(in srgb, var(--danger) 45%, var(--line));
        }

        .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 16px;
        }

        .list-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
        }

        .list-head h2 { font-size: 1.06rem; }
        .list-head span { font-size: 0.82rem; color: var(--muted); }

        .list-tools { display: flex; gap: 8px; margin-bottom: 10px; }

        .search {
            flex: 1;
            min-width: 0;
            padding: 9px 10px;
            border: 1px solid var(--line);
            border-radius: 8px;
            font-size: 0.88rem;
            background: var(--panel);
            color: var(--text);
        }

        .search:focus { outline: none; border-color: var(--primary); }

        .jobs {
            display: grid;
            gap: 8px;
            max-height: calc(100vh - 250px);
            overflow: auto;
            padding-right: 2px;
        }

        .job {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 10px;
            background: var(--panel);
        }

        .job-head {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            align-items: start;
        }

        .job-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2px;
        }

        .job-url { font-size: 0.78rem; color: var(--muted); word-break: break-word; }

        .badge {
            font-size: 0.72rem;
            font-weight: 700;
            border-radius: 999px;
            padding: 3px 8px;
            border: 1px solid transparent;
            white-space: nowrap;
            text-transform: uppercase;
        }

        .status-completed { color: var(--success); background: color-mix(in srgb, var(--success) 12%, var(--panel)); border-color: color-mix(in srgb, var(--success) 40%, var(--line)); }
        .status-processing { color: var(--primary); background: color-mix(in srgb, var(--primary) 14%, var(--panel)); border-color: color-mix(in srgb, var(--primary) 40%, var(--line)); }
        .status-queued { color: var(--warning); background: color-mix(in srgb, var(--warning) 12%, var(--panel)); border-color: color-mix(in srgb, var(--warning) 40%, var(--line)); }
        .status-failed { color: var(--danger); background: color-mix(in srgb, var(--danger) 10%, var(--panel)); border-color: color-mix(in srgb, var(--danger) 40%, var(--line)); }

        .job-meta {
            margin-top: 7px;
            font-size: 0.76rem;
            color: var(--muted);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .job-progress {
            margin-top: 7px;
            border-top: 1px dashed var(--line);
            padding-top: 7px;
            font-size: 0.8rem;
            color: var(--muted);
            word-break: break-word;
        }

        .job-actions {
            margin-top: 8px;
            display: flex;
            justify-content: flex-end;
        }

        .empty {
            border: 1px dashed var(--line);
            border-radius: 8px;
            background: var(--panel);
            color: var(--muted);
            text-align: center;
            padding: 24px 16px;
            font-size: 0.9rem;
        }

        @media (max-width: 760px) {
            body { padding: 12px; }
            .topbar { flex-direction: column; align-items: flex-start; }
            .topbar-right { width: 100%; justify-content: space-between; }
            .list-head { flex-direction: column; align-items: flex-start; }
            .job-head { flex-direction: column; }
            .jobs { max-height: none; }
        }
    </style>
</head>
<body>
    <div class="app">
        <header class="topbar">
            <div class="brand">CodeWiki 文档中心</div>
            <div class="topbar-right">
                <nav class="nav">
                    <a class="active" href="/">首页</a>
                    <a href="/admin">控制台</a>
                </nav>
                <button id="themeToggle" class="btn" type="button">深色模式</button>
            </div>
        </header>

        <section class="hero">
            <h1>文档生成列表</h1>
            <p>首页仅用于浏览已生成文档。新建任务请进入控制台。</p>
            <div class="hero-actions">
                <a href="/admin" class="btn">进入控制台创建任务</a>
            </div>
        </section>

        {% if message %}
        <div class="alert alert-{{ message_type }}">{{ message }}</div>
        {% endif %}

        <section class="panel">
            <div class="list-head">
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
        </section>
    </div>

    <script>
        const THEME_KEY = "codewiki_theme";

        function applyTheme(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            const btn = document.getElementById("themeToggle");
            if (btn) {
                btn.textContent = theme === "dark" ? "浅色模式" : "深色模式";
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
"""

# HTML template for the documentation pages
DOCS_VIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.9.0/dist/mermaid.min.js"></script>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #f1f5f9;
            --text-color: #334155;
            --border-color: #e2e8f0;
            --hover-color: #f8fafc;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #ffffff;
        }
        
        .container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 300px;
            background-color: var(--secondary-color);
            border-right: 1px solid var(--border-color);
            padding: 20px;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
        }
        
        .content {
            flex: 1;
            margin-left: 300px;
            padding: 40px 60px;
            max-width: calc(100% - 300px);
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 12px;
            text-decoration: none;
            display: block;
        }

        .home-link {
            display: inline-block;
            font-size: 12px;
            color: #64748b;
            text-decoration: none;
            margin-bottom: 14px;
            border: 1px solid #d8e2ee;
            border-radius: 999px;
            padding: 4px 10px;
        }

        .home-link:hover {
            color: var(--primary-color);
            background: #f8fafc;
        }

        .sidebar-control {
            margin: 12px 0 16px 0;
        }

        .sidebar-control-label {
            display: block;
            font-size: 12px;
            color: #64748b;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .sidebar-control-input {
            width: 100%;
            padding: 8px 10px;
            border: 1px solid #c9d5e3;
            border-radius: 6px;
            font-size: 13px;
            background: #fff;
            color: #334155;
        }

        .sidebar-control-readonly {
            width: 100%;
            padding: 8px 10px;
            border: 1px solid #c9d5e3;
            border-radius: 6px;
            font-size: 13px;
            background: #fff;
            color: #334155;
            line-height: 1.2;
            min-height: 34px;
            display: flex;
            align-items: center;
        }
        
        .nav-section {
            margin-bottom: 25px;
        }
        
        .nav-section h3 {
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }
        
        .nav-item {
            display: block;
            padding: 8px 12px;
            color: var(--text-color);
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.2s ease;
            margin-bottom: 2px;
        }
        
        .nav-item:hover {
            background-color: var(--hover-color);
            color: var(--primary-color);
        }
        
        .nav-item.active {
            background-color: var(--primary-color);
            color: white;
        }
        
        .nav-subsection {
            margin-left: 15px;
            margin-top: 8px;
        }
        
        .nav-subsection .nav-item {
            font-size: 13px;
            color: #64748b;
        }
        
        .nav-section-header {
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
            padding: 8px 12px;
        }
        
        /* Nested subsection indentation - scalable for any depth */
        .nav-subsection .nav-subsection {
            margin-left: 20px;
        }
        
        .nav-subsection .nav-subsection .nav-item {
            font-size: 12px;
        }
        
        /* Additional nesting levels */
        .nav-subsection .nav-subsection .nav-subsection {
            margin-left: 15px;
        }
        
        .nav-subsection .nav-subsection .nav-subsection .nav-item {
            font-size: 11px;
        }
        
        .markdown-content {
            max-width: none;
        }
        
        .markdown-content h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }
        
        .markdown-content h2 {
            font-size: 2rem;
            font-weight: 600;
            color: #334155;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        .markdown-content h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: #475569;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }
        
        .markdown-content p {
            margin-bottom: 1rem;
            color: #475569;
        }
        
        .markdown-content ul, .markdown-content ol {
            margin-bottom: 1rem;
            padding-left: 1.5rem;
        }
        
        .markdown-content li {
            margin-bottom: 0.5rem;
            color: #475569;
        }
        
        .markdown-content code {
            background-color: #f1f5f9;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 0.875rem;
        }
        
        .markdown-content pre {
            background-color: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1rem;
        }
        
        .markdown-content pre code {
            background-color: transparent;
            padding: 0;
        }
        
        .markdown-content blockquote {
            border-left: 4px solid var(--primary-color);
            padding-left: 1rem;
            margin-bottom: 1rem;
            font-style: italic;
            color: #64748b;
        }
        
        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
        
        .markdown-content th, .markdown-content td {
            border: 1px solid var(--border-color);
            padding: 0.75rem;
            text-align: left;
        }
        
        .markdown-content th {
            background-color: var(--secondary-color);
            font-weight: 600;
        }
        
        .markdown-content a {
            color: var(--primary-color);
            text-decoration: underline;
        }
        
        .markdown-content a:hover {
            text-decoration: none;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
            }
            
            .content {
                margin-left: 0;
                padding: 20px;
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <a href="/static-docs/{{ job_id }}/overview.md{{ query_suffix }}" class="logo">📚 {{ repo_name }}</a>
            <a href="{{ docs_home_url or '/' }}" class="home-link">← 返回文档中心</a>
            
            {% if metadata and metadata.generation_info %}
            <div style="margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                <h4 style="margin: 0 0 10px 0; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Generation Info</h4>
                <div style="font-size: 11px; color: #475569; line-height: 1.4;">
                    <div style="margin-bottom: 4px;"><strong>Model:</strong> {{ metadata.generation_info.main_model }}</div>
                    <div style="margin-bottom: 4px;"><strong>Generated:</strong> {{ metadata.generation_info.timestamp[:16] }}</div>
                    {% if metadata.generation_info.commit_id %}
                    <div style="margin-bottom: 4px;"><strong>Commit:</strong> {{ metadata.generation_info.commit_id[:8] }}</div>
                    {% endif %}
                    {% if metadata.statistics %}
                    <div><strong>Components:</strong> {{ metadata.statistics.total_components }}</div>
                    {% endif %}
                </div>
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
                <a href="/static-docs/{{ job_id }}/overview.md{{ query_suffix }}" class="nav-item {% if current_page == 'overview.md' %}active{% endif %}">
                    Overview
                </a>
            </div>
            
            {% macro render_nav_item(key, data, depth=0) %}
                {% set indent_class = 'nav-subsection' if depth > 0 else '' %}
                {% set indent_style = 'margin-left: ' + (depth * 15)|string + 'px;' if depth > 0 else '' %}
                <div class="{{ indent_class }}" {% if indent_style %}style="{{ indent_style }}"{% endif %}>
                    {% if data.components %}
                        <a href="/static-docs/{{ job_id }}/{{ key }}.md{{ query_suffix }}" class="nav-item {% if current_page == key + '.md' %}active{% endif %}">
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
                <a href="/static-docs/{{ job_id }}/{{ nav_item.path }}{{ query_suffix }}" class="nav-item {% if current_page == nav_item.path %}active{% endif %}">
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
            <div class="markdown-content">
                {{ content | safe }}
            </div>
        </main>
    </div>
    
    <script>
        // Initialize mermaid with configuration
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#2563eb',
                primaryTextColor: '#334155',
                primaryBorderColor: '#e2e8f0',
                lineColor: '#64748b',
                sectionBkgColor: '#f8fafc',
                altSectionBkgColor: '#f1f5f9',
                gridColor: '#e2e8f0',
                secondaryColor: '#f1f5f9',
                tertiaryColor: '#f8fafc'
            },
            flowchart: {
                htmlLabels: true,
                curve: 'basis'
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
        
        // Re-render mermaid diagrams after page load
        document.addEventListener('DOMContentLoaded', function() {
            const buildQuery = () => {
                const params = new URLSearchParams(window.location.search);
                const versionSelect = document.getElementById('versionSelect');
                const languageSelect = document.getElementById('languageSelect');
                if (versionSelect) {
                    const version = versionSelect.value || '';
                    if (version) params.set('version', version);
                    else params.delete('version');
                }
                if (languageSelect) {
                    const lang = languageSelect.value || '';
                    if (lang) params.set('lang', lang);
                    else params.delete('lang');
                }
                const query = params.toString();
                return query ? ('?' + query) : '';
            };

            const versionSelect = document.getElementById('versionSelect');
            if (versionSelect) {
                versionSelect.addEventListener('change', function() {
                    window.location.href = '/static-docs/{{ job_id }}/{{ current_page }}' + buildQuery();
                });
            }

            const languageSelect = document.getElementById('languageSelect');
            if (languageSelect) {
                languageSelect.addEventListener('change', function() {
                    window.location.href = '/static-docs/{{ job_id }}/{{ current_page }}' + buildQuery();
                });
            }
            const viewSelect = document.getElementById('viewSelect');
            if (viewSelect) {
                viewSelect.addEventListener('change', function() {
                    const targetJobId = viewSelect.value || '{{ job_id }}';
                    const params = new URLSearchParams(window.location.search);
                    params.delete('version');
                    const query = params.toString();
                    window.location.href = '/static-docs/' + targetJobId + '/overview.md' + (query ? ('?' + query) : '');
                });
            }
            mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        });
    </script>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeWiki 控制台</title>
    <style>
        :root {
            --bg: #f4f6f8;
            --panel: #ffffff;
            --line: #dbe1e8;
            --text: #132033;
            --muted: #5f6f82;
            --primary: #1f4d7a;
            --primary-soft: #e8f0f7;
            --success: #177245;
            --warning: #9a5e00;
            --danger: #b42318;
            --info: #1e4e8c;
        }

        [data-theme="dark"] {
            --bg: #0f1722;
            --panel: #162131;
            --line: #263a52;
            --text: #e6edf7;
            --muted: #99abc2;
            --primary: #63a5df;
            --primary-soft: #1b2d44;
            --success: #46bf83;
            --warning: #e2a341;
            --danger: #f08980;
            --info: #78b8f2;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.5;
            padding: 20px;
        }

        .app { max-width: 1240px; margin: 0 auto; }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 14px;
        }

        .brand {
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: var(--primary);
        }

        .topbar-right { display: flex; align-items: center; gap: 8px; }

        .nav { display: flex; gap: 8px; }

        .nav a {
            text-decoration: none;
            color: var(--muted);
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 0.88rem;
            font-weight: 600;
            background: var(--panel);
        }

        .nav a.active {
            color: var(--primary);
            background: var(--primary-soft);
            border-color: var(--line);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            background: var(--panel);
            color: var(--muted);
        }

        .btn:hover { background: var(--primary-soft); color: var(--primary); }

        .btn-primary {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }

        .btn-primary:hover { background: color-mix(in srgb, var(--primary) 85%, #000 15%); color: #fff; }

        .btn-danger {
            color: var(--danger);
            border-color: color-mix(in srgb, var(--danger) 40%, var(--line));
        }

        .btn-danger:hover { background: color-mix(in srgb, var(--danger) 10%, var(--panel)); color: var(--danger); }

        .hero {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }

        .hero h1 { font-size: 1.3rem; margin-bottom: 4px; }
        .hero p { color: var(--muted); font-size: 0.9rem; }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }

        .stat {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 12px;
        }

        .stat .value {
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 2px;
        }

        .stat .label {
            font-size: 0.82rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .stat.queued .value { color: var(--warning); }
        .stat.processing .value { color: var(--info); }
        .stat.completed .value { color: var(--success); }
        .stat.failed .value { color: var(--danger); }

        .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }

        .panel h2 { font-size: 1.08rem; margin-bottom: 10px; }

        .alert {
            margin-bottom: 10px;
            border-radius: 8px;
            border: 1px solid color-mix(in srgb, var(--danger) 45%, var(--line));
            background: color-mix(in srgb, var(--danger) 10%, var(--panel));
            color: var(--danger);
            padding: 8px 10px;
            font-size: 0.88rem;
        }

        .alert.alert-success {
            border: 1px solid color-mix(in srgb, var(--success) 45%, var(--line));
            background: color-mix(in srgb, var(--success) 10%, var(--panel));
            color: var(--success);
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 210px 130px;
            gap: 10px;
        }

        .field { margin-bottom: 10px; }

        .field label {
            display: block;
            font-size: 0.83rem;
            font-weight: 600;
            margin-bottom: 4px;
            color: var(--muted);
        }

        .field input,
        .field select,
        .field textarea {
            width: 100%;
            padding: 9px 10px;
            border: 1px solid var(--line);
            border-radius: 8px;
            font-size: 0.88rem;
            background: var(--panel);
            color: var(--text);
        }

        .field input:focus,
        .field select:focus,
        .field textarea:focus {
            outline: none;
            border-color: var(--primary);
        }

        .actions-row { display: flex; justify-content: flex-end; gap: 8px; }

        .options-details {
            margin-bottom: 10px;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--panel);
            padding: 6px;
        }

        .options-details summary {
            cursor: pointer;
            font-weight: 600;
            color: var(--muted);
            padding: 6px 8px;
            list-style: none;
        }

        .options-details summary::-webkit-details-marker { display: none; }
        .options-details summary::before { content: "+ "; color: var(--muted); }
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

        .check-field input[type="checkbox"] { width: 16px; height: 16px; }
        .check-field label { font-size: 0.85rem; color: var(--muted); }

        .task-toolbar { display: flex; gap: 8px; margin-bottom: 10px; }

        .task-toolbar input,
        .task-toolbar select {
            padding: 8px 10px;
            border: 1px solid var(--line);
            border-radius: 8px;
            font-size: 0.85rem;
            background: var(--panel);
            color: var(--text);
        }

        .task-toolbar input { flex: 1; min-width: 0; }

        .table-wrap {
            overflow: auto;
            border: 1px solid var(--line);
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.86rem;
            min-width: 900px;
        }

        th,
        td {
            text-align: left;
            padding: 9px 10px;
            border-bottom: 1px solid var(--line);
            vertical-align: top;
        }

        th {
            background: color-mix(in srgb, var(--panel) 88%, var(--line) 12%);
            color: var(--muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }

        tr:last-child td { border-bottom: none; }

        .task-title {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 2px;
        }

        .task-url { font-size: 0.76rem; color: var(--muted); word-break: break-word; }

        .status {
            display: inline-flex;
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 0.72rem;
            font-weight: 700;
            border: 1px solid transparent;
            text-transform: uppercase;
        }

        .status.queued { color: var(--warning); background: color-mix(in srgb, var(--warning) 12%, var(--panel)); border-color: color-mix(in srgb, var(--warning) 40%, var(--line)); }
        .status.processing { color: var(--info); background: color-mix(in srgb, var(--info) 12%, var(--panel)); border-color: color-mix(in srgb, var(--info) 40%, var(--line)); }
        .status.completed { color: var(--success); background: color-mix(in srgb, var(--success) 12%, var(--panel)); border-color: color-mix(in srgb, var(--success) 40%, var(--line)); }
        .status.failed { color: var(--danger); background: color-mix(in srgb, var(--danger) 10%, var(--panel)); border-color: color-mix(in srgb, var(--danger) 40%, var(--line)); }
        .status.stopped { color: var(--muted); background: color-mix(in srgb, var(--muted) 14%, var(--panel)); border-color: color-mix(in srgb, var(--muted) 35%, var(--line)); }

        .task-progress { color: var(--muted); word-break: break-word; }
        .task-actions { display: flex; gap: 6px; }

        .log-modal {
            position: fixed;
            inset: 0;
            background: rgba(8, 16, 26, 0.5);
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
            width: min(1000px, 100%);
            max-height: 80vh;
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .log-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-bottom: 1px solid var(--line);
        }

        .log-head strong {
            color: var(--primary);
            font-size: 0.9rem;
        }

        .log-body {
            padding: 10px 12px;
            overflow: auto;
            background: color-mix(in srgb, var(--panel) 92%, var(--line) 8%);
        }

        .log-body pre {
            margin: 0;
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 0.78rem;
            line-height: 1.45;
            color: var(--text);
        }

        .empty {
            border: 1px dashed var(--line);
            border-radius: 8px;
            background: var(--panel);
            color: var(--muted);
            text-align: center;
            padding: 24px 16px;
            font-size: 0.9rem;
        }

        details.error { margin-top: 6px; }
        details.error summary { cursor: pointer; color: var(--danger); font-weight: 600; font-size: 0.8rem; }

        details.error pre {
            margin-top: 6px;
            border: 1px solid color-mix(in srgb, var(--danger) 40%, var(--line));
            border-radius: 6px;
            padding: 8px;
            background: color-mix(in srgb, var(--danger) 10%, var(--panel));
            color: var(--danger);
            white-space: pre-wrap;
            font-size: 0.76rem;
            line-height: 1.4;
        }

        @media (max-width: 1120px) {
            .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .options-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        @media (max-width: 760px) {
            body { padding: 12px; }
            .topbar { flex-direction: column; align-items: flex-start; }
            .topbar-right { width: 100%; justify-content: space-between; }
            .form-grid { grid-template-columns: 1fr; }
            .options-grid { grid-template-columns: 1fr; }
            .stats { grid-template-columns: 1fr; }
            .task-toolbar { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="app">
        <header class="topbar">
            <div class="brand">CodeWiki 文档中心</div>
            <div class="topbar-right">
                <nav class="nav">
                    <a href="/">首页</a>
                    <a class="active" href="/admin">控制台</a>
                    <a href="/api/tasks" target="_blank">任务 API</a>
                </nav>
                <button id="themeToggle" class="btn" type="button">深色模式</button>
            </div>
        </header>

        <section class="hero">
            <h1>任务控制台</h1>
            <p>创建文档任务，查看队列状态，并管理已完成或失败任务。</p>
            <p style="margin-top:8px;color:var(--muted);font-size:13px;">
                任务并行执行: {{ task_concurrency }} / {{ task_concurrency_max }}（可通过启动参数 `--task-concurrency` 配置）
            </p>
        </section>

        <section class="stats">
            <article class="stat queued">
                <div class="value">{{ queued_count }}</div>
                <div class="label">Queued</div>
            </article>
            <article class="stat processing">
                <div class="value">{{ processing_count }}</div>
                <div class="label">Processing</div>
            </article>
            <article class="stat completed">
                <div class="value">{{ completed_count }}</div>
                <div class="label">Completed</div>
            </article>
            <article class="stat failed">
                <div class="value">{{ failed_count }}</div>
                <div class="label">Failed</div>
            </article>
        </section>

        <section class="panel">
            <h2>创建新任务</h2>

            {% if error %}
            <div class="alert">{{ error }}</div>
            {% endif %}
            {% if message %}
            <div class="alert {% if message_type == 'success' %}alert-success{% endif %}">{{ message }}</div>
            {% endif %}

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

        <section class="panel">
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
                    <div style="padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg-soft);">
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

        <section class="panel">
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
                        <tr data-status="{{ job.status }}" data-search="{{ (job.title or '') ~ ' ' ~ job.repo_url ~ ' ' ~ job.job_id ~ ' ' ~ (job.progress or '') ~ ' ' ~ ((job.options.subproject_name if job.options and job.options.subproject_name else '') ) ~ ' ' ~ ((job.options.subproject_path if job.options and job.options.subproject_path else '') ) }}">
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
                                    <button class="btn" onclick="regenerateTask('{{ job.job_id }}')" title="重新生成">重新生成</button>
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
        const THEME_KEY = "codewiki_theme";
        let currentLogJobId = "";
        let logAutoRefreshTimer = null;
        let logAutoRefreshEnabled = false;

        function applyTheme(theme) {
            document.documentElement.setAttribute("data-theme", theme);
            const btn = document.getElementById("themeToggle");
            if (btn) {
                btn.textContent = theme === "dark" ? "浅色模式" : "深色模式";
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

        async function regenerateTask(jobId) {
            if (!confirm("确定为该任务重新生成文档吗？将创建新的版本目录。")) {
                return;
            }
            try {
                const response = await fetch(`/api/tasks/${jobId}/regenerate`, { method: "POST" });
                if (response.ok) {
                    window.location.reload();
                } else {
                    const data = await response.json();
                    alert("重新生成失败: " + (data.detail || "未知错误"));
                }
            } catch (error) {
                alert("重新生成出错: " + error.message);
            }
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
"""
