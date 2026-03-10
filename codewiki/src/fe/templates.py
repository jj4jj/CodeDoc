#!/usr/bin/env python3
"""
HTML templates for the CodeWiki web application.
"""

_SHARED_UI_TOKENS = """
        :root {
            --bg: #f3f5f8;
            --surface: #ffffff;
            --surface-soft: #eef2f7;
            --surface-hover: #f5f8fc;
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

        [data-theme="slate"] {
            --bg: #f1f4f8;
            --surface: #ffffff;
            --surface-soft: #e9eef4;
            --surface-hover: #edf3f9;
            --line: #cdd6e0;
            --line-strong: #b5c1cf;
            --text: #1b2736;
            --muted: #617184;
            --primary: #3c5f84;
            --primary-strong: #2e4a68;
            --primary-soft: #e4edf6;
            --success: #2f6d58;
            --warning: #866432;
            --danger: #9a4740;
            --shadow: 0 1px 2px rgba(22, 34, 51, 0.06);
        }

        [data-theme="sage"] {
            --bg: #f2f6f2;
            --surface: #ffffff;
            --surface-soft: #e8f0e8;
            --surface-hover: #edf4ed;
            --line: #cbd9cb;
            --line-strong: #b2c7b2;
            --text: #1f2d22;
            --muted: #5f7564;
            --primary: #3e6b4f;
            --primary-strong: #30543d;
            --primary-soft: #dfecdf;
            --success: #2f714f;
            --warning: #7a6732;
            --danger: #8f4a3f;
            --shadow: 0 1px 2px rgba(23, 34, 27, 0.08);
        }

        [data-theme="dark"] {
            --bg: #111823;
            --surface: #172334;
            --surface-soft: #1c2a3d;
            --surface-hover: #223249;
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
            transition: background-color 0.16s ease, border-color 0.16s ease;
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

        .theme-select {
            min-width: 126px;
            height: 34px;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            font-size: 0.8rem;
            padding: 0 8px;
            border-radius: var(--radius-sm);
        }

        .theme-toggle-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .theme-icon-light {
            display: inline-flex;
        }

        .theme-icon-dark {
            display: none;
        }

        [data-theme="dark"] .theme-icon-light {
            display: none;
        }

        [data-theme="dark"] .theme-icon-dark {
            display: inline-flex;
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

        .doc-card,
        .rank-item,
        .stat-chip,
        .stat,
        .agent-item,
        .sidebar-info,
        .table-wrap {
            transition: background-color 0.16s ease, border-color 0.16s ease;
        }

        @media (hover: hover) {
            .doc-card:hover,
            .rank-item:hover,
            .stat-chip:hover,
            .stat:hover,
            .agent-item:hover,
            .sidebar-info:hover {
                background: var(--surface-hover);
                border-color: var(--line-strong);
            }
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
        .app {
            max-width: 1580px;
            min-height: 100vh;
        }

        .topbar {
            min-height: 90px;
            padding: 16px 20px;
            justify-content: space-between;
        }

        .home-hint {
            flex: 1;
            text-align: center;
            color: var(--muted);
            font-size: 0.9rem;
            letter-spacing: 0.01em;
            padding: 0 16px;
        }

        .portal-layout {
            display: grid;
            grid-template-columns: 330px minmax(0, 1fr);
            gap: 14px;
            min-height: calc(100vh - 152px);
        }

        .left-rail {
            display: flex;
            flex-direction: column;
            gap: 12px;
            min-height: 0;
        }

        .rail-title {
            font-size: 0.86rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
        }

        .rank-tabs {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 8px;
        }

        .rank-tab {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 600;
            padding: 7px 8px;
            cursor: pointer;
            border-radius: var(--radius-sm);
        }

        .rank-tab.active {
            border-color: var(--primary);
            background: var(--primary-soft);
            color: var(--primary);
        }

        .rank-list {
            border: 1px solid var(--line);
            background: var(--surface);
            overflow: auto;
            min-height: 0;
            max-height: calc(100vh - 260px);
            border-radius: var(--radius-sm);
        }

        .rank-item {
            border-bottom: 1px solid var(--line);
            padding: 10px 11px;
        }

        .rank-item:last-child {
            border-bottom: none;
        }

        .rank-item a {
            display: block;
            text-decoration: none;
            color: var(--text);
        }

        .rank-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 3px;
        }

        .rank-title {
            font-size: 0.84rem;
            font-weight: 700;
            color: var(--primary);
        }

        .rank-score {
            font-size: 0.72rem;
            color: var(--muted);
            white-space: nowrap;
        }

        .rank-badges {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .rank-type {
            font-size: 0.92rem;
            line-height: 1;
            display: inline-flex;
            align-items: center;
        }

        .rank-sub {
            color: var(--muted);
            font-size: 0.76rem;
            line-height: 1.4;
            word-break: break-word;
        }

        .catalog {
            display: flex;
            flex-direction: column;
            min-height: 0;
        }

        .catalog-toolbar {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 160px 190px auto;
            gap: 8px;
            margin-bottom: 12px;
        }

        .catalog-toolbar .search,
        .catalog-toolbar select {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            padding: 10px 12px;
            font-size: 0.86rem;
            border-radius: var(--radius-sm);
        }

        .stats-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 12px;
        }

        .stat-chip {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            padding: 8px 10px;
            border-radius: var(--radius-sm);
        }

        .stat-value {
            font-size: 1.12rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.2;
        }

        .stat-label {
            font-size: 0.74rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            overflow: auto;
            padding-right: 2px;
            max-height: calc(100vh - 324px);
        }

        .doc-card {
            border: 1px solid var(--line);
            background: var(--surface);
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            border-radius: var(--radius-sm);
            cursor: pointer;
        }

        .card-head {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
        }

        .card-title {
            color: var(--primary);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 700;
            line-height: 1.35;
        }

        .card-title:hover {
            text-decoration: underline;
        }

        .card-tag {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            color: var(--muted);
            font-size: 0.72rem;
            padding: 2px 7px;
            white-space: nowrap;
            border-radius: var(--radius-sm);
        }

        .card-type-list {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
            justify-content: flex-end;
            max-width: 180px;
        }

        .card-type-icon {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1;
            width: 28px;
            height: 24px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
        }

        .card-sub {
            color: var(--muted);
            font-size: 0.78rem;
            word-break: break-word;
            line-height: 1.35;
        }

        .card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            color: var(--muted);
            font-size: 0.74rem;
            border-top: 1px dashed var(--line);
            border-bottom: 1px dashed var(--line);
            padding: 8px 0;
        }

        .card-subprojects {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            color: var(--muted);
            font-size: 0.75rem;
        }

        .card-chip {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            color: var(--muted);
            font-size: 0.72rem;
            padding: 1px 7px;
            border-radius: var(--radius-sm);
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .engage {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .engage-btn {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            font-size: 0.78rem;
            padding: 4px 8px;
            cursor: pointer;
            border-radius: var(--radius-sm);
        }

        .engage-btn.active {
            color: var(--primary);
            border-color: var(--primary);
            background: var(--primary-soft);
        }

        .card-open {
            text-decoration: none;
            border: 1px solid var(--primary);
            background: var(--primary);
            color: #fff;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 6px 10px;
            border-radius: var(--radius-sm);
        }

        .card-open:hover {
            background: var(--primary-strong);
            border-color: var(--primary-strong);
        }

        .alert-error {
            border-color: #dfbebc;
            background: #fbf1f0;
            color: var(--danger);
        }

        @media (max-width: 1240px) {
            .portal-layout {
                grid-template-columns: 1fr;
            }

            .rank-list {
                max-height: none;
            }

            .cards-grid {
                max-height: none;
            }
        }

        @media (max-width: 940px) {
            .topbar {
                flex-wrap: wrap;
                gap: 10px;
                min-height: auto;
            }

            .home-hint {
                order: 3;
                width: 100%;
                text-align: left;
                padding: 0;
            }

            .catalog-toolbar {
                grid-template-columns: 1fr;
            }

            .stats-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .cards-grid {
                grid-template-columns: 1fr;
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
                <select id="themePreset" class="theme-select" aria-label="主题配色">
                    <option value="light">浅色蓝</option>
                    <option value="slate">雾蓝灰</option>
                    <option value="sage">清新绿</option>
                    <option value="dark">深色夜</option>
                </select>
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
        <div class="alert {% if message_type == 'success' %}alert-success{% elif message_type == 'error' %}alert-error{% endif %}">{{ message }}</div>
        {% endif %}

        <section class="portal-layout">
            <aside class="panel left-rail">
                <div class="rank-tabs">
                    <button type="button" class="rank-tab active" data-rank-mode="hot">热门</button>
                    <button type="button" class="rank-tab" data-rank-mode="latest">最新</button>
                    <button type="button" class="rank-tab" data-rank-mode="favorites">收藏</button>
                </div>
                <div id="rankList" class="rank-list">
                    {% for item in home_leaderboard %}
                    <div class="rank-item" data-job-id="{{ item.job_id }}">
                        <a href="/docs/{{ item.job_id }}" target="_blank" rel="noopener">
                            <div class="rank-head">
                                <span class="rank-title">{{ item.display_title }}</span>
                                <span class="rank-badges">
                                    <span class="rank-type" title="文档类型: {{ item.doc_type }}">{{ item.doc_type_icon }}</span>
                                    <span class="rank-score">🔥 {{ item.score }}</span>
                                </span>
                            </div>
                            <div class="rank-sub">{{ item.repo_url }}</div>
                        </a>
                    </div>
                    {% endfor %}
                    {% if not home_leaderboard %}
                    <div class="empty">暂无榜单数据</div>
                    {% endif %}
                </div>
            </aside>

            <main class="panel catalog">
                <div class="catalog-toolbar">
                    <input id="homeSearch" class="search" type="text" placeholder="搜索/筛选文档仓库、子项目、文档类型...">
                    <select id="homeStatusFilter">
                        <option value="all">全部状态</option>
                        <option value="completed">Completed</option>
                        <option value="processing">Processing</option>
                        <option value="queued">Queued</option>
                        <option value="failed">Failed</option>
                    </select>
                    <select id="homeSortMode">
                        <option value="score">排序: 热度优先</option>
                        <option value="latest">排序: 最新优先</option>
                        <option value="likes">排序: 点赞优先</option>
                        <option value="favorites">排序: 收藏优先</option>
                    </select>
                    <button class="btn" type="button" id="homeRefresh">刷新</button>
                </div>

                <div class="stats-strip">
                    <div class="stat-chip">
                        <div class="stat-value">{{ home_stats.total_docs if home_stats else 0 }}</div>
                        <div class="stat-label">文档仓库</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-value">{{ home_stats.total_components if home_stats else 0 }}</div>
                        <div class="stat-label">组件总数</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-value">{{ home_stats.total_files if home_stats else 0 }}</div>
                        <div class="stat-label">Markdown 文件</div>
                    </div>
                    <div class="stat-chip">
                        <div class="stat-value">{{ home_stats.total_views if home_stats else 0 }}</div>
                        <div class="stat-label">浏览量</div>
                    </div>
                </div>

                {% if home_cards %}
                <div id="cardsGrid" class="cards-grid">
                    {% for card in home_cards %}
                    <article
                        class="doc-card"
                        data-job-id="{{ card.job_id }}"
                        data-title="{{ card.title }}"
                        data-display-title="{{ card.display_title }}"
                        data-search="{{ card.display_title ~ ' ' ~ card.title ~ ' ' ~ card.repo_url ~ ' ' ~ card.subproject ~ ' ' ~ card.doc_type }}"
                        data-status="{{ card.status }}"
                        data-created-at="{{ card.completed_at }}"
                        data-doc-type="{{ card.doc_type }}"
                        data-doc-type-icon="{{ card.doc_type_icon }}"
                        data-likes="{{ card.likes }}"
                        data-favorites="{{ card.favorites }}"
                        data-views="{{ card.views }}"
                        data-score="{{ card.score }}"
                        data-liked="false"
                        data-favorited="false"
                    >
                        <div class="card-head">
                            <a class="card-title" href="/docs/{{ card.job_id }}" target="_blank" rel="noopener">{{ card.display_title }}</a>
                            <div class="card-type-list" aria-label="文档类型列表">
                                {% for doc_view in card.doc_types %}
                                <span class="card-type-icon" title="文档类型: {{ doc_view.name }}">{{ doc_view.icon }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        <div class="card-sub">{{ card.repo_url }}</div>
                        <div class="card-meta">
                            <span>时间: {{ card.completed_at }}</span>
                            <span>子项目: {{ card.subprojects|length }} 个</span>
                            <span>文档视图: {{ card.doc_types|length }} 个</span>
                            <span>组件: {{ card.components_count }}</span>
                            <span>文件: {{ card.file_count }}</span>
                        </div>
                        <div class="card-subprojects">
                            <span>子项目:</span>
                            {% for sp in card.subprojects %}
                            <span class="card-chip">{{ sp }}</span>
                            {% endfor %}
                        </div>
                        <div class="card-footer">
                            <div class="engage">
                                <button type="button" class="engage-btn" data-action="like" data-job-id="{{ card.job_id }}">
                                    👍 <span class="value">{{ card.likes }}</span>
                                </button>
                                <button type="button" class="engage-btn" data-action="favorite" data-job-id="{{ card.job_id }}">
                                    ★ <span class="value">{{ card.favorites }}</span>
                                </button>
                                <span class="rank-score">👁 {{ card.views }}</span>
                            </div>
                            <a class="card-open" href="/docs/{{ card.job_id }}" target="_blank" rel="noopener">打开文档</a>
                        </div>
                    </article>
                    {% endfor %}
                </div>
                {% else %}
                <div class="empty">暂无可访问文档，请先到控制台创建任务。</div>
                {% endif %}
            </main>
        </section>
    </div>

    <script>
        const THEME_KEY = "codewiki_theme";
        const THEME_PRESETS = ["light", "slate", "sage", "dark"];
        const THEME_LABELS = {
            light: "浅色蓝",
            slate: "雾蓝灰",
            sage: "清新绿",
            dark: "深色夜",
        };
        const CLIENT_ID_KEY = "codewiki_home_client_id";

        function normalizeTheme(theme) {
            return THEME_PRESETS.includes(theme) ? theme : "light";
        }

        function applyTheme(theme) {
            const normalized = normalizeTheme(theme);
            document.documentElement.setAttribute("data-theme", normalized);
            const select = document.getElementById("themePreset");
            if (select && select.value !== normalized) {
                select.value = normalized;
            }
            const btn = document.getElementById("themeToggle");
            if (btn) {
                const index = THEME_PRESETS.indexOf(normalized);
                const next = THEME_PRESETS[(index + 1) % THEME_PRESETS.length];
                const nextLabel = `切换主题（下一个: ${THEME_LABELS[next] || next}）`;
                btn.setAttribute("title", nextLabel);
                btn.setAttribute("aria-label", nextLabel);
            }
        }

        function initTheme() {
            const stored = normalizeTheme(localStorage.getItem(THEME_KEY) || "light");
            applyTheme(stored);
        }

        const MERMAID_DEBUG =
            (new URLSearchParams(window.location.search).get("debugMermaid") === "1")
            || (window.localStorage.getItem("cw_debug_mermaid") === "1");
        const mermaidLog = (...args) => {
            if (MERMAID_DEBUG) console.log("[MermaidLB][shell]", ...args);
        };

        function toggleTheme() {
            const current = normalizeTheme(document.documentElement.getAttribute("data-theme") || "light");
            const index = THEME_PRESETS.indexOf(current);
            const next = THEME_PRESETS[(index + 1) % THEME_PRESETS.length];
            localStorage.setItem(THEME_KEY, next);
            applyTheme(next);
        }

        function ensureClientId() {
            let clientId = localStorage.getItem(CLIENT_ID_KEY) || "";
            if (!clientId) {
                clientId = "c" + Math.random().toString(16).slice(2) + Date.now().toString(16);
                localStorage.setItem(CLIENT_ID_KEY, clientId);
            }
            return clientId;
        }

        function parseCardTimestamp(raw) {
            const value = String(raw || "").replace(" ", "T");
            const ts = Date.parse(value);
            return Number.isNaN(ts) ? 0 : ts;
        }

        function cardScore(card) {
            return Number(card.dataset.score || 0);
        }

        function cardLikes(card) {
            return Number(card.dataset.likes || 0);
        }

        function cardFavorites(card) {
            return Number(card.dataset.favorites || 0);
        }

        function cardCreatedAt(card) {
            return parseCardTimestamp(card.dataset.createdAt || "");
        }

        function escapeHtml(text) {
            return String(text || "")
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\"/g, "&quot;")
                .replace(/'/g, "&#39;");
        }

        function setButtonState(card, action, active) {
            const selector = `.engage-btn[data-action="${action}"][data-job-id="${card.dataset.jobId}"]`;
            const btn = card.querySelector(selector);
            if (!btn) return;
            btn.classList.toggle("active", Boolean(active));
        }

        function renderRankList(mode) {
            const rankList = document.getElementById("rankList");
            const cards = Array.from(document.querySelectorAll("#cardsGrid .doc-card"));
            if (!rankList || !cards.length) return;

            let items = cards.slice();
            if (mode === "favorites") {
                items = items.filter((card) => card.dataset.favorited === "true");
                items.sort((a, b) => cardFavorites(b) - cardFavorites(a));
            } else if (mode === "latest") {
                items.sort((a, b) => cardCreatedAt(b) - cardCreatedAt(a));
            } else {
                items.sort((a, b) => cardScore(b) - cardScore(a));
            }

            const top = items.slice(0, 10);
            if (!top.length) {
                rankList.innerHTML = '<div class="empty">当前分类暂无内容</div>';
                return;
            }

            rankList.innerHTML = top.map((card) => {
                const title = card.dataset.displayTitle || card.dataset.title || card.dataset.jobId || "";
                const repo = (card.querySelector(".card-sub") || {}).textContent || "";
                const score = card.dataset.score || "0";
                const docType = card.dataset.docType || "default";
                const docTypeIcon = card.dataset.docTypeIcon || "📄";
                return `
                    <div class="rank-item" data-job-id="${card.dataset.jobId}">
                        <a href="/docs/${card.dataset.jobId}" target="_blank" rel="noopener">
                            <div class="rank-head">
                                <span class="rank-title">${escapeHtml(title)}</span>
                                <span class="rank-badges">
                                    <span class="rank-type" title="文档类型: ${escapeHtml(docType)}">${escapeHtml(docTypeIcon)}</span>
                                    <span class="rank-score">🔥 ${score}</span>
                                </span>
                            </div>
                            <div class="rank-sub">${escapeHtml(repo)}</div>
                        </a>
                    </div>
                `;
            }).join("");
        }

        function applyFiltersAndSort() {
            const cardsGrid = document.getElementById("cardsGrid");
            if (!cardsGrid) return;
            const cards = Array.from(cardsGrid.querySelectorAll(".doc-card"));
            const q = (document.getElementById("homeSearch")?.value || "").trim().toLowerCase();
            const st = document.getElementById("homeStatusFilter")?.value || "all";
            const sort = document.getElementById("homeSortMode")?.value || "score";

            cards.forEach((card) => {
                const hay = (card.dataset.search || "").toLowerCase();
                const status = card.dataset.status || "";
                const visible = (!q || hay.includes(q)) && (st === "all" || st === status);
                card.style.display = visible ? "" : "none";
            });

            const visible = cards.filter((card) => card.style.display !== "none");
            visible.sort((a, b) => {
                if (sort === "latest") return cardCreatedAt(b) - cardCreatedAt(a);
                if (sort === "likes") return cardLikes(b) - cardLikes(a);
                if (sort === "favorites") return cardFavorites(b) - cardFavorites(a);
                return cardScore(b) - cardScore(a);
            });
            visible.forEach((card) => cardsGrid.appendChild(card));
        }

        async function loadEngagementMetrics(clientId) {
            const cards = Array.from(document.querySelectorAll("#cardsGrid .doc-card"));
            if (!cards.length) return;
            try {
                const res = await fetch(`/api/docs/engagement?client_id=${encodeURIComponent(clientId)}`);
                if (!res.ok) return;
                const data = await res.json();
                const serverClientId = data.client_id || clientId;
                if (serverClientId !== clientId) {
                    localStorage.setItem(CLIENT_ID_KEY, serverClientId);
                }
                const metrics = data.metrics || {};
                cards.forEach((card) => {
                    const m = metrics[card.dataset.jobId];
                    if (!m) return;
                    card.dataset.likes = String(m.likes || 0);
                    card.dataset.favorites = String(m.favorites || 0);
                    card.dataset.views = String(m.views || 0);
                    card.dataset.score = String(m.score || 0);
                    card.dataset.liked = m.liked ? "true" : "false";
                    card.dataset.favorited = m.favorited ? "true" : "false";
                    const likeBtn = card.querySelector('.engage-btn[data-action="like"] .value');
                    const favBtn = card.querySelector('.engage-btn[data-action="favorite"] .value');
                    if (likeBtn) likeBtn.textContent = String(m.likes || 0);
                    if (favBtn) favBtn.textContent = String(m.favorites || 0);
                    setButtonState(card, "like", m.liked);
                    setButtonState(card, "favorite", m.favorited);
                });
            } catch (e) {
                // ignore load failures
            }
        }

        async function toggleEngagement(button, clientId) {
            const jobId = button.dataset.jobId || "";
            const action = button.dataset.action || "";
            if (!jobId || !action) return;
            const card = button.closest(".doc-card");
            if (!card) return;

            const currentlyActive = button.classList.contains("active");
            const enabled = !currentlyActive;
            button.disabled = true;
            try {
                const res = await fetch(`/api/docs/${encodeURIComponent(jobId)}/engagement`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        type: action,
                        enabled: enabled,
                        client_id: clientId,
                    }),
                });
                if (!res.ok) throw new Error("request failed");
                const data = await res.json();
                const m = (data && data.metrics) || {};
                card.dataset.likes = String(m.likes || 0);
                card.dataset.favorites = String(m.favorites || 0);
                card.dataset.views = String(m.views || 0);
                card.dataset.score = String(m.score || 0);
                card.dataset.liked = m.liked ? "true" : "false";
                card.dataset.favorited = m.favorited ? "true" : "false";
                const likeBtn = card.querySelector('.engage-btn[data-action="like"] .value');
                const favBtn = card.querySelector('.engage-btn[data-action="favorite"] .value');
                if (likeBtn) likeBtn.textContent = String(m.likes || 0);
                if (favBtn) favBtn.textContent = String(m.favorites || 0);
                setButtonState(card, "like", m.liked);
                setButtonState(card, "favorite", m.favorited);
                const tab = document.querySelector(".rank-tab.active");
                renderRankList((tab && tab.dataset.rankMode) || "hot");
                applyFiltersAndSort();
            } catch (e) {
                // ignore update failure
            } finally {
                button.disabled = false;
            }
        }

        document.addEventListener("DOMContentLoaded", function() {
            initTheme();
            const clientId = ensureClientId();

            const themeToggle = document.getElementById("themeToggle");
            if (themeToggle) {
                themeToggle.addEventListener("click", toggleTheme);
            }
            const themePreset = document.getElementById("themePreset");
            if (themePreset) {
                themePreset.addEventListener("change", function() {
                    const next = normalizeTheme(themePreset.value);
                    localStorage.setItem(THEME_KEY, next);
                    applyTheme(next);
                });
            }

            const refreshBtn = document.getElementById("homeRefresh");
            if (refreshBtn) {
                refreshBtn.addEventListener("click", function() {
                    window.location.reload();
                });
            }

            const search = document.getElementById("homeSearch");
            const status = document.getElementById("homeStatusFilter");
            const sort = document.getElementById("homeSortMode");
            [search, status, sort].forEach((el) => {
                if (!el) return;
                el.addEventListener("input", applyFiltersAndSort);
                el.addEventListener("change", applyFiltersAndSort);
            });

            document.querySelectorAll(".rank-tab").forEach((button) => {
                button.addEventListener("click", function() {
                    document.querySelectorAll(".rank-tab").forEach((item) => item.classList.remove("active"));
                    button.classList.add("active");
                    renderRankList(button.dataset.rankMode || "hot");
                });
            });

            document.querySelectorAll(".engage-btn").forEach((button) => {
                button.addEventListener("click", function(event) {
                    event.preventDefault();
                    event.stopPropagation();
                    toggleEngagement(button, clientId);
                });
            });

            document.querySelectorAll("#cardsGrid .doc-card").forEach((card) => {
                card.addEventListener("click", function(event) {
                    const target = event.target;
                    if (target && (target.closest("a") || target.closest("button"))) {
                        return;
                    }
                    const jobId = card.dataset.jobId || "";
                    if (!jobId) return;
                    window.open(`/docs/${jobId}`, "_blank", "noopener");
                });
            });

            applyFiltersAndSort();
            loadEngagementMetrics(clientId).finally(() => {
                renderRankList("hot");
            });
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
            right: 34px;
            top: 32px;
            transform: none;
            width: 68px;
            height: 68px;
            border: none;
            background: transparent;
            color: #7ea9ce;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            box-shadow: none;
            cursor: pointer;
            z-index: 125;
            transition: right 0.22s ease, color 0.14s ease, transform 0.14s ease;
        }

        .chat-drawer-toggle:hover {
            color: #5f8eb8;
            transform: scale(1.06);
        }

        .chat-drawer-toggle:focus-visible {
            outline: 2px solid #a8c3dc;
            outline-offset: 4px;
        }

        .chat-drawer-toggle svg {
            width: 42px;
            height: 42px;
            filter: drop-shadow(0 2px 4px rgba(71, 110, 145, 0.2));
        }

        body.chat-open .chat-drawer-toggle {
            opacity: 0;
            pointer-events: none;
        }

        .chat-panel-toggle {
            width: 34px;
            height: 34px;
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--primary);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius-sm);
            cursor: pointer;
            flex: 0 0 34px;
        }

        .chat-panel-toggle:hover {
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .chat-panel-toggle svg {
            width: 18px;
            height: 18px;
        }

        .chat-title-wrap {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            min-width: 0;
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
            color: var(--text);
        }

        .chat-bubble.user {
            background: #dfeeff;
            border-color: #9ec0e3;
            color: #17324d;
            margin-left: 26px;
        }

        .chat-bubble.assistant {
            background: #f7fafd;
            border-color: #ccd9e7;
            color: #1f2f42;
            margin-right: 26px;
        }

        .chat-bubble.assistant.streaming {
            background: #eaf3fe;
            border-color: #adc8e5;
            color: #294663;
            white-space: normal;
            padding: 10px 11px;
        }

        .chat-stream-status {
            font-size: 0.74rem;
            color: #4a6786;
            display: flex;
            align-items: center;
            gap: 7px;
            margin-bottom: 6px;
        }

        .chat-stream-status::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #6f9cc8;
            animation: chatPulse 1.1s ease-in-out infinite;
        }

        .chat-stream-content {
            min-height: 1.2em;
            white-space: pre-wrap;
        }

        .chat-stream-events {
            margin-bottom: 8px;
        }

        .chat-bubble.assistant.structured {
            white-space: normal;
            padding: 10px 11px;
        }

        .chat-event-block + .chat-event-block {
            margin-top: 8px;
        }

        .chat-event-details {
            border: 1px solid var(--line);
            border-radius: var(--radius-sm);
            background: var(--surface);
            overflow: hidden;
        }

        .chat-event-details[open] {
            background: #fbfdff;
        }

        .chat-event-summary {
            list-style: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 7px 9px;
            font-size: 0.74rem;
            font-weight: 600;
            color: #415b78;
            user-select: none;
        }

        .chat-event-summary::-webkit-details-marker {
            display: none;
        }

        .chat-event-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 1px solid transparent;
            flex: 0 0 auto;
        }

        .chat-event-icon svg {
            width: 14px;
            height: 14px;
        }

        .chat-event-brief {
            flex: 1 1 auto;
            min-width: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #345170;
        }

        .chat-event-duration {
            font-size: 0.69rem;
            color: #6e8298;
            font-weight: 600;
            font-variant-numeric: tabular-nums;
            flex: 0 0 auto;
        }

        .chat-event-state {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #8fa8bf;
            border: 1px solid transparent;
            flex: 0 0 auto;
        }

        .chat-event-state.neutral {
            background: #8fa8bf;
            border-color: #b5c4d3;
        }

        .chat-event-state.ok {
            background: #57b57f;
            border-color: #9cccb0;
        }

        .chat-event-state.error {
            background: #d56a6a;
            border-color: #ebb0b0;
        }

        .chat-event-state.running {
            background: #d1ad45;
            border-color: #e3d08e;
        }

        .chat-event-body {
            padding: 8px 9px 9px;
            border-top: 1px dashed var(--line);
        }

        .chat-event-io-title {
            font-size: 0.68rem;
            color: var(--muted);
            margin-bottom: 3px;
        }

        .chat-event-io {
            margin: 0 0 7px;
            padding: 6px 7px;
            border: 1px solid var(--line);
            border-radius: 4px;
            background: var(--surface-soft);
            color: var(--text);
            font-size: 0.72rem;
            line-height: 1.4;
            overflow-x: auto;
            white-space: pre-wrap;
        }

        .chat-event-content {
            font-size: 0.79rem;
            line-height: 1.5;
        }

        .chat-event-thinking .chat-event-icon {
            color: #6f4f00;
            background: #fff3cf;
            border-color: #e7d093;
        }

        .chat-event-tool .chat-event-icon {
            color: #204f78;
            background: #e7f3fe;
            border-color: #a6c7e3;
        }

        .chat-event-skill .chat-event-icon {
            color: #5c356f;
            background: #f2eaff;
            border-color: #ccb6e7;
        }

        .chat-event-content-block .chat-event-icon {
            color: #285931;
            background: #e8f8ed;
            border-color: #9acaa7;
        }

        @keyframes chatPulse {
            0% { transform: scale(0.85); opacity: 0.8; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.85); opacity: 0.8; }
        }

        @keyframes chatCursorBlink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }

        .chat-bubble.assistant.markdown {
            white-space: normal;
            line-height: 1.5;
        }

        .chat-bubble.assistant.markdown p {
            margin: 0 0 0.58rem;
        }

        .chat-bubble.assistant.markdown p:last-child {
            margin-bottom: 0;
        }

        .chat-bubble.assistant.markdown pre {
            margin: 0.5rem 0;
            padding: 8px;
            border: 1px solid var(--line);
            background: var(--surface);
            overflow-x: auto;
        }

        .chat-bubble.assistant.markdown code {
            font-family: "Courier New", Consolas, monospace;
            font-size: 0.85em;
            background: var(--surface-soft);
            border: 1px solid var(--line);
            padding: 0.08rem 0.3rem;
        }

        .chat-bubble.assistant.markdown pre code {
            border: none;
            padding: 0;
            background: transparent;
        }

        .chat-bubble.assistant.markdown ul,
        .chat-bubble.assistant.markdown ol {
            margin: 0.35rem 0 0.55rem 1.2rem;
            padding: 0;
        }

        .chat-bubble.assistant.markdown table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.5rem 0;
            font-size: 0.77rem;
        }

        .chat-bubble.assistant.markdown th,
        .chat-bubble.assistant.markdown td {
            border: 1px solid var(--line);
            padding: 4px 6px;
            vertical-align: top;
            text-align: left;
        }

        [data-theme="dark"] .chat-bubble.user {
            background: #244767;
            border-color: #4778a6;
            color: #e7f2ff;
        }

        [data-theme="dark"] .chat-bubble.assistant {
            background: #1b2a3d;
            border-color: #395170;
            color: #dbe7f5;
        }

        [data-theme="dark"] .chat-bubble.assistant.streaming {
            background: #21364d;
            border-color: #4f7298;
            color: #d7e9fb;
        }

        [data-theme="dark"] .chat-stream-status {
            color: #98bcde;
        }

        [data-theme="dark"] .chat-stream-status::before {
            background: #9ec8f1;
        }

        [data-theme="dark"] .chat-event-details {
            background: #162432;
            border-color: #354a63;
        }

        [data-theme="dark"] .chat-event-details[open] {
            background: #1b2c3d;
        }

        [data-theme="dark"] .chat-event-summary {
            color: #bdd6ee;
        }

        [data-theme="dark"] .chat-event-brief {
            color: #d2e4f5;
        }

        [data-theme="dark"] .chat-event-duration {
            color: #90aac3;
        }

        [data-theme="dark"] .chat-event-body {
            border-top-color: #38506a;
        }

        [data-theme="dark"] .chat-event-io {
            background: #132130;
            border-color: #35506a;
            color: #dbe8f6;
        }

        [data-theme="dark"] .chat-event-state.ok {
            background: #68c18e;
            border-color: #2f6f47;
        }

        [data-theme="dark"] .chat-event-state.error {
            background: #df7f7f;
            border-color: #7d3a3a;
        }

        [data-theme="dark"] .chat-event-state.running {
            background: #dfbe62;
            border-color: #7f6b31;
        }

        [data-theme="dark"] .chat-event-state.neutral {
            background: #7890a7;
            border-color: #4e647a;
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

        .repo-title {
            display: block;
            color: var(--primary);
            font-size: 1.34rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 10px;
            word-break: break-word;
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
            position: relative;
            cursor: zoom-in;
        }

        .mermaid-lightbox-overlay {
            position: fixed;
            inset: 0;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(14, 23, 35, 0.72);
            z-index: 2200;
            padding: 0;
        }

        .mermaid-lightbox-overlay.show {
            display: flex;
        }

        .mermaid-lightbox-panel {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            border: none;
            background: var(--surface);
            box-shadow: none;
        }

        .mermaid-lightbox-toolbar {
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 0 10px;
            border-bottom: 1px solid var(--line);
            background: var(--surface-soft);
            font-size: 0.8rem;
        }

        .mermaid-lightbox-toolbar strong {
            color: var(--text);
            font-size: 0.82rem;
        }

        .mermaid-lightbox-hint {
            color: var(--muted);
            font-size: 0.76rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .mermaid-lightbox-actions {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .mermaid-lightbox-btn {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            width: 30px;
            height: 30px;
            padding: 0;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .mermaid-lightbox-btn svg {
            width: 15px;
            height: 15px;
        }

        .mermaid-lightbox-btn:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .mermaid-lightbox-canvas {
            flex: 1;
            overflow: hidden;
            position: relative;
            background: var(--surface);
            cursor: grab;
        }

        .mermaid-lightbox-canvas.dragging {
            cursor: grabbing;
        }

        .mermaid-lightbox-content {
            position: absolute;
            left: 0;
            top: 0;
            transform-origin: 0 0;
            will-change: auto;
        }

        .mermaid-lightbox-content svg {
            max-width: none;
            shape-rendering: geometricPrecision;
            text-rendering: geometricPrecision;
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

            .chat-drawer-toggle {
                right: 18px;
                top: 18px;
                width: 58px;
                height: 58px;
            }

            .chat-drawer-toggle svg {
                width: 36px;
                height: 36px;
            }
        }
    </style>
</head>
<body>
    <div class="docs-shell">
        <nav class="sidebar">
            <a href="{{ docs_home_url or '/' }}" class="home-link">← 返回文档中心</a>
            <div class="repo-title">{{ docs_display_title or repo_name }}</div>
            <div class="sidebar-control">
                <label for="docsThemeSelect" class="sidebar-control-label">主题配色</label>
                <select id="docsThemeSelect" class="sidebar-control-input">
                    <option value="light">浅色蓝</option>
                    <option value="slate">雾蓝灰</option>
                    <option value="sage">清新绿</option>
                    <option value="dark">深色夜</option>
                </select>
            </div>

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

            {% if versions and versions|length > 0 %}
            <div class="sidebar-control">
                <label for="versionSelect" class="sidebar-control-label">版本</label>
                <select id="versionSelect" class="sidebar-control-input" {% if versions|length <= 1 %}disabled{% endif %}>
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

            {% if subproject_options and subproject_options|length > 1 %}
            <div class="sidebar-control">
                <label for="subprojectSelect" class="sidebar-control-label">子项目</label>
                <select id="subprojectSelect" class="sidebar-control-input">
                    {% for sp in subproject_options %}
                    <option value="{{ sp.key }}" data-job-id="{{ sp.job_id }}" {% if current_subproject_key == sp.key %}selected{% endif %}>{{ sp.label }}</option>
                    {% endfor %}
                </select>
            </div>
            {% elif current_subproject_label %}
            <div class="sidebar-control">
                <label class="sidebar-control-label">子项目</label>
                <div class="sidebar-control-readonly">{{ current_subproject_label }}</div>
            </div>
            {% endif %}

            {% if view_options and view_options|length > 1 %}
            <div class="sidebar-control">
                <label for="viewSelect" class="sidebar-control-label">文档视图</label>
                <select id="viewSelect" class="sidebar-control-input">
                    {% for v in view_options %}
                    <option value="{{ v.job_id }}" {% if current_view_job_id == v.job_id %}selected{% endif %}>{{ v.label }}</option>
                    {% endfor %}
                </select>
            </div>
            {% elif current_doc_type %}
            <div class="sidebar-control">
                <label class="sidebar-control-label">文档视图</label>
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
            <svg viewBox="0 0 96 96" fill="none" aria-hidden="true">
                <g stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M48 14v9"/>
                    <path d="M26 33h-5M75 33h-5"/>
                    <rect x="22" y="24" width="52" height="44" rx="15"/>
                    <path d="M32 44h12M52 44h12"/>
                    <path d="M34 57c3.7 4.4 8.4 6.6 14 6.6 5.6 0 10.3-2.2 14-6.6"/>
                    <path d="M36 74h24"/>
                </g>
                <circle cx="48" cy="10" r="4.4" fill="currentColor"/>
                <circle cx="38.8" cy="49.5" r="3.4" fill="currentColor"/>
                <circle cx="57.2" cy="49.5" r="3.4" fill="currentColor"/>
                <path d="M80.5 18.5l1.9 4.1 4.2 1.9-4.2 1.9-1.9 4.2-1.9-4.2-4.1-1.9 4.1-1.9 1.9-4.1z" fill="currentColor"/>
                <path d="M18.4 18.8l1.2 2.6 2.6 1.2-2.6 1.2-1.2 2.6-1.2-2.6-2.6-1.2 2.6-1.2 1.2-2.6z" fill="currentColor"/>
                <path d="M66.6 28.8l2.2 1.2v2.5l-2.2 1.2-2.2-1.2V30l2.2-1.2z" fill="currentColor" opacity="0.7"/>
                <path d="M29.4 28.8l2.2 1.2v2.5l-2.2 1.2-2.2-1.2V30l2.2-1.2z" fill="currentColor" opacity="0.7"/>
            </svg>
        </button>

        <aside
            class="chat-panel"
            data-chat-api="{{ chat_api_url }}"
            data-chat-stream-api="{{ chat_stream_api_url or '' }}"
            data-chat-session-api-base="{{ chat_session_api_base or '' }}"
            data-chat-protocol="{{ chat_protocol }}"
        >
            <div class="chat-header">
                <div class="chat-header-top">
                    <div class="chat-title-wrap">
                        <button id="chatPanelToggle" class="chat-panel-toggle" type="button" title="收起聊天助手" aria-label="收起聊天助手">
                            <svg viewBox="0 0 64 64" fill="none" aria-hidden="true">
                                <path d="M32 10v6" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                                <circle cx="32" cy="7" r="3.2" fill="currentColor"/>
                                <rect x="16" y="18" width="32" height="27" rx="8" stroke="currentColor" stroke-width="3"/>
                                <circle cx="25.5" cy="31" r="2.2" fill="currentColor"/>
                                <circle cx="38.5" cy="31" r="2.2" fill="currentColor"/>
                                <path d="M24.5 38.5c2.3 2 4.7 3 7.5 3s5.2-1 7.5-3" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            </svg>
                        </button>
                        <div class="chat-title">CodeWikiAgent</div>
                    </div>
                    <div class="chat-session-controls">
                        <select id="chatSessionSelect" class="chat-session-select"></select>
                        <button id="chatNewSessionBtn" class="chat-new-session" type="button">新建会话</button>
                    </div>
                </div>
                <div class="chat-subtitle">
                    可读取文档与代码目录；仅允许修改文档目录的 Markdown 文件，禁止修改代码。会话关闭后服务器仍会继续执行并可恢复。
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

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js"></script>
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

        const MERMAID_DEBUG =
            (new URLSearchParams(window.location.search).get("debugMermaid") === "1")
            || (window.localStorage.getItem("cw_debug_mermaid") === "1");
        const mermaidLog = (...args) => {
            if (MERMAID_DEBUG) console.log("[MermaidLB][content]", ...args);
        };

        const THEME_KEY = "codewiki_theme";
        const THEME_PRESETS = ["light", "slate", "sage", "dark"];

        function normalizeTheme(theme) {
            return THEME_PRESETS.includes(theme) ? theme : "light";
        }

        function applyTheme(theme) {
            const normalized = normalizeTheme(theme);
            document.documentElement.setAttribute("data-theme", normalized);
            const select = document.getElementById("docsThemeSelect");
            if (select && select.value !== normalized) {
                select.value = normalized;
            }
        }

        function initTheme() {
            const stored = normalizeTheme(localStorage.getItem(THEME_KEY) || "light");
            applyTheme(stored);
        }

        function createMermaidLightbox() {
            const overlay = document.createElement("div");
            overlay.className = "mermaid-lightbox-overlay";
            overlay.innerHTML = `
                <div class="mermaid-lightbox-panel" role="dialog" aria-modal="true" aria-label="Mermaid 独立视图">
                    <div class="mermaid-lightbox-toolbar">
                        <strong>Mermaid 独立视图</strong>
                        <span class="mermaid-lightbox-hint">滚轮缩放 · 拖动平移 · 双击复位</span>
                        <div class="mermaid-lightbox-actions">
                            <button type="button" class="mermaid-lightbox-btn" data-action="reset" title="复位" aria-label="复位">
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                    <path d="M20 12a8 8 0 1 1-2.3-5.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                                    <path d="M20 4v5.4h-5.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </button>
                            <button type="button" class="mermaid-lightbox-btn" data-action="close" title="关闭" aria-label="关闭">
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                    <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="mermaid-lightbox-canvas">
                        <div class="mermaid-lightbox-content"></div>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);

            const panel = overlay.querySelector(".mermaid-lightbox-panel");
            const canvas = overlay.querySelector(".mermaid-lightbox-canvas");
            const content = overlay.querySelector(".mermaid-lightbox-content");
            const closeBtn = overlay.querySelector('[data-action="close"]');
            const resetBtn = overlay.querySelector('[data-action="reset"]');

            const state = {
                open: false,
                dragging: false,
                scale: 1,
                x: 0,
                y: 0,
                startX: 0,
                startY: 0,
                sourceWidth: 0,
                sourceHeight: 0,
                currentSvg: null,
            };

            const clampScale = (value) => Math.max(0.2, Math.min(8, value));

            const apply = () => {
                content.style.transform = `translate(${state.x}px, ${state.y}px)`;
                if (state.currentSvg && state.sourceWidth > 0 && state.sourceHeight > 0) {
                    state.currentSvg.style.width = `${Math.max(1, state.sourceWidth * state.scale)}px`;
                    state.currentSvg.style.height = `${Math.max(1, state.sourceHeight * state.scale)}px`;
                }
            };

            const fitToCanvas = () => {
                const svg = state.currentSvg || content.querySelector("svg");
                if (!svg) return;

                let sourceWidth = 0;
                let sourceHeight = 0;
                const vb = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal : null;
                if (vb && vb.width && vb.height) {
                    sourceWidth = vb.width;
                    sourceHeight = vb.height;
                }
                if (!sourceWidth || !sourceHeight) {
                    const bbox = typeof svg.getBBox === "function" ? svg.getBBox() : null;
                    if (bbox && bbox.width && bbox.height) {
                        sourceWidth = bbox.width;
                        sourceHeight = bbox.height;
                    }
                }
                if (!sourceWidth || !sourceHeight) {
                    const rect = svg.getBoundingClientRect();
                    sourceWidth = rect.width || 1200;
                    sourceHeight = rect.height || 800;
                }

                state.sourceWidth = sourceWidth;
                state.sourceHeight = sourceHeight;

                const availW = Math.max(200, canvas.clientWidth - 48);
                const availH = Math.max(200, canvas.clientHeight - 48);
                state.scale = clampScale(Math.min(availW / sourceWidth, availH / sourceHeight, 1.2));
                state.x = Math.round((canvas.clientWidth - sourceWidth * state.scale) / 2);
                state.y = Math.round((canvas.clientHeight - sourceHeight * state.scale) / 2);
                apply();
            };

            const close = () => {
                state.open = false;
                state.dragging = false;
                overlay.classList.remove("show");
                canvas.classList.remove("dragging");
                content.innerHTML = "";
                state.currentSvg = null;
                state.sourceWidth = 0;
                state.sourceHeight = 0;
                mermaidLog("close");
            };

            const open = (sourceSvg) => {
                if (!sourceSvg) return;
                const clone = sourceSvg.cloneNode(true);
                clone.removeAttribute("style");
                clone.style.maxWidth = "none";
                clone.style.width = "";
                clone.style.height = "";
                clone.style.shapeRendering = "geometricPrecision";
                clone.style.textRendering = "geometricPrecision";
                content.innerHTML = "";
                content.appendChild(clone);
                state.currentSvg = clone;
                overlay.classList.add("show");
                state.open = true;
                state.dragging = false;
                canvas.classList.remove("dragging");
                window.requestAnimationFrame(fitToCanvas);
                mermaidLog("open", { sourceId: sourceSvg.id || "", width: sourceSvg.getAttribute("width") || "" });
            };

            closeBtn.addEventListener("click", close);
            resetBtn.addEventListener("click", fitToCanvas);
            overlay.addEventListener("click", (event) => {
                if (event.target === overlay) close();
            });

            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape" && state.open) {
                    close();
                }
            });

            canvas.addEventListener("dblclick", (event) => {
                if (!state.open) return;
                event.preventDefault();
                fitToCanvas();
            });

            canvas.addEventListener("wheel", (event) => {
                if (!state.open) return;
                event.preventDefault();
                const rect = canvas.getBoundingClientRect();
                const cx = event.clientX - rect.left;
                const cy = event.clientY - rect.top;
                const zoomFactor = event.deltaY < 0 ? 1.12 : 0.9;
                const nextScale = clampScale(state.scale * zoomFactor);
                const px = (cx - state.x) / state.scale;
                const py = (cy - state.y) / state.scale;
                state.scale = nextScale;
                state.x = cx - px * state.scale;
                state.y = cy - py * state.scale;
                apply();
            }, { passive: false });

            canvas.addEventListener("mousedown", (event) => {
                if (!state.open || event.button !== 0) return;
                event.preventDefault();
                state.dragging = true;
                state.startX = event.clientX - state.x;
                state.startY = event.clientY - state.y;
                canvas.classList.add("dragging");
            });

            window.addEventListener("mousemove", (event) => {
                if (!state.dragging) return;
                state.x = event.clientX - state.startX;
                state.y = event.clientY - state.startY;
                apply();
            });

            window.addEventListener("mouseup", () => {
                if (!state.dragging) return;
                state.dragging = false;
                canvas.classList.remove("dragging");
            });

            return { open };
        }

        function bindMermaidLightbox(container, lightbox) {
            if (!container || !lightbox || container.dataset.lightboxBound === "1") return;
            container.dataset.lightboxBound = "1";
            container.title = "双击打开独立视图";
            container.style.cursor = "zoom-in";
            container.addEventListener("dblclick", (event) => {
                event.preventDefault();
                event.stopPropagation();
                const svg = container.tagName && container.tagName.toLowerCase() === "svg"
                    ? container
                    : container.querySelector("svg");
                mermaidLog("dblclick(shell)", { hasSvg: Boolean(svg) });
                if (!svg) return;
                lightbox.open(svg);
            }, true);
        }

        function bindMermaidLightboxFromDocument(doc, lightbox) {
            if (!doc || !lightbox) return;
            const nodes = Array.from(doc.querySelectorAll(".mermaid, svg[id^='mermaid-']"));
            mermaidLog("bindFromDocument", { nodeCount: nodes.length });
            nodes.forEach((node) => {
                if (node.dataset.lightboxBoundParent === "1") return;
                node.dataset.lightboxBoundParent = "1";
                node.title = "双击打开独立视图";
                node.style.cursor = "zoom-in";
                node.addEventListener("dblclick", (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    const svg = node.tagName && node.tagName.toLowerCase() === "svg"
                        ? node
                        : node.querySelector("svg");
                    mermaidLog("dblclick(frame)", { hasSvg: Boolean(svg) });
                    if (!svg) return;
                    lightbox.open(svg);
                }, true);
            });
        }

        document.addEventListener("DOMContentLoaded", function() {
            initTheme();
            const mermaidLightbox = createMermaidLightbox();
            const docsThemeSelect = document.getElementById("docsThemeSelect");
            if (docsThemeSelect) {
                docsThemeSelect.addEventListener("change", function() {
                    const next = normalizeTheme(docsThemeSelect.value);
                    localStorage.setItem(THEME_KEY, next);
                    applyTheme(next);
                });
            }

            const docsFrame = document.getElementById("docsContentFrame");
            const frameMode = Boolean(docsFrame);
            mermaidLog("init", { frameMode: frameMode });
            const shellNavBase = "{{ shell_nav_base or ('/static-docs/' ~ (job_id or '')) }}";
            const contentNavBase = "{{ content_nav_base or (shell_nav_base or ('/static-docs/' ~ (job_id or ''))) }}";
            let currentPagePath = {{ (current_page or "overview.md")|tojson }};
            const navLinks = Array.from(document.querySelectorAll(".nav-link[data-page]"));
            const currentJobId = {{ (job_id or "")|tojson }};
            const currentSubprojectKey = {{ (current_subproject_key or "__root__")|tojson }};
            const currentViewJobId = {{ (current_view_job_id or job_id or "")|tojson }};
            const viewMatrix = {{ (view_matrix or {})|tojson }};

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

            const escapeOptionText = (value) => {
                return String(value || "")
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/\"/g, "&quot;")
                    .replace(/'/g, "&#39;");
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
            const subprojectSelect = document.getElementById("subprojectSelect");
            const navigateToVariantJob = (targetJobId) => {
                const safeJobId = String(targetJobId || currentJobId || "").trim();
                if (!safeJobId) return;
                const params = new URLSearchParams(window.location.search);
                params.delete("version");
                const query = params.toString();
                window.location.href = "/static-docs/" + encodeURIComponent(safeJobId) + "/overview.md" + (query ? ("?" + query) : "");
            };

            const populateViewSelect = (subKey, preferredJobId) => {
                if (!viewSelect) return "";
                const key = String(subKey || "");
                const views = Array.isArray(viewMatrix[key]) ? viewMatrix[key] : [];
                if (!views.length) {
                    viewSelect.innerHTML = "";
                    return "";
                }
                viewSelect.innerHTML = views.map(function(item) {
                    return `<option value="${escapeOptionText(item.job_id)}">${escapeOptionText(item.label || item.doc_type || "default")}</option>`;
                }).join("");
                const matched = views.find(function(item) { return item.job_id === preferredJobId; });
                const selectedJobId = (matched && matched.job_id) || views[0].job_id;
                viewSelect.value = selectedJobId;
                return selectedJobId;
            };

            if (subprojectSelect) {
                const initSubKey = subprojectSelect.value || currentSubprojectKey;
                if (viewSelect) {
                    populateViewSelect(initSubKey, currentViewJobId || currentJobId);
                }
                subprojectSelect.addEventListener("change", function() {
                    const selectedKey = subprojectSelect.value || "";
                    if (viewSelect) {
                        const targetJobId = populateViewSelect(selectedKey, "");
                        navigateToVariantJob(targetJobId);
                        return;
                    }
                    const selectedOption = subprojectSelect.selectedOptions && subprojectSelect.selectedOptions[0];
                    navigateToVariantJob(selectedOption ? selectedOption.getAttribute("data-job-id") : "");
                });
            }

            if (viewSelect) {
                if (!subprojectSelect) {
                    populateViewSelect(currentSubprojectKey, currentViewJobId || currentJobId);
                }
                viewSelect.addEventListener("change", function() {
                    const targetJobId = viewSelect.value || currentJobId;
                    navigateToVariantJob(targetJobId);
                });
            }

            setActiveNav(currentPagePath);

            if (!frameMode) {
                const mermaidNodes = Array.from(document.querySelectorAll(".mermaid"));
                mermaidLog("bindInline", { mermaidCount: mermaidNodes.length });
                mermaid.init(undefined, mermaidNodes);
                window.setTimeout(() => {
                    const bindNodes = Array.from(document.querySelectorAll(".mermaid, svg[id^='mermaid-']"));
                    mermaidLog("bindInline-afterRender", { nodeCount: bindNodes.length });
                    bindNodes.forEach((node) => bindMermaidLightbox(node, mermaidLightbox));
                }, 0);
            } else if (docsFrame) {
                const bindFromFrame = () => {
                    try {
                        mermaidLog("bindFromFrame-attempt");
                        bindMermaidLightboxFromDocument(docsFrame.contentDocument, mermaidLightbox);
                    } catch (e) {
                        mermaidLog("bindFromFrame-error", String(e));
                        // ignore frame access issues
                    }
                };
                docsFrame.addEventListener("load", () => {
                    // Mermaid render may finish slightly after iframe load.
                    window.setTimeout(bindFromFrame, 80);
                    window.setTimeout(bindFromFrame, 260);
                });
                window.setTimeout(bindFromFrame, 180);
            }

            const chatPanel = document.querySelector(".chat-panel");
            const chatDrawerToggle = document.getElementById("chatDrawerToggle");
            const chatPanelToggle = document.getElementById("chatPanelToggle");
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
            const streamApiUrl = chatPanel.getAttribute("data-chat-stream-api") || "";
            const sessionApiBase = chatPanel.getAttribute("data-chat-session-api-base") || "";
            const protocol = chatPanel.getAttribute("data-chat-protocol") || "a2ui-0.1";
            let chatStore = { activeSessionId: "", sessions: [] };
            let chatSessionPollTimer = null;

            const setDrawerState = (isOpen) => {
                document.body.classList.toggle("chat-open", Boolean(isOpen));
                if (chatDrawerToggle) {
                    chatDrawerToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
                    chatDrawerToggle.setAttribute("title", isOpen ? "收起聊天助手" : "打开聊天助手");
                    chatDrawerToggle.setAttribute("aria-label", isOpen ? "收起聊天助手" : "打开聊天助手");
                }
                if (chatPanelToggle) {
                    chatPanelToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
                    chatPanelToggle.setAttribute("title", isOpen ? "收起聊天助手" : "打开聊天助手");
                    chatPanelToggle.setAttribute("aria-label", isOpen ? "收起聊天助手" : "打开聊天助手");
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
            if (chatPanelToggle) {
                chatPanelToggle.addEventListener("click", function() {
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
                    serverRunning: false,
                    serverUpdatedAt: "",
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
                chatStore.sessions = chatStore.sessions.map(function(item) {
                    const session = item && typeof item === "object" ? item : createSession();
                    if (!Array.isArray(session.messages)) {
                        session.messages = [{ role: "assistant", content: greetingText }];
                    }
                    if (typeof session.serverSessionId !== "string") session.serverSessionId = "";
                    session.serverRunning = Boolean(session.serverRunning);
                    if (typeof session.serverUpdatedAt !== "string") session.serverUpdatedAt = "";
                    return session;
                });
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

            const getSessionApiUrl = (serverSessionId) => {
                const safe = String(serverSessionId || "").trim();
                if (!safe || !sessionApiBase) return "";
                return sessionApiBase + "/" + encodeURIComponent(safe);
            };

            const escapeHtml = (value) => {
                return String(value || "")
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/\"/g, "&quot;")
                    .replace(/'/g, "&#39;");
            };

            const renderMarkdown = (rawText) => {
                const text = String(rawText || "");
                if (window.marked && typeof window.marked.parse === "function") {
                    try {
                        const html = window.marked.parse(text, { breaks: true, gfm: true });
                        if (window.DOMPurify && typeof window.DOMPurify.sanitize === "function") {
                            return window.DOMPurify.sanitize(html);
                        }
                        return html;
                    } catch (e) {
                        return escapeHtml(text);
                    }
                }
                return escapeHtml(text);
            };

            const CHAT_EVENT_META = {
                thinking: {
                    className: "chat-event-thinking",
                    defaultCollapsed: true,
                    icon: `
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M12 3.3a6.9 6.9 0 0 0-4.9 11.8c.9.9 1.5 1.9 1.7 3.1h6.4c.2-1.2.8-2.2 1.7-3.1A6.9 6.9 0 0 0 12 3.3z" stroke="currentColor" stroke-width="1.7"/>
                            <path d="M9.7 21h4.6M10.3 18.8h3.4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                        </svg>
                    `,
                },
                tool: {
                    className: "chat-event-tool",
                    defaultCollapsed: true,
                    icon: `
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M13.5 5.2a4 4 0 0 0 4.9 4.9L11 17.6a2.3 2.3 0 0 1-3.3 0l-1.3-1.3a2.3 2.3 0 0 1 0-3.3l7.1-7.8z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
                            <path d="M14.8 9.2l-1.7 1.7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                        </svg>
                    `,
                },
                skill: {
                    className: "chat-event-skill",
                    defaultCollapsed: true,
                    icon: `
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M9.5 4.2h-2a2 2 0 0 0-2 2v2M14.5 4.2h2a2 2 0 0 1 2 2v2M14.5 19.8h2a2 2 0 0 0 2-2v-2M9.5 19.8h-2a2 2 0 0 1-2-2v-2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                            <rect x="9.1" y="9.1" width="5.8" height="5.8" rx="1.4" stroke="currentColor" stroke-width="1.7"/>
                        </svg>
                    `,
                },
                content: {
                    className: "chat-event-content-block",
                    defaultCollapsed: false,
                    icon: `
                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                            <path d="M5.5 6.5a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v6.9a2 2 0 0 1-2 2h-6l-3.8 3v-3h-.2a2 2 0 0 1-2-2V6.5z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>
                            <path d="M8.5 8.8h7M8.5 11.5h4.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>
                        </svg>
                    `,
                },
            };

            const toEpoch = (value) => {
                if (!value) return 0;
                const ms = Date.parse(String(value));
                return Number.isFinite(ms) ? ms : 0;
            };

            const formatDurationMs = (rawMs) => {
                const ms = Math.max(0, Number(rawMs) || 0);
                if (ms < 1000) return ms + " ms";
                const sec = ms / 1000;
                if (sec < 10) return sec.toFixed(2) + " s";
                if (sec < 100) return sec.toFixed(1) + " s";
                return Math.round(sec) + " s";
            };

            const normalizeAssistantEvents = (events, fallbackText, ensureContent = true) => {
                const list = Array.isArray(events)
                    ? events.filter(function(item) { return item && typeof item === "object"; })
                    : [];
                if (!list.length) {
                    return [{
                        type: "content",
                        title: "回答",
                        content: String(fallbackText || ""),
                        collapsed: false,
                        status: "ok",
                        duration_ms: 0
                    }];
                }
                const normalized = list.map(function(item) {
                    return {
                        type: String(item.type || "content").toLowerCase(),
                        title: String(item.title || ""),
                        content: String(item.content || ""),
                        input: String(item.input || ""),
                        tool_name: String(item.tool_name || ""),
                        status: String(item.status || ""),
                        collapsed: typeof item.collapsed === "boolean" ? item.collapsed : undefined,
                        timestamp: String(item.timestamp || ""),
                        started_at: String(item.started_at || item.timestamp || ""),
                        finished_at: String(item.finished_at || ""),
                        duration_ms: Number(item.duration_ms || 0),
                    };
                });
                const hasContent = normalized.some(function(item) { return item.type === "content"; });
                if (ensureContent && !hasContent && String(fallbackText || "").trim()) {
                    normalized.push({
                        type: "content",
                        title: "回答",
                        content: String(fallbackText || ""),
                        collapsed: false,
                        status: "ok",
                        duration_ms: 0
                    });
                }
                return normalized;
            };

            const deriveEventDuration = (event) => {
                if (Number.isFinite(event.duration_ms) && event.duration_ms > 0) {
                    return Math.max(0, Number(event.duration_ms));
                }
                const started = toEpoch(event.started_at || event.timestamp);
                if (!started) return 0;
                const status = String(event.status || "").toLowerCase();
                const end = toEpoch(event.finished_at) || (status === "running" ? Date.now() : started);
                return Math.max(0, end - started);
            };

            const buildEventBrief = (eventType, event) => {
                if (eventType === "tool") {
                    const explicit = String(event.tool_name || "").trim();
                    if (explicit) return explicit;
                    const title = String(event.title || "").trim();
                    const sepIdx = Math.max(title.lastIndexOf(":"), title.lastIndexOf("："));
                    if (sepIdx >= 0 && sepIdx + 1 < title.length) {
                        const maybeTool = title.slice(sepIdx + 1).trim();
                        if (maybeTool) return maybeTool;
                    }
                    return "shell";
                }

                let title = String(event.title || "");
                ["思考", "已启用技能", "工具调用", "回答", "块"].forEach(function(token) {
                    title = title.split(token).join("");
                });
                title = title.split(":").join(" ").split("：").join(" ").trim();
                if (title) return title;

                const line = String(event.content || "").split("\\n").find(function(part) {
                    return String(part || "").trim();
                }) || "";
                const normalized = String(line).trim();
                if (!normalized) return " ";
                return normalized.length > 48 ? normalized.slice(0, 48) + "…" : normalized;
            };

            const renderAssistantStructured = (events, fallbackText, ensureContent = true) => {
                const normalized = normalizeAssistantEvents(events, fallbackText, ensureContent);
                return normalized.map(function(event) {
                    const eventType = CHAT_EVENT_META[event.type] ? event.type : "content";
                    const meta = CHAT_EVENT_META[eventType];
                    const status = event.status ? event.status.toLowerCase() : "";
                    const collapsed = typeof event.collapsed === "boolean" ? event.collapsed : meta.defaultCollapsed;
                    const openAttr = collapsed ? "" : " open";
                    const statusClass = (
                        status === "ok" || status === "error" || status === "running"
                    ) ? status : "neutral";
                    const brief = buildEventBrief(eventType, event);
                    const durationText = formatDurationMs(deriveEventDuration(event));
                    const inputHtml = event.input
                        ? `<div class="chat-event-io-title">输入参数</div><pre class="chat-event-io">${escapeHtml(event.input)}</pre>`
                        : "";
                    const contentHtml = renderMarkdown(event.content || "");
                    return `
                        <div class="chat-event-block ${meta.className}">
                            <details class="chat-event-details" ${openAttr}>
                                <summary class="chat-event-summary">
                                    <span class="chat-event-icon">${meta.icon}</span>
                                    <span class="chat-event-brief">${escapeHtml(brief)}</span>
                                    <span class="chat-event-duration">${durationText}</span>
                                    <span class="chat-event-state ${statusClass}"></span>
                                </summary>
                                <div class="chat-event-body">
                                    ${inputHtml}
                                    <div class="chat-event-content">${contentHtml}</div>
                                </div>
                            </details>
                        </div>
                    `;
                }).join("");
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
                    if (msg.role === "assistant") {
                        if (Array.isArray(msg.events) && msg.events.length) {
                            bubble.classList.add("structured");
                            bubble.innerHTML = renderAssistantStructured(msg.events, msg.content || "");
                        } else {
                            bubble.classList.add("markdown");
                            bubble.innerHTML = renderMarkdown(msg.content || "");
                        }
                    } else {
                        bubble.textContent = String(msg.content || "");
                    }
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
                syncOneSessionFromServer(target, { render: true }).finally(refreshChatSessionPolling);
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

            const commitAssistantMessage = (text, events, opts = {}) => {
                const options = opts || {};
                const session = getActiveSession();
                if (!session) return;
                if (!Array.isArray(session.messages)) {
                    session.messages = [];
                }
                session.messages.push({
                    role: "assistant",
                    content: text || "",
                    events: Array.isArray(events) ? events : []
                });
                if (!options.keepRunning) {
                    session.serverRunning = false;
                }
                session.updatedAt = nowText();
                persistChatStore();
            };

            const normalizeServerMessages = (messages) => {
                if (!Array.isArray(messages)) return [];
                return messages
                    .filter(function(item) { return item && typeof item === "object"; })
                    .map(function(item) {
                        return {
                            role: String(item.role || "assistant").toLowerCase() === "user" ? "user" : "assistant",
                            content: String(item.content || ""),
                            events: Array.isArray(item.events) ? item.events : [],
                        };
                    });
            };

            const mergeSessionMessagesFromServer = (session, messages) => {
                if (!session) return false;
                const incoming = normalizeServerMessages(messages);
                if (!incoming.length) return false;

                const local = Array.isArray(session.messages) ? session.messages : [];
                const signature = (msg) => `${msg.role || ""}::${msg.content || ""}`;
                const localSig = local.map(signature).join("|");
                const incomingSig = incoming.map(signature).join("|");
                if (localSig === incomingSig) return false;

                // Prefer server history as source-of-truth when it has new content.
                const shouldReplace = incoming.length >= local.length || !local.length;
                if (shouldReplace) {
                    session.messages = incoming;
                    session.updatedAt = nowText();
                    return true;
                }
                return false;
            };

            const syncOneSessionFromServer = async (session, opts = {}) => {
                const options = opts || {};
                if (!session || !session.serverSessionId) return false;
                const url = getSessionApiUrl(session.serverSessionId);
                if (!url) return false;
                try {
                    const response = await fetch(url, { method: "GET" });
                    if (!response.ok) {
                        if (response.status === 404) return false;
                        throw new Error("HTTP " + response.status);
                    }
                    const data = await response.json();
                    if (!data || typeof data !== "object") return false;

                    let changed = false;
                    if (typeof data.session_id === "string" && data.session_id && session.serverSessionId !== data.session_id) {
                        session.serverSessionId = data.session_id;
                        changed = true;
                    }
                    const running = String(data.status || "").toLowerCase() === "running";
                    if (Boolean(session.serverRunning) !== running) {
                        session.serverRunning = running;
                        changed = true;
                    }
                    if (typeof data.updated_at === "string" && data.updated_at !== session.serverUpdatedAt) {
                        session.serverUpdatedAt = data.updated_at;
                        changed = true;
                    }
                    if (mergeSessionMessagesFromServer(session, data.messages)) {
                        changed = true;
                    }
                    if (changed) {
                        persistChatStore();
                        if (options.render !== false && session.id === chatStore.activeSessionId) {
                            renderActiveMessages();
                            renderSessionOptions();
                        }
                    }
                    return changed;
                } catch (error) {
                    console.warn("Failed to sync chat session from server", error);
                    return false;
                }
            };

            const syncAllSessionsFromServer = async (opts = {}) => {
                const sessions = Array.isArray(chatStore.sessions) ? chatStore.sessions : [];
                for (const session of sessions) {
                    if (!session || !session.serverSessionId) continue;
                    await syncOneSessionFromServer(session, opts);
                }
            };

            const refreshChatSessionPolling = () => {
                if (chatSessionPollTimer) {
                    window.clearInterval(chatSessionPollTimer);
                    chatSessionPollTimer = null;
                }
                const active = getActiveSession();
                if (!active || !active.serverSessionId) return;
                chatSessionPollTimer = window.setInterval(async function() {
                    const current = getActiveSession();
                    if (!current || !current.serverSessionId) return;
                    const changed = await syncOneSessionFromServer(current, { render: true });
                    if (!current.serverRunning && !changed) {
                        // Slow down by stopping when idle and no incremental updates.
                        window.clearInterval(chatSessionPollTimer);
                        chatSessionPollTimer = null;
                    }
                }, active.serverRunning ? 1800 : 3500);
            };

            const createStreamingAssistantBubble = () => {
                const bubble = document.createElement("div");
                bubble.className = "chat-bubble assistant streaming";
                bubble.innerHTML = `
                    <div class="chat-stream-status">正在思考...</div>
                    <div class="chat-stream-events"></div>
                    <div class="chat-stream-content"></div>
                `;
                const statusEl = bubble.querySelector(".chat-stream-status");
                const eventsEl = bubble.querySelector(".chat-stream-events");
                const contentEl = bubble.querySelector(".chat-stream-content");
                chatMessagesEl.appendChild(bubble);
                chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                return {
                    update(partialText) {
                        if (contentEl) contentEl.textContent = String(partialText || " ");
                        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                    },
                    setStatus(statusText) {
                        if (statusEl) statusEl.textContent = String(statusText || "处理中...");
                    },
                    renderEvents(events) {
                        if (!eventsEl) return;
                        const list = Array.isArray(events) ? events : [];
                        if (!list.length) {
                            eventsEl.innerHTML = "";
                            return;
                        }
                        eventsEl.innerHTML = renderAssistantStructured(list, "", false);
                        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                    },
                    finalize(finalText, events) {
                        bubble.classList.remove("streaming");
                        if (Array.isArray(events) && events.length) {
                            bubble.classList.add("structured");
                            bubble.innerHTML = renderAssistantStructured(events, finalText || "");
                        } else {
                            bubble.classList.add("markdown");
                            bubble.innerHTML = renderMarkdown(finalText || "");
                        }
                        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                    },
                    fail(errorText) {
                        bubble.classList.remove("streaming");
                        bubble.textContent = String(errorText || "请求失败");
                        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
                    }
                };
            };

            const createWaitingAnimator = (streamingBubble) => {
                const phases = [
                    "正在分析问题",
                    "正在检索文档",
                    "正在读取代码",
                    "正在整理回答"
                ];
                let tick = 0;
                const timer = window.setInterval(function() {
                    const phase = phases[Math.floor(tick / 4) % phases.length];
                    const dots = ".".repeat((tick % 3) + 1);
                    streamingBubble.setStatus(phase + dots);
                    tick += 1;
                }, 420);
                return function stop() {
                    window.clearInterval(timer);
                };
            };

            const streamTextLike = async (text, onUpdate) => {
                const fullText = String(text || "");
                if (!fullText) {
                    onUpdate("");
                    return;
                }
                let index = 0;
                while (index < fullText.length) {
                    const remain = fullText.length - index;
                    const step = remain > 1800 ? 36 : (remain > 900 ? 22 : (remain > 400 ? 12 : 6));
                    index = Math.min(fullText.length, index + step);
                    onUpdate(fullText.slice(0, index));
                    await new Promise((resolve) => setTimeout(resolve, 14));
                }
            };

            const parseSseFrame = (rawFrame) => {
                const frame = String(rawFrame || "").trim();
                if (!frame) return null;
                const lines = frame.split("\\n");
                let eventName = "message";
                const dataLines = [];
                lines.forEach(function(line) {
                    if (!line || line.startsWith(":")) return;
                    if (line.startsWith("event:")) {
                        eventName = line.slice(6).trim() || "message";
                        return;
                    }
                    if (line.startsWith("data:")) {
                        dataLines.push(line.slice(5).trimStart());
                    }
                });
                return {
                    event: eventName,
                    data: dataLines.join("\\n"),
                };
            };

            const consumeChatSse = async (url, payload, onEvent) => {
                const response = await fetch(url, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });
                if (!response.ok) {
                    const text = await response.text();
                    throw new Error("HTTP " + response.status + ": " + text);
                }
                if (!response.body || !response.body.getReader) {
                    throw new Error("SSE stream body is not readable");
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let buffer = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        buffer += decoder.decode();
                        break;
                    }
                    buffer += decoder.decode(value, { stream: true });
                    let sepIndex = buffer.indexOf("\\n\\n");
                    while (sepIndex >= 0) {
                        const rawFrame = buffer.slice(0, sepIndex);
                        buffer = buffer.slice(sepIndex + 2);
                        const frame = parseSseFrame(rawFrame);
                        if (frame) {
                            if (frame.event === "done") {
                                return;
                            }
                            if (frame.data) {
                                let payloadObj = null;
                                try {
                                    payloadObj = JSON.parse(frame.data);
                                } catch (e) {
                                    // ignore non-json frames
                                }
                                if (payloadObj) onEvent(payloadObj);
                            }
                        }
                        sepIndex = buffer.indexOf("\\n\\n");
                    }
                }

                const tail = parseSseFrame(buffer);
                if (tail && tail.event !== "done" && tail.data) {
                    try {
                        const payloadObj = JSON.parse(tail.data);
                        onEvent(payloadObj);
                    } catch (e) {
                        // ignore
                    }
                }
            };

            loadChatStore();
            renderSessionOptions();
            renderActiveMessages();
            syncAllSessionsFromServer({ render: true }).finally(refreshChatSessionPolling);

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
                refreshChatSessionPolling();
            });

            const sendChat = async () => {
                if (!apiUrl && !streamApiUrl) return;
                const session = getActiveSession();
                if (!session) return;

                const question = (chatInputEl.value || "").trim();
                if (!question) return;

                appendMessage("user", question);
                chatInputEl.value = "";
                session.serverRunning = true;
                persistChatStore();
                chatSendBtn.disabled = true;
                chatSessionSelectEl.disabled = true;
                chatNewSessionBtn.disabled = true;
                const streamingBubble = createStreamingAssistantBubble();
                const stopWaiting = createWaitingAnimator(streamingBubble);

                const payload = {
                    protocol: protocol,
                    session_id: session.serverSessionId || session.id,
                    message: question,
                    messages: (session.messages || []).slice(-12).map(function(item) {
                        return {
                            role: item.role || "",
                            content: item.content || ""
                        };
                    }),
                    current_page: currentPagePath || "overview.md",
                    version: "{{ current_version or '' }}",
                    lang: "{{ current_lang or '' }}"
                };

                try {
                    let answer = "No response";
                    let responseEvents = [];
                    const liveTraceEvents = [];

                    if (streamApiUrl) {
                        let finalResult = null;
                        await consumeChatSse(streamApiUrl, payload, function(packet) {
                            const packetType = String(packet && packet.type || "");
                            if (packetType === "session") {
                                if (packet.session_id) {
                                    session.serverSessionId = String(packet.session_id);
                                }
                                session.serverRunning = true;
                                return;
                            }
                            if (packetType === "heartbeat") {
                                return;
                            }
                            if (packetType === "trace.append") {
                                const idx = Math.max(0, Number(packet.index || 0));
                                liveTraceEvents[idx] = packet.event || {};
                                const visible = liveTraceEvents.filter(function(item) {
                                    return item && item.type && item.type !== "content";
                                });
                                streamingBubble.renderEvents(visible);
                                return;
                            }
                            if (packetType === "trace.update") {
                                const idx = Math.max(0, Number(packet.index || 0));
                                liveTraceEvents[idx] = packet.event || {};
                                const visible = liveTraceEvents.filter(function(item) {
                                    return item && item.type && item.type !== "content";
                                });
                                streamingBubble.renderEvents(visible);
                                return;
                            }
                            if (packetType === "result") {
                                finalResult = packet.data || {};
                                session.serverRunning = false;
                                return;
                            }
                            if (packetType === "error") {
                                session.serverRunning = false;
                                throw new Error(String(packet.message || "stream error"));
                            }
                        });

                        if (!finalResult) {
                            throw new Error("流式通道已结束，但未收到最终结果");
                        }
                        answer = (finalResult.output || (finalResult.messages && finalResult.messages[0] && finalResult.messages[0].content)) || "No response";
                        responseEvents = Array.isArray(finalResult.events) ? finalResult.events : [];
                        if (finalResult.session_id) {
                            session.serverSessionId = String(finalResult.session_id);
                        }
                        session.serverRunning = false;
                    } else {
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
                        answer = (data && (data.output || (data.messages && data.messages[0] && data.messages[0].content))) || "No response";
                        responseEvents = Array.isArray(data && data.events) ? data.events : [];
                        if (data && data.session_id) {
                            session.serverSessionId = data.session_id;
                        }
                        session.serverRunning = false;
                    }

                    stopWaiting();
                    await streamTextLike(answer, (partial) => streamingBubble.update(partial));
                    streamingBubble.finalize(answer, responseEvents);
                    commitAssistantMessage(answer, responseEvents);
                    persistChatStore();
                } catch (error) {
                    stopWaiting();
                    const message = "请求失败: " + (error && error.message ? error.message : String(error));
                    const busy = message.includes("仍在处理中") || message.toLowerCase().includes("busy");
                    session.serverRunning = busy;
                    streamingBubble.fail(message);
                    commitAssistantMessage(message, [{
                        type: "content",
                        title: "错误",
                        content: message,
                        collapsed: false,
                        status: "error"
                    }], { keepRunning: busy });
                } finally {
                    chatSendBtn.disabled = false;
                    chatSessionSelectEl.disabled = false;
                    chatNewSessionBtn.disabled = false;
                    refreshChatSessionPolling();
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
            position: relative;
            cursor: zoom-in;
        }

        .mermaid-lightbox-overlay {
            position: fixed;
            inset: 0;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(14, 23, 35, 0.72);
            z-index: 2200;
            padding: 0;
        }

        .mermaid-lightbox-overlay.show {
            display: flex;
        }

        .mermaid-lightbox-panel {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            border: none;
            background: var(--surface);
            box-shadow: none;
        }

        .mermaid-lightbox-toolbar {
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 0 10px;
            border-bottom: 1px solid var(--line);
            background: var(--surface-soft);
            font-size: 0.8rem;
        }

        .mermaid-lightbox-toolbar strong {
            color: var(--text);
            font-size: 0.82rem;
        }

        .mermaid-lightbox-hint {
            color: var(--muted);
            font-size: 0.76rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .mermaid-lightbox-actions {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .mermaid-lightbox-btn {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            width: 30px;
            height: 30px;
            padding: 0;
            border-radius: var(--radius-sm);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .mermaid-lightbox-btn svg {
            width: 15px;
            height: 15px;
        }

        .mermaid-lightbox-btn:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--primary-soft);
        }

        .mermaid-lightbox-canvas {
            flex: 1;
            overflow: hidden;
            position: relative;
            background: var(--surface);
            cursor: grab;
        }

        .mermaid-lightbox-canvas.dragging {
            cursor: grabbing;
        }

        .mermaid-lightbox-content {
            position: absolute;
            left: 0;
            top: 0;
            transform-origin: 0 0;
            will-change: auto;
        }

        .mermaid-lightbox-content svg {
            max-width: none;
            shape-rendering: geometricPrecision;
            text-rendering: geometricPrecision;
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

        const MERMAID_DEBUG =
            (new URLSearchParams(window.location.search).get("debugMermaid") === "1")
            || (window.localStorage.getItem("cw_debug_mermaid") === "1");
        const mermaidLog = (...args) => {
            if (MERMAID_DEBUG) console.log("[MermaidLB][content]", ...args);
        };

        function createMermaidLightbox() {
            const overlay = document.createElement("div");
            overlay.className = "mermaid-lightbox-overlay";
            overlay.innerHTML = `
                <div class="mermaid-lightbox-panel" role="dialog" aria-modal="true" aria-label="Mermaid 独立视图">
                    <div class="mermaid-lightbox-toolbar">
                        <strong>Mermaid 独立视图</strong>
                        <span class="mermaid-lightbox-hint">滚轮缩放 · 拖动平移 · 双击复位</span>
                        <div class="mermaid-lightbox-actions">
                            <button type="button" class="mermaid-lightbox-btn" data-action="reset" title="复位" aria-label="复位">
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                    <path d="M20 12a8 8 0 1 1-2.3-5.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                                    <path d="M20 4v5.4h-5.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </button>
                            <button type="button" class="mermaid-lightbox-btn" data-action="close" title="关闭" aria-label="关闭">
                                <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                    <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="mermaid-lightbox-canvas">
                        <div class="mermaid-lightbox-content"></div>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);

            const canvas = overlay.querySelector(".mermaid-lightbox-canvas");
            const content = overlay.querySelector(".mermaid-lightbox-content");
            const closeBtn = overlay.querySelector('[data-action="close"]');
            const resetBtn = overlay.querySelector('[data-action="reset"]');

            const state = {
                open: false,
                dragging: false,
                scale: 1,
                x: 0,
                y: 0,
                startX: 0,
                startY: 0,
                sourceWidth: 0,
                sourceHeight: 0,
                currentSvg: null,
            };

            const clampScale = (value) => Math.max(0.2, Math.min(8, value));

            const apply = () => {
                content.style.transform = `translate(${state.x}px, ${state.y}px)`;
                if (state.currentSvg && state.sourceWidth > 0 && state.sourceHeight > 0) {
                    state.currentSvg.style.width = `${Math.max(1, state.sourceWidth * state.scale)}px`;
                    state.currentSvg.style.height = `${Math.max(1, state.sourceHeight * state.scale)}px`;
                }
            };

            const fitToCanvas = () => {
                const svg = state.currentSvg || content.querySelector("svg");
                if (!svg) return;

                let sourceWidth = 0;
                let sourceHeight = 0;
                const vb = svg.viewBox && svg.viewBox.baseVal ? svg.viewBox.baseVal : null;
                if (vb && vb.width && vb.height) {
                    sourceWidth = vb.width;
                    sourceHeight = vb.height;
                }
                if (!sourceWidth || !sourceHeight) {
                    const bbox = typeof svg.getBBox === "function" ? svg.getBBox() : null;
                    if (bbox && bbox.width && bbox.height) {
                        sourceWidth = bbox.width;
                        sourceHeight = bbox.height;
                    }
                }
                if (!sourceWidth || !sourceHeight) {
                    const rect = svg.getBoundingClientRect();
                    sourceWidth = rect.width || 1200;
                    sourceHeight = rect.height || 800;
                }

                state.sourceWidth = sourceWidth;
                state.sourceHeight = sourceHeight;

                const availW = Math.max(200, canvas.clientWidth - 48);
                const availH = Math.max(200, canvas.clientHeight - 48);
                state.scale = clampScale(Math.min(availW / sourceWidth, availH / sourceHeight, 1.2));
                state.x = Math.round((canvas.clientWidth - sourceWidth * state.scale) / 2);
                state.y = Math.round((canvas.clientHeight - sourceHeight * state.scale) / 2);
                apply();
            };

            const close = () => {
                state.open = false;
                state.dragging = false;
                overlay.classList.remove("show");
                canvas.classList.remove("dragging");
                content.innerHTML = "";
                state.currentSvg = null;
                state.sourceWidth = 0;
                state.sourceHeight = 0;
                mermaidLog("close");
            };

            const open = (sourceSvg) => {
                if (!sourceSvg) return;
                const clone = sourceSvg.cloneNode(true);
                clone.removeAttribute("style");
                clone.style.maxWidth = "none";
                clone.style.width = "";
                clone.style.height = "";
                clone.style.shapeRendering = "geometricPrecision";
                clone.style.textRendering = "geometricPrecision";
                content.innerHTML = "";
                content.appendChild(clone);
                state.currentSvg = clone;
                overlay.classList.add("show");
                state.open = true;
                state.dragging = false;
                canvas.classList.remove("dragging");
                window.requestAnimationFrame(fitToCanvas);
                mermaidLog("open", { sourceId: sourceSvg.id || "" });
            };

            closeBtn.addEventListener("click", close);
            resetBtn.addEventListener("click", fitToCanvas);
            overlay.addEventListener("click", (event) => {
                if (event.target === overlay) close();
            });

            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape" && state.open) {
                    close();
                }
            });

            canvas.addEventListener("dblclick", (event) => {
                if (!state.open) return;
                event.preventDefault();
                fitToCanvas();
            });

            canvas.addEventListener("wheel", (event) => {
                if (!state.open) return;
                event.preventDefault();
                const rect = canvas.getBoundingClientRect();
                const cx = event.clientX - rect.left;
                const cy = event.clientY - rect.top;
                const zoomFactor = event.deltaY < 0 ? 1.12 : 0.9;
                const nextScale = clampScale(state.scale * zoomFactor);
                const px = (cx - state.x) / state.scale;
                const py = (cy - state.y) / state.scale;
                state.scale = nextScale;
                state.x = cx - px * state.scale;
                state.y = cy - py * state.scale;
                apply();
            }, { passive: false });

            canvas.addEventListener("mousedown", (event) => {
                if (!state.open || event.button !== 0) return;
                event.preventDefault();
                state.dragging = true;
                state.startX = event.clientX - state.x;
                state.startY = event.clientY - state.y;
                canvas.classList.add("dragging");
            });

            window.addEventListener("mousemove", (event) => {
                if (!state.dragging) return;
                state.x = event.clientX - state.startX;
                state.y = event.clientY - state.startY;
                apply();
            });

            window.addEventListener("mouseup", () => {
                if (!state.dragging) return;
                state.dragging = false;
                canvas.classList.remove("dragging");
            });

            return { open };
        }

        function bindMermaidLightbox(container, lightbox) {
            if (!container || !lightbox || container.dataset.lightboxBound === "1") return;
            container.dataset.lightboxBound = "1";
            container.title = "双击打开独立视图";
            container.style.cursor = "zoom-in";
            container.addEventListener("dblclick", (event) => {
                event.preventDefault();
                event.stopPropagation();
                const svg = container.tagName && container.tagName.toLowerCase() === "svg"
                    ? container
                    : container.querySelector("svg");
                mermaidLog("dblclick(content)", { hasSvg: Boolean(svg) });
                if (!svg) return;
                lightbox.open(svg);
            }, true);
        }

        document.addEventListener("DOMContentLoaded", function() {
            const mermaidNodes = Array.from(document.querySelectorAll(".mermaid"));
            mermaidLog("init", { mermaidCount: mermaidNodes.length });
            mermaid.init(undefined, mermaidNodes);
            if (window.self !== window.top) {
                mermaidLog("skip-lightbox-in-iframe");
                return;
            }
            const lightbox = createMermaidLightbox();
            window.setTimeout(() => {
                const bindNodes = Array.from(document.querySelectorAll(".mermaid, svg[id^='mermaid-']"));
                mermaidLog("bind-afterRender", { nodeCount: bindNodes.length });
                bindNodes.forEach((node) => bindMermaidLightbox(node, lightbox));
            }, 0);
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
            max-width: 1580px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .topbar {
            min-height: 90px;
            padding: 16px 20px;
        }

        .console-hint {
            flex: 1;
            text-align: center;
            color: var(--muted);
            font-size: 0.9rem;
            padding: 0 16px;
        }

        .console-tabs {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin-bottom: 12px;
        }

        .admin-nav-btn {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--text);
            text-align: center;
            padding: 9px 12px;
            font-size: 0.86rem;
            font-weight: 600;
            border-radius: var(--radius-sm);
            cursor: pointer;
        }

        .admin-nav-btn:hover {
            color: var(--primary);
            border-color: var(--line-strong);
            background: var(--surface-soft);
        }

        .admin-nav-btn.active {
            color: #fff;
            border-color: var(--primary);
            background: var(--primary);
        }

        .console-body {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            min-height: calc(100vh - 166px);
        }

        .admin-panel {
            display: none;
            overflow: auto;
            margin-bottom: 0;
        }

        .admin-panel.active {
            display: block;
        }

        .panel-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }

        .panel-head h2 {
            margin: 0;
            font-size: 1.12rem;
        }

        .panel-desc {
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }

        .stat {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            padding: 10px 12px;
            border-radius: var(--radius-sm);
        }

        .stat .value {
            font-size: 1.22rem;
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

        .form-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }

        .form-grid-2 {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }

        .actions-row {
            display: flex;
            justify-content: flex-end;
            gap: 8px;
            margin-top: 8px;
        }

        .panel-head-tight {
            margin-top: 2px;
            margin-bottom: 10px;
            align-items: center;
        }

        .panel-head-tight h3 {
            font-size: 0.95rem;
            color: var(--text);
        }

        .doc-type-actions {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }

        .options-details {
            margin-bottom: 12px;
            border: 1px solid var(--line);
            background: var(--surface-soft);
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

        .label-with-help {
            display: inline-flex !important;
            align-items: center;
            gap: 6px;
        }

        .field-help-btn {
            width: 16px;
            height: 16px;
            border: 1px solid var(--line-strong);
            border-radius: 4px;
            background: var(--surface);
            color: var(--primary);
            font-size: 11px;
            font-weight: 700;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            cursor: pointer;
        }

        .field-help-btn:hover {
            background: var(--primary-soft);
            border-color: var(--primary);
        }

        .field-help-modal {
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.42);
            z-index: 1200;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .field-help-modal.open {
            display: flex;
        }

        .field-help-dialog {
            width: min(680px, 92vw);
            max-height: 78vh;
            overflow: auto;
            border: 1px solid var(--line);
            background: var(--surface);
            border-radius: var(--radius-sm);
            box-shadow: 0 18px 46px rgba(15, 23, 42, 0.16);
        }

        .field-help-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 14px;
            border-bottom: 1px solid var(--line);
            background: var(--surface-soft);
        }

        .field-help-title {
            margin: 0;
            font-size: 1rem;
            color: var(--text);
        }

        .field-help-close {
            border: 1px solid var(--line);
            background: var(--surface);
            color: var(--muted);
            min-width: 28px;
            height: 28px;
            padding: 0 6px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-size: 1rem;
            line-height: 1;
        }

        .field-help-close:hover {
            color: var(--text);
            border-color: var(--line-strong);
            background: var(--surface-soft);
        }

        .field-help-body {
            padding: 14px;
            color: var(--text);
            font-size: 0.88rem;
            line-height: 1.6;
        }

        .field-help-desc {
            margin: 0 0 10px 0;
            color: var(--text);
            white-space: pre-line;
        }

        .field-help-subtitle {
            margin: 0 0 6px 0;
            color: var(--muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .field-help-examples {
            margin: 0;
            padding-left: 18px;
        }

        .field-help-examples li + li {
            margin-top: 6px;
        }

        .agent-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-top: 10px;
        }

        .agent-item {
            border: 1px solid var(--line);
            background: var(--surface-soft);
            padding: 10px;
            border-radius: var(--radius-sm);
        }

        .agent-item h4 {
            font-size: 0.78rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .agent-item p {
            font-size: 0.86rem;
            color: var(--text);
            word-break: break-word;
            line-height: 1.45;
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

        .input-with-action {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .input-with-action input {
            flex: 1;
            min-width: 0;
        }

        .input-with-action .btn {
            flex: 0 0 auto;
            white-space: nowrap;
        }

        .output-generate-btn {
            width: 34px;
            height: 34px;
            padding: 0;
        }

        .output-generate-btn svg {
            width: 16px;
            height: 16px;
        }

        .table-wrap {
            overflow: auto;
            border: 1px solid var(--line);
            border-radius: var(--radius-sm);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 960px;
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

        [data-theme="dark"] .status.completed {
            color: #8ee3b4;
            border-color: #2a7b52;
            background: #143325;
        }

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
            .console-tabs {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

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

            .topbar {
                flex-wrap: wrap;
                min-height: auto;
            }

            .console-hint {
                order: 3;
                width: 100%;
                text-align: left;
                padding: 0;
            }

            .console-tabs,
            .form-grid,
            .form-grid-2,
            .options-grid,
            .agent-grid,
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
                <select id="themePreset" class="theme-select" aria-label="主题配色">
                    <option value="light">浅色蓝</option>
                    <option value="slate">雾蓝灰</option>
                    <option value="sage">清新绿</option>
                    <option value="dark">深色夜</option>
                </select>
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

        <div class="console-tabs">
            <button type="button" class="admin-nav-btn active" data-admin-panel="panel-stats">任务概览</button>
            <button type="button" class="admin-nav-btn" data-admin-panel="panel-create">新建任务</button>
            <button type="button" class="admin-nav-btn" data-admin-panel="panel-doc-types">文档模板设置</button>
            <button type="button" class="admin-nav-btn" data-admin-panel="panel-agent">Agent 设置</button>
        </div>

        <section class="console-body">
            <section class="panel admin-panel active" id="panel-stats">
                <div class="panel-head">
                    <h2>任务概览</h2>
                    <div class="panel-desc">任务并行执行: {{ task_concurrency }} / {{ task_concurrency_max }}</div>
                </div>
                <div class="stats">
                    <div class="stat queued">
                        <div class="value" id="statQueued">{{ queued_count }}</div>
                        <div class="label">Queued</div>
                    </div>
                    <div class="stat processing">
                        <div class="value" id="statProcessing">{{ processing_count }}</div>
                        <div class="label">Processing</div>
                    </div>
                    <div class="stat completed">
                        <div class="value" id="statCompleted">{{ completed_count }}</div>
                        <div class="label">Completed</div>
                    </div>
                    <div class="stat failed">
                        <div class="value" id="statFailed">{{ failed_count }}</div>
                        <div class="label">Failed</div>
                    </div>
                </div>

                <div class="panel-head" style="margin-top:14px;">
                    <h2>全部任务 ({{ total_count }})</h2>
                    <div class="panel-desc">支持状态筛选、日志查看、参数回填重新生成。</div>
                </div>

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

                {% if jobs and jobs|length > 0 %}
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
                                data-search="{{ (job.display_title or job.title or '') ~ ' ' ~ job.repo_url ~ ' ' ~ job.job_id ~ ' ' ~ (job.progress or '') ~ ' ' ~ ((job.options.subproject_name if job.options and job.options.subproject_name else '') ) ~ ' ' ~ ((job.options.subproject_path if job.options and job.options.subproject_path else '') ) }}"
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
                                    <div class="task-title">{{ job.display_title or job.title or job.repo_url }}</div>
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

            <section class="panel admin-panel" id="panel-create">
                <div class="panel-head">
                    <h2>创建新任务</h2>
                    <div class="panel-desc">支持 monorepo 子项目与文档类型模板参数绑定。</div>
                </div>

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
                        <div class="field">
                            <label for="doc_type">文档类型</label>
                            <select id="doc_type" name="doc_type">
                                <option value="">默认</option>
                                {% for option in doc_type_options %}
                                <option value="{{ option.name }}">{{ option.name }}{% if option.display_name %} - {{ option.display_name }}{% endif %}{% if option.built_in %} (内置){% endif %}</option>
                                {% endfor %}
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
                                <div class="input-with-action">
                                    <input type="text" id="output" name="output" placeholder="docs/codewiki">
                                    <button class="btn icon-btn output-generate-btn" type="button" id="generateOutputPathBtn" title="生成输出目录" aria-label="生成输出目录">
                                        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                            <path d="M20 12a8 8 0 1 1-2.3-5.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                                            <path d="M20 4v5.4h-5.4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </button>
                                </div>
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
                                <input type="text" id="focus" name="focus" placeholder="pkg/api,pkg/service">
                            </div>
                            <div class="field">
                                <label for="instructions">附加指令</label>
                                <textarea id="instructions" name="instructions" rows="4" placeholder="补充给模型的生成约束..."></textarea>
                            </div>
                            <div class="field">
                                <label for="skills">Skills</label>
                                <input type="text" id="skills" name="skills" placeholder="skill-a,skill-b">
                            </div>
                            <div class="field">
                                <label for="custom_cli_args">自定义 CLI 参数</label>
                                <input type="text" id="custom_cli_args" name="custom_cli_args" placeholder="例如: -v --max-depth 4">
                            </div>
                            <div class="check-field">
                                <input type="checkbox" id="create_branch" name="create_branch">
                                <label for="create_branch">生成后创建分支</label>
                            </div>
                            <div class="check-field">
                                <input type="checkbox" id="github_pages" name="github_pages">
                                <label for="github_pages">生成 GitHub Pages 页面</label>
                            </div>
                            <div class="check-field">
                                <input type="checkbox" id="no_cache" name="no_cache">
                                <label for="no_cache">禁用缓存</label>
                            </div>
                        </div>
                    </details>

                    <div class="actions-row">
                        <button class="btn btn-primary" type="submit">提交任务</button>
                    </div>
                </form>
            </section>

            <section class="panel admin-panel" id="panel-doc-types">
                <div class="panel-head">
                    <h2>文档模板设置</h2>
                    <div class="panel-desc">定义不同文档类型的结构重点与指令，并在任务中通过 <code>doc_type</code> 选择。</div>
                </div>

                <form method="POST" action="/admin/doc-types" id="docTypeForm">
                    <div class="panel-head panel-head-tight">
                        <h3 id="docTypeFormTitle">创建模板</h3>
                        <div class="panel-desc" id="docTypeFormDesc">填写模板信息后保存；可通过下方表格快速编辑或复制。</div>
                    </div>
                    <div class="options-grid" style="padding:0;">
                        <div class="field">
                            <label for="profile_doc_type">文档类型 Key</label>
                            <input id="profile_doc_type" name="doc_type" type="text" required placeholder="例如: architecture">
                        </div>
                        <div class="field">
                            <label for="profile_display_name">显示名称</label>
                            <input id="profile_display_name" name="display_name" type="text" placeholder="例如: Architecture View">
                        </div>
                        <div class="field">
                            <label for="profile_description">描述</label>
                            <input id="profile_description" name="description" type="text" placeholder="例如: 面向架构师的模块设计视图">
                        </div>
                        <div class="field" style="grid-column: 1 / -1;">
                            <label for="profile_prompt">模板 Prompt</label>
                            <textarea id="profile_prompt" name="prompt" rows="5" placeholder="填写文档类型专属提示词..."></textarea>
                        </div>
                        <div class="field">
                            <label for="profile_include">include_patterns</label>
                            <input id="profile_include" name="include" type="text" placeholder="*.go,*.proto">
                        </div>
                        <div class="field">
                            <label for="profile_exclude">exclude_patterns</label>
                            <input id="profile_exclude" name="exclude" type="text" placeholder="*test*">
                        </div>
                        <div class="field">
                            <label for="profile_focus">focus_modules</label>
                            <input id="profile_focus" name="focus" type="text" placeholder="pkg/api,pkg/service">
                        </div>
                        <div class="field">
                            <label for="profile_skills">skills</label>
                            <input id="profile_skills" name="skills" type="text" placeholder="skill-a,skill-b">
                        </div>
                        <div class="field">
                            <label for="profile_max_tokens">max_tokens</label>
                            <input id="profile_max_tokens" name="max_tokens" type="number" placeholder="可选">
                        </div>
                        <div class="field">
                            <label for="profile_max_token_per_module">max_token_per_module</label>
                            <input id="profile_max_token_per_module" name="max_token_per_module" type="number" placeholder="可选">
                        </div>
                        <div class="field">
                            <label for="profile_max_token_per_leaf_module">max_token_per_leaf_module</label>
                            <input id="profile_max_token_per_leaf_module" name="max_token_per_leaf_module" type="number" placeholder="可选">
                        </div>
                        <div class="field">
                            <label for="profile_max_depth">max_depth</label>
                            <input id="profile_max_depth" name="max_depth" type="number" placeholder="可选">
                        </div>
                        <div class="field">
                            <label for="profile_concurrency">concurrency</label>
                            <input id="profile_concurrency" name="profile_concurrency" type="number" placeholder="可选">
                        </div>
                    </div>
                    <div class="actions-row">
                        <button class="btn" type="button" id="docTypeResetBtn">重置</button>
                        <button class="btn btn-primary" type="submit" id="docTypeSubmitBtn">保存模板</button>
                    </div>
                </form>

                {% if doc_type_options and doc_type_options|length > 0 %}
                <div style="margin-top: 14px; border-top: 1px solid var(--line); padding-top: 12px;">
                    <h3 style="font-size:0.94rem; margin-bottom:8px;">当前文档类型</h3>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>key</th>
                                    <th>显示名</th>
                                    <th>说明</th>
                                    <th>类型</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for option in doc_type_options %}
                                <tr>
                                    <td>{{ option.name }}</td>
                                    <td>{{ option.display_name or '-' }}</td>
                                    <td>{{ option.description or '-' }}</td>
                                    <td>{% if option.built_in %}Built-in{% else %}Custom{% endif %}</td>
                                    <td>
                                        <div class="doc-type-actions">
                                            <button
                                                type="button"
                                                class="btn doc-type-edit-btn"
                                                data-profile="{{ option|tojson|forceescape }}"
                                                title="编辑模板"
                                            >
                                                编辑
                                            </button>
                                            <button
                                                type="button"
                                                class="btn doc-type-copy-btn"
                                                data-profile="{{ option|tojson|forceescape }}"
                                                title="复制模板"
                                            >
                                                复制
                                            </button>
                                            {% if not option.built_in %}
                                            <button
                                                type="button"
                                                class="btn btn-danger doc-type-delete-btn"
                                                data-doc-type="{{ option.name }}"
                                                title="删除模板"
                                            >
                                                删除
                                            </button>
                                            {% endif %}
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endif %}
                <form method="POST" action="/admin/doc-types/delete" id="docTypeDeleteInlineForm" style="display:none;">
                    <input type="hidden" name="doc_type" id="docTypeDeleteInlineInput" value="">
                </form>
            </section>

            <section class="panel admin-panel" id="panel-agent">
                <div class="panel-head">
                    <h2>Agent 设置</h2>
                    <div class="panel-desc">当前运行时 Agent 配置来自环境变量，可在 <code>docker/.env</code> 调整后重启服务。</div>
                </div>
                <div class="agent-grid">
                    <div class="agent-item">
                        <h4>模型 Base URL</h4>
                        <p>{{ agent_base_url or "未配置" }}</p>
                    </div>
                    <div class="agent-item">
                        <h4>模型列表（Fallback 顺序）</h4>
                        <p>{{ agent_models or "未配置" }}</p>
                    </div>
                    <div class="agent-item">
                        <h4>API Key 状态</h4>
                        <p>{% if agent_api_key_set %}已配置{% else %}未配置{% endif %}</p>
                    </div>
                    <div class="agent-item">
                        <h4>建议</h4>
                        <p>建议先配置 <code>AGENT_MODEL_API_KEY</code>、<code>AGENT_MODEL_BASE_URL</code>、<code>AGENT_MODEL_NAMES</code>，再在任务中启用对应模板与技能。</p>
                    </div>
                </div>
            </section>

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

        <div id="fieldHelpModal" class="field-help-modal" aria-hidden="true">
            <div class="field-help-dialog" role="dialog" aria-modal="true" aria-labelledby="fieldHelpTitle">
                <div class="field-help-head">
                    <h3 class="field-help-title" id="fieldHelpTitle">参数说明</h3>
                    <button type="button" id="fieldHelpCloseBtn" class="field-help-close" aria-label="关闭">×</button>
                </div>
                <div class="field-help-body">
                    <p id="fieldHelpDesc" class="field-help-desc">暂无说明。</p>
                    <div>
                        <div class="field-help-subtitle">示例</div>
                        <ul id="fieldHelpExamples" class="field-help-examples"></ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ADVANCED_STORAGE_KEY = "codewiki_admin_advanced_options";
        const ADMIN_PANEL_STORAGE_KEY = "codewiki_admin_active_panel";
        const THEME_KEY = "codewiki_theme";
        const THEME_PRESETS = ["light", "slate", "sage", "dark"];
        const THEME_LABELS = {
            light: "浅色蓝",
            slate: "雾蓝灰",
            sage: "清新绿",
            dark: "深色夜",
        };
        let currentLogJobId = "";
        let logAutoRefreshTimer = null;
        let logAutoRefreshEnabled = false;

        function normalizeTheme(theme) {
            return THEME_PRESETS.includes(theme) ? theme : "light";
        }

        function applyTheme(theme) {
            const normalized = normalizeTheme(theme);
            document.documentElement.setAttribute("data-theme", normalized);
            const select = document.getElementById("themePreset");
            if (select && select.value !== normalized) {
                select.value = normalized;
            }
            const btn = document.getElementById("themeToggle");
            if (btn) {
                const index = THEME_PRESETS.indexOf(normalized);
                const next = THEME_PRESETS[(index + 1) % THEME_PRESETS.length];
                const nextLabel = `切换主题（下一个: ${THEME_LABELS[next] || next}）`;
                btn.setAttribute("title", nextLabel);
                btn.setAttribute("aria-label", nextLabel);
            }
        }

        function initTheme() {
            const stored = normalizeTheme(localStorage.getItem(THEME_KEY) || "light");
            applyTheme(stored);
        }

        function toggleTheme() {
            const current = normalizeTheme(document.documentElement.getAttribute("data-theme") || "light");
            const index = THEME_PRESETS.indexOf(current);
            const next = THEME_PRESETS[(index + 1) % THEME_PRESETS.length];
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

            setActivePanel(initialPanelId || "panel-stats", { persist: false, updateHash: Boolean(hash) });
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

        function _normalizeSubprojectPath(path) {
            let value = String(path || "").trim().replace(/\\\\/g, "/");
            while (value.startsWith("./")) value = value.slice(2);
            value = value.replace(/^\/+|\/+$/g, "");
            if (value === "." || value === "") return "";
            return value;
        }

        function _sanitizeJobSegment(value) {
            return String(value || "")
                .trim()
                .replace(/[^a-zA-Z0-9._-]+/g, "-")
                .replace(/-{2,}/g, "-")
                .replace(/^-+|-+$/g, "")
                .slice(0, 80);
        }

        function _normalizeDocType(value) {
            return _sanitizeJobSegment(String(value || "").trim().toLowerCase());
        }

        function _parseRepoFullName(repoUrl) {
            const raw = String(repoUrl || "").trim();
            if (!raw) return "";

            if (raw.startsWith("ssh://")) {
                try {
                    const u = new URL(raw);
                    const path = String(u.pathname || "").replace(/^\/+/, "").replace(/\.git$/i, "");
                    const parts = path.split("/").filter(Boolean);
                    if (parts.length >= 2) return `${parts[0]}/${parts[1]}`;
                } catch (e) {
                    return "";
                }
            }

            if (raw.includes("@") && raw.includes(":") && !/^https?:\/\//i.test(raw)) {
                const idx = raw.indexOf(":");
                if (idx > -1) {
                    const path = raw.slice(idx + 1).replace(/^\/+/, "").replace(/\.git$/i, "");
                    const parts = path.split("/").filter(Boolean);
                    if (parts.length >= 2) return `${parts[0]}/${parts[1]}`;
                }
            }

            try {
                const u = new URL(raw);
                const path = String(u.pathname || "").replace(/^\/+/, "").replace(/\.git$/i, "");
                const parts = path.split("/").filter(Boolean);
                if (parts.length >= 2) return `${parts[0]}/${parts[1]}`;
            } catch (e) {
                return "";
            }
            return "";
        }

        function _buildJobIdFromForm(form) {
            const repoUrl = form.querySelector('[name="repo_url"]')?.value || "";
            const repoFullName = _parseRepoFullName(repoUrl);
            if (!repoFullName) return "";

            const baseId = repoFullName.replace("/", "--");
            const subprojectName = form.querySelector('[name="subproject_name"]')?.value || "";
            const subprojectPathRaw = form.querySelector('[name="subproject_path"]')?.value || "";
            const subprojectPath = _normalizeSubprojectPath(subprojectPathRaw);
            const safeSubName = _sanitizeJobSegment(subprojectName);
            const safeSubPath = _sanitizeJobSegment(subprojectPath.replace(/\//g, "__"));
            const subKey = safeSubName || safeSubPath;

            const docTypeRaw = form.querySelector('[name="doc_type"]')?.value || "";
            const docKey = _normalizeDocType(docTypeRaw);

            let jobId = baseId;
            if (subKey) jobId += `__sp__${subKey}`;
            if (docKey) jobId += `__dt__${docKey}`;
            return jobId;
        }

        function _buildVersionStamp() {
            const d = new Date();
            const pad = (n) => String(n).padStart(2, "0");
            const yy = String(d.getFullYear()).slice(-2);
            return `${yy}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
        }

        function generateOutputPath(form) {
            if (!form) return;
            const outputInput = form.querySelector('[name="output"]');
            if (!outputInput) return;

            const jobId = _buildJobIdFromForm(form);
            if (!jobId) {
                outputInput.value = `output/docs/codewiki/${_buildVersionStamp()}`;
                return;
            }
            outputInput.value = `output/docs/${jobId}/${_buildVersionStamp()}`;
        }

        function wireOutputPathAutoGeneration(form) {
            if (!form) return;

            const refresh = () => generateOutputPath(form);
            const watchedFields = ["repo_url", "subproject_name", "subproject_path", "doc_type"];
            watchedFields.forEach((name) => {
                const el = form.querySelector(`[name="${name}"]`);
                if (!el) return;
                el.addEventListener("input", refresh);
                el.addEventListener("change", refresh);
            });

            form.addEventListener("submit", () => {
                generateOutputPath(form);
            });

            refresh();
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
            _setFormValue(form, "output", "");
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

            generateOutputPath(form);
            saveAdvancedOptions();
        }

        function _parseDocTypeProfile(raw) {
            const text = String(raw || "").trim();
            if (!text) return null;
            try {
                const parsed = JSON.parse(text);
                return parsed && typeof parsed === "object" ? parsed : null;
            } catch (error) {
                console.warn("Failed to parse doc type profile", error);
                return null;
            }
        }

        function _setDocTypeFormMode(mode, sourceName) {
            const titleEl = document.getElementById("docTypeFormTitle");
            const descEl = document.getElementById("docTypeFormDesc");
            const submitBtn = document.getElementById("docTypeSubmitBtn");
            const keyInput = document.getElementById("profile_doc_type");
            const safeName = String(sourceName || "").trim();

            if (mode === "edit") {
                if (titleEl) titleEl.textContent = safeName ? `编辑模板: ${safeName}` : "编辑模板";
                if (descEl) descEl.textContent = "将更新相同 key 的模板配置（编辑模式下 key 不可修改）。";
                if (submitBtn) submitBtn.textContent = "保存修改";
                if (keyInput) {
                    keyInput.readOnly = true;
                    keyInput.setAttribute("aria-readonly", "true");
                    keyInput.title = "编辑模式下文档类型 Key 不可修改";
                }
                return;
            }

            if (mode === "copy") {
                if (titleEl) titleEl.textContent = safeName ? `复制模板: ${safeName}` : "复制模板";
                if (descEl) descEl.textContent = "请修改 Key 后保存为新模板。";
                if (submitBtn) submitBtn.textContent = "保存为新模板";
                if (keyInput) {
                    keyInput.readOnly = false;
                    keyInput.removeAttribute("aria-readonly");
                    keyInput.title = "";
                }
                return;
            }

            if (titleEl) titleEl.textContent = "创建模板";
            if (descEl) descEl.textContent = "填写模板信息后保存；可通过下方表格快速编辑或复制。";
            if (submitBtn) submitBtn.textContent = "保存模板";
            if (keyInput) {
                keyInput.readOnly = false;
                keyInput.removeAttribute("aria-readonly");
                keyInput.title = "";
            }
        }

        function _fillDocTypeForm(profile, mode) {
            const form = document.getElementById("docTypeForm");
            if (!form || !profile || typeof profile !== "object") return;

            const sourceName = String(profile.name || "").trim();
            _setDocTypeFormMode(mode, sourceName);

            let docType = sourceName;
            if (mode === "copy") {
                docType = sourceName ? `${sourceName}-copy` : "";
            }

            _setFormValue(form, "doc_type", docType);
            _setFormValue(form, "display_name", profile.display_name || "");
            _setFormValue(form, "description", profile.description || "");
            _setFormValue(form, "prompt", profile.prompt || "");
            _setFormValue(form, "include", profile.include || "");
            _setFormValue(form, "exclude", profile.exclude || "");
            _setFormValue(form, "focus", profile.focus || "");
            _setFormValue(form, "skills", profile.skills || "");
            _setFormValue(form, "max_tokens", profile.max_tokens ?? "");
            _setFormValue(form, "max_token_per_module", profile.max_token_per_module ?? "");
            _setFormValue(form, "max_token_per_leaf_module", profile.max_token_per_leaf_module ?? "");
            _setFormValue(form, "max_depth", profile.max_depth ?? "");
            _setFormValue(form, "profile_concurrency", profile.concurrency ?? "");

            const keyInput = document.getElementById("profile_doc_type");
            if (keyInput) {
                keyInput.focus();
                if (mode === "copy") keyInput.select();
            }
        }

        function wireDocTypeManager() {
            const form = document.getElementById("docTypeForm");
            if (!form) return;

            const resetBtn = document.getElementById("docTypeResetBtn");
            if (resetBtn) {
                resetBtn.addEventListener("click", () => {
                    form.reset();
                    _setDocTypeFormMode("create", "");
                });
            }

            document.querySelectorAll(".doc-type-edit-btn[data-profile]").forEach((btn) => {
                btn.addEventListener("click", () => {
                    const profile = _parseDocTypeProfile(btn.getAttribute("data-profile"));
                    if (!profile) return;
                    _fillDocTypeForm(profile, "edit");
                });
            });

            document.querySelectorAll(".doc-type-copy-btn[data-profile]").forEach((btn) => {
                btn.addEventListener("click", () => {
                    const profile = _parseDocTypeProfile(btn.getAttribute("data-profile"));
                    if (!profile) return;
                    _fillDocTypeForm(profile, "copy");
                });
            });

            const deleteForm = document.getElementById("docTypeDeleteInlineForm");
            const deleteInput = document.getElementById("docTypeDeleteInlineInput");
            document.querySelectorAll(".doc-type-delete-btn[data-doc-type]").forEach((btn) => {
                btn.addEventListener("click", () => {
                    const docType = String(btn.getAttribute("data-doc-type") || "").trim();
                    if (!docType) return;
                    const typed = window.prompt(
                        `危险操作：将删除自定义模板 \"${docType}\"。\n请输入模板 Key 以确认：`,
                        "",
                    );
                    if (typed === null) return;
                    if (String(typed).trim() !== docType) {
                        alert("输入的模板 Key 不一致，已取消删除。");
                        return;
                    }
                    if (!deleteForm || !deleteInput) return;
                    deleteInput.value = docType;
                    deleteForm.submit();
                });
            });
        }

        function _advancedOptionHelpMap() {
            return {
                agent_cmd: {
                    title: "Agent 命令",
                    desc: "指定外部 Agent 命令来生成文档内容。留空表示使用默认模型 API 路径。",
                    examples: [
                        "claude -p",
                        "opencode",
                        "python my_agent.py --mode doc",
                    ],
                },
                output: {
                    title: "输出目录",
                    desc: "文档输出的目标目录。建议使用带时间戳的版本目录，避免覆盖历史结果。",
                    examples: [
                        "output/docs/o1--server/260310-153000",
                        "output/docs/o1--server__sp__game-admin/260310-153000",
                    ],
                },
                max_depth: {
                    title: "最大深度",
                    desc: "控制模块树聚类/文档组织深度。值越大层次越细，生成耗时通常越高。",
                    examples: [
                        "2: 粗粒度总览文档",
                        "4: 常用平衡值（推荐）",
                        "6: 细粒度风险或开发视图",
                    ],
                },
                concurrency: {
                    title: "并发数",
                    desc: "控制任务内部并行生成的工作线程数。过高可能增加模型并发压力与限流风险。",
                    examples: [
                        "2: 低负载稳定模式",
                        "4: 默认通用配置",
                        "8: 大仓库提速（需模型侧并发能力支持）",
                    ],
                },
                output_lang: {
                    title: "输出语言",
                    desc: "文档输出语言。默认保留主文档语言，可填目标语言代码触发翻译输出。",
                    examples: [
                        "zh",
                        "en",
                        "ja",
                    ],
                },
                max_tokens: {
                    title: "最大 Tokens",
                    desc: "单次模型回答的总 token 上限。过低会导致回答截断，过高会增加成本与延迟。",
                    examples: [
                        "32000",
                        "64000",
                    ],
                },
                max_token_per_module: {
                    title: "每模块最大 Tokens",
                    desc: "限制非叶子模块文档生成时的 token 上限，避免单模块输出过长。",
                    examples: [
                        "8000: 更紧凑",
                        "16000: 常用设置",
                    ],
                },
                max_token_per_leaf_module: {
                    title: "叶子模块最大 Tokens",
                    desc: "限制叶子模块（具体代码包）输出长度。用于控制细节深度与成本。",
                    examples: [
                        "6000: 概要型",
                        "12000: 详细型",
                    ],
                },
                include: {
                    title: "包含模式",
                    desc: "仅分析匹配模式的文件（逗号分隔）。用于快速聚焦某些语言或目录。",
                    examples: [
                        "*.go,*.proto",
                        "cmd/*.go,pkg/**/*.go",
                    ],
                },
                exclude: {
                    title: "排除模式",
                    desc: "忽略匹配模式的文件（逗号分隔）。常用于过滤测试、第三方和生成代码。",
                    examples: [
                        "*test*,*mock*",
                        "vendor/**,node_modules/**,**/*_gen.go",
                    ],
                },
                focus: {
                    title: "聚焦路径",
                    desc: "指定重点分析的模块/目录，模型会优先输出这些区域的详细内容。",
                    examples: [
                        "pkg/api,pkg/service",
                        "internal/order,internal/payment",
                    ],
                },
                instructions: {
                    title: "附加指令",
                    desc: "补充给模型的额外约束与风格要求，会叠加到文档类型模板提示词中。",
                    examples: [
                        "重点输出风险清单并给出修复优先级。",
                        "所有流程说明都要求带 Mermaid 时序图。",
                    ],
                },
                skills: {
                    title: "Skills",
                    desc: "启用内置技能提示词（逗号分隔），用于增强特定能力（如 Mermaid 校验）。",
                    examples: [
                        "mermaid-validator",
                        "mermaid-validator,security-checklist",
                    ],
                },
                custom_cli_args: {
                    title: "自定义 CLI 参数",
                    desc: "透传到底层 CLI 的额外参数。仅建议用于临时调试或高级定制。",
                    examples: [
                        "-v --max-depth 4",
                        "--include '*.go' --exclude '*test*'",
                    ],
                },
                create_branch: {
                    title: "生成后创建分支",
                    desc: "任务完成后在仓库中创建文档分支，便于后续提交流程。",
                    examples: [
                        "启用: 自动创建分支承载文档变更",
                        "关闭: 仅在本地输出目录生成文档",
                    ],
                },
                github_pages: {
                    title: "生成 GitHub Pages 页面",
                    desc: "生成可静态托管的页面资源，便于直接部署文档站点。",
                    examples: [
                        "启用: 输出 HTML 静态页面",
                        "关闭: 仅输出 Markdown 文档",
                    ],
                },
                no_cache: {
                    title: "禁用缓存",
                    desc: "忽略已有缓存，强制重新分析和生成。适用于代码刚变更或模板刚调整的场景。",
                    examples: [
                        "启用: 始终全量重跑",
                        "关闭: 优先复用缓存加速",
                    ],
                },
            };
        }

        function wireAdvancedOptionHelp() {
            const panel = document.getElementById("panel-create");
            if (!panel) return;

            const modal = document.getElementById("fieldHelpModal");
            const titleEl = document.getElementById("fieldHelpTitle");
            const descEl = document.getElementById("fieldHelpDesc");
            const examplesEl = document.getElementById("fieldHelpExamples");
            const closeBtn = document.getElementById("fieldHelpCloseBtn");
            if (!modal || !titleEl || !descEl || !examplesEl || !closeBtn) return;

            const showModal = (help) => {
                titleEl.textContent = help.title || "参数说明";
                descEl.textContent = help.desc || "暂无说明。";
                examplesEl.innerHTML = "";
                const examples = Array.isArray(help.examples) ? help.examples : [];
                if (!examples.length) {
                    const li = document.createElement("li");
                    li.textContent = "暂无示例";
                    examplesEl.appendChild(li);
                } else {
                    examples.forEach((item) => {
                        const li = document.createElement("li");
                        li.textContent = String(item || "");
                        examplesEl.appendChild(li);
                    });
                }
                modal.classList.add("open");
                modal.setAttribute("aria-hidden", "false");
            };

            const hideModal = () => {
                modal.classList.remove("open");
                modal.setAttribute("aria-hidden", "true");
            };

            closeBtn.addEventListener("click", hideModal);
            modal.addEventListener("click", (event) => {
                if (event.target === modal) hideModal();
            });
            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape" && modal.classList.contains("open")) {
                    hideModal();
                }
            });

            const helpMap = _advancedOptionHelpMap();
            Object.entries(helpMap).forEach(([fieldId, help]) => {
                const label = panel.querySelector(`.options-grid label[for="${fieldId}"]`);
                if (!label || label.dataset.helpBound === "1") return;
                label.dataset.helpBound = "1";
                label.classList.add("label-with-help");

                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "field-help-btn";
                btn.textContent = "i";
                btn.setAttribute("aria-label", `${help.title} 参数说明`);
                btn.setAttribute("title", "查看参数说明");
                btn.addEventListener("click", (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    showModal(help);
                });
                label.appendChild(btn);
            });
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
            const themePreset = document.getElementById("themePreset");
            if (themePreset) {
                themePreset.addEventListener("change", function() {
                    const next = normalizeTheme(themePreset.value);
                    localStorage.setItem(THEME_KEY, next);
                    applyTheme(next);
                });
            }

            loadAdvancedOptions();
            wireAdvancedOptionsPersistence();
            wireAdvancedOptionHelp();
            wireAdminPanels();
            wireDocTypeManager();
            const forcePanelFromServer = {{ (active_panel or "")|tojson }};
            if (forcePanelFromServer && typeof window.setAdminPanel === "function") {
                window.setAdminPanel(forcePanelFromServer);
            }
            wireTaskFilters();

            const createTaskForm = document.querySelector('form[action="/admin"]');
            const generateOutputBtn = document.getElementById("generateOutputPathBtn");
            if (createTaskForm) {
                wireOutputPathAutoGeneration(createTaskForm);
                if (generateOutputBtn) {
                    generateOutputBtn.addEventListener("click", () => generateOutputPath(createTaskForm));
                }
            }

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
