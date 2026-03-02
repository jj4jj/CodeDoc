# CodeDoc - 全局项目上下文与开发者指南

> [!NOTE]
> **项目特别说明：** **CodeDoc** 是从优秀的开源项目 [FSoft-AI4Code/CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki) fork 而来的增强版本。  
> 我们在保留原项目核心功能的基础上，引入了多项重大增强，包括无视上下文窗口的 **Agent 执行模式**、**多路并行生成**、**多语言文档自动翻译及无缝动态切换**以及对 **Golang** 的解析支持。详见下方的 [✨ 本项目的新增特性](#-本项目的新增特性)。

CodeWiki 是一个用于评估和生成大型代码库全景文档的 AI 驱动框架。本项目通过**多语言代码解析**、**架构感知的模块划分**以及**多智能体（Multi-Agent）递归生成**，为代码库构建结构化的文本及可视化文档（如：Mermaid 架构图、数据流图等）。

本文档主要面向新接手参与此项目的 **AI Agent** 和 **人类开发者**，提供快速理解系统核心、项目架构、扩展方式与开发规范的全局上下文信息。

## ✨ 本项目的新增特性

相较于原始 CodeWiki 项目，CodeDoc 重点增强了文档生成的速度、灵活性和国际化表现：

- **🤖 CLI Agent 执行模式 (`--with-agent-cmd`)**：允许将 Prompt 路由给外部 CLI 智能体进程（如 Claude Code, OpenCode）执行，**彻底绕开 LLM API 的上下文窗口限制和网关超时问题**。
- **⚡ 并行文档生成 (`-j`)**：将毫不相干的、底层的叶子模块（Leaf Modules）投入多线程并行提问，大幅度缩减大型项目的文档生成耗时。
- **🌍 多语言自动翻译 (`--output-lang`)**：可在生成基准文档的同时自动进行指定目标语言（如 `zh` 中文, `ja` 日文等）的全文翻译，并完整保留目录结构和图表。
- **🌐 动态 GitHub Pages 视图集成**：为你自动生成的 `index.html` 阅览页面嵌入了原生的**语言切换下拉菜单**，无需冗余页面即可一键在英文及你的翻译语言中来回无缝切换。
- **🐹 Golang 语言支持**：新增了核心对 Go 语言包机制的 AST 分析与依赖树提取的支持。
- **📊 Web 文档平台与任务队列**：内置 FastAPI Web 服务，提供任务提交、排队执行、进度追踪、管理面板（带图标）、RESTful API 接口，支持从仓库 URL 自动生成标题 (`<host>/<group>/<repo>` 格式)。

---

## 1. 核心技术栈与架构设计

- **主要语言**: Python 3.12+ 
- **核心依赖**:
  - `tree-sitter`: 提供7种主流语言的 AST 解析。
  - `pydantic` & `pydantic-ai`: 用于数据模型验证和 Agent 构建。
  - `litellm` & `openai`: 统一的 LLM 接口支持（Claude/GPT 等多模型调度）。
  - `click`: 强大而灵活的命令行界面构建。
  - `FastAPI`: 提供文档结果的展示后台与 Web 接口服务。
- **系统数据流架构**:
  `代码库树分析` -> `抽象语法树 AST 解析` -> `依赖关系图提取` -> `层次化聚类算法分解` -> `构建模块树` -> `递归 Agent 智能生成文档` -> `合成多维度全局文档 (Markdown + 交互视图)`

## 2. 项目核心模块与目录结构

```text
codewiki/
├── codewiki/                 # 核心代码包
│   ├── cli/                  # 命令行交互工具（CLI）
│   │   ├── commands/         # 子命令定义（config, generate）
│   │   ├── models/           # 配置相关的数据模型层
│   │   └── adapters/         # 外部服务集成适配
│   ├── src/                  # 系统核心业务逻辑
│   │   ├── be/               # 后端：依赖分析引擎与 Agent 编排系统
│   │   │   ├── dependency_analyzer/ # 多语言源代码 AST 解析器（BaseAnalyzer 及各语言子类）
│   │   │   ├── cluster_modules.py   # 基于功能与拓扑级联关系的模块聚类引擎
│   │   │   ├── agent_orchestrator.py# 中心化调度 Agent 工作流的编排核心
│   │   │   ├── agent_tools/         # 供 LLM Agent 调用的工具函数集合（如解析文件、读取节点等）
│   │   │   └── prompt_template.py   # LLM Prompt 系统提示词集中管理
│   │   └── fe/               # 前端：结果展示和 Web 服务后台
│   │       ├── web_app.py           # FastAPI 服务器核心逻辑
│   │       └── visualise_docs.py    # 文档数据可视化层
│   ├── templates/            # Web 端渲染交互组件的界面模板
│   └── run_web_app.py        # 独立启动 Web 服务的入口点
├── docs/                     # 生成完毕的文档目录示例及导出内容
├── docker/                   # 容器化部署方案配置
├── pyproject.toml            # Python 核心依赖及元数据定义文件
├── pytest.ini                # Pytest 测试框架配置参数
└── DEVELOPMENT.md            # 英文版的标准开发者指南
```

## 3. 关键设计模式与抽象机制

为了应对多语言代码的解析及其生成逻辑中的不确定性因素，项目抽象出以下几个关键性架构设计：

1. **策略模式与多态解析（Strategy Pattern）**:
   多语言的 AST 解析能力由 `src/be/dependency_analyzer/analyzers/base.py` 中定义的抽象基类 `BaseAnalyzer` 提供。每种受支持的编程语言都会通过继承该类来实现自身固有的语言树逻辑。相关注册点位于 `ast_parser.py` 的解析字典内，达成语言扩充与主流程的解耦化。
2. **层次化归并映射设计（Hierarchical Clustering）**:
   利用 `cluster_modules.py` 将大型代码库拆解成 LLM 当前 Context Window 易于理解的小型叶子节点（Leaf modules）。该分簇系统在兼顾 Token 管控上限的同时，能保持极强的项目上下游逻辑连贯性和层级结构。
3. **递归多智能体机制（Recursive Multi-Agent System）**:
   在核心编排引擎 `agent_orchestrator.py` 里，程序会动态评估各个解析模块的内部复杂度。当某功能节点体量异常时，主 Agent 程序会递归实例化和委派（Delegation） 子 Agents 进行处理，处理完毕后通过聚类整合返回结果。

## 4. 如何进行二次开发与扩展 (Extension Guide)

### 场景 A：添加新语言解析支持
系统天然内置良好的扩展闭环，如需注入新语言：
1. 前往 `codewiki/src/be/dependency_analyzer/analyzers` 新建新语言分析器（如 `php_analyzer.py`）。
2. 在该类体内继承 `BaseAnalyzer` 并实现两大核心方法：
   - `extract_dependencies(self, ast_node)`
   - `extract_components(self, ast_node)`
3. 跳转至 `src/be/dependency_analyzer/ast_parser.py` 中的 `LANGUAGE_ANALYZERS` 字典里，以键值对形式挂载新建的解析类。
4. （可选）在 `pyproject.toml` 的项目依赖表中加入新语言相应的 `tree-sitter-[lang]` 组件并更新环境。

### 场景 B：增加自定义的 CLI Agent 控制指令
1. 于 `cli/models/config.py` 中的 `AgentInstructions` `dataclass` 类型下添加对应功能所需的新变量字段。
2. 更新该配置结构的串行化生命周期方法（涉及 `to_dict` 与 `from_dict` 等）。
3. 前往 `cli/commands/generate.py` 使用 `@click.option` 将新功能暴露至终端环境。
4. 补齐消费侧逻辑：确保后方业务逻辑，或是系统提示词中正确响应新增加字段。

## 5. 项目开发规范 (Development Guidelines)

- **Python 代码风格风格**: 严格遵循 PEP-8；推荐集成并使用 `black` 自动化格式（`line-length = 100`）以及 `ruff` 代码 Linter。
- **类型提示 (Type Hints)**: 所有函数参数及返回值均推荐启用显式类型注解，通过 `mypy` 规避运行时动态错误。
- **文档维护**: 暴露在外的核心 Class 或 Utility 必须撰写包含输入输出详尽说明的 docstrings。
- **测试提交流程**: 集成了完善的单元测试套件，新分支提交必须确保所有 `pytest` 用例运行完毕且覆盖率未滑坡。

## 6. 构建与安装说明

### 环境准备工作
- 需准备 **Python 3.12** 及以上版本。
- 需具备 **Node.js** 的执行环境（>= 14.0，主要用于确保输出 Mermaid 解析图表的正确渲染核实）。

### 从源码安装调试
```bash
# 1. 下载源码并构建纯净的沙盒虚拟环境
git clone https://github.com/jj4jj/CodeDoc.git
cd CodeWiki
uv venv --python 3.12
#python3.12 -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2. 安装库至 Editable（开发） 模式及拉取依赖
uv pip install -e .
uv pip install -r requirements.txt
```

## 7. 常用运行与测试使用方法

### 大模型及系统配置初始化
使用生成前需进行必要的 AI Model 及基准令牌（Token）的路由配置，目前兼容支持全部类 OpenAI 格式。
```bash
codewiki config set \
  --api-key YOUR_API_KEY \
  --base-url {LLM_PROVIDER_HOST} \
  --main-model claude-sonnet-4 \
  --cluster-model claude-sonnet-4 \
  --fallback-models claude-sonnet-4,deepseek-chat

  $ codewiki config set --api-key sk-abc123 --base-url https://api.deepseek.com \
      --main-model deepseek-chat --cluster-model deepseek-chat --fallback-model deepseek-chat

  # Use environment variables instead (no config set needed)
  $ export CODEWIKI_API_KEY=sk-abc123
  $ export CODEWIKI_BASE_URL=https://api.deepseek.com
  $ export CODEWIKI_MAIN_MODEL=deepseek-chat
  $ export CODEWIKI_CLUSTER_MODEL=deepseek-chat
  $ codewiki generate

  # Update only max tokens
  $ codewiki config set --max-tokens 4096

  # Force API key into config file (no keychain)
  $ codewiki config set --api-key sk-xxx --save-key-to-file

Options:
  --api-key TEXT                  LLM API key. Stored in system keychain if
                                  available, otherwise saved in
                                  ~/.codewiki/config.json. Can also be set via
                                  CODEWIKI_API_KEY env var.
  --base-url TEXT                 LLM API base URL (e.g.,
                                  https://api.deepseek.com). Env:
                                  CODEWIKI_BASE_URL
  --main-model TEXT               Primary model for documentation generation.
                                  Env: CODEWIKI_MAIN_MODEL
  --cluster-model TEXT            Model for module clustering (recommend top-
                                  tier). Env: CODEWIKI_CLUSTER_MODEL
  --fallback-models TEXT          Comma-separated ordered list of fallback
                                  models to try when the main model fails.
                                  Example: 'deepseek-chat,deepseek-reasoner'.
                                  Env: CODEWIKI_FALLBACK_MODEL
  --save-key-to-file              Force API key to be saved in
                                  ~/.codewiki/config.json instead of the
                                  system keychain. Useful in CI or headless
                                  environments.
  --max-tokens INTEGER            Maximum tokens for LLM response (default:
                                  32768)
  --max-token-per-module INTEGER  Maximum tokens per module for clustering
                                  (default: 36369)
  --max-token-per-leaf-module INTEGER
                                  Maximum tokens per leaf module (default:
                                  16000)
  --max-depth INTEGER             Maximum depth for hierarchical decomposition
                                  (default: 2)
  --help                          Show this message and exit.


```

也可以通过 **环境变量** 或直接编辑 `~/.codewiki/config.json` 来配置：

```bash
# 环境变量（最高优先级）
export CODEWIKI_API_KEY=sk-...
export CODEWIKI_BASE_URL=https://api.openai.com/v1
export CODEWIKI_MAIN_MODEL=gpt-4o
export CODEWIKI_CLUSTER_MODEL=gpt-4o
```

**API Key 优先级**（高 → 低）：
1. `CODEWIKI_API_KEY` 环境变量
2. `~/.codewiki/config.json` 中的 `api_key` 字段
3. 系统钥匙串（keychain）

验证配置：
```bash
codewiki config validate         # 完整验证（含 API 连通性测试）
codewiki config validate --quick  # 跳过 API 连通性测试
codewiki config show              # 显示当前配置
```

### 业务级文档一键分析生成
```bash
# 执行整个工程代码分析并创建含有交互页面的文档分支
codewiki generate --github-pages --create-branch
```

### CLI Agent 模式（绕过上下文窗口限制）

通过 `--with-agent-cmd` 将 LLM 提示词路由至 CLI Agent 子进程（如 Claude Code），**完全绕开 API 上下文窗口和网关超时限制**：

```bash
# 使用 Claude CLI 作为文档生成后端
codewiki generate --with-agent-cmd "claude --dangerously-skip-permissions -p"

# 搭配并行处理加速
codewiki generate \
  --with-agent-cmd "claude --dangerously-skip-permissions -p" \
  --github-pages \
  --output-lang zh \
  --create-branch \
  -j 4
```

### 多语言翻译

生成文档的同时自动翻译为指定语言：

```bash
# 生成文档 + 中文翻译
codewiki generate --output-lang zh

# 生成文档 + 日文翻译
codewiki generate --output-lang ja

# 支持任意 BCP-47 语言代码: zh, zh-tw, ja, ko, fr, de, es …
codewiki generate --output-lang fr
```

翻译输出写入 `<output-dir>/<lang>/` 目录，保持相同文件结构。

### 并行处理

叶模块（leaf module）相互独立，可以安全并行处理：

```bash
# 默认: 4 路并行
codewiki generate

# 增加并行数
codewiki generate -j 8

# 串行模式（用于 API 限速场景）
codewiki generate -j 1
```

### 断点续跑

如果生成中途中断，重新运行相同命令即可自动**从上次进度恢复**：

```bash
# 第一次运行（中途 Ctrl-C 中断）
codewiki generate --with-agent-cmd "claude -p"
# ^C

# 重新运行：自动检测已完成的模块并跳过
codewiki generate --with-agent-cmd "claude -p"
# 出现提示时选择 [r] Resume
```

进度输出示例：
```
  [1/24] ↩ [skip] LLM Providers        ← 已存在，跳过
  [2/24] ↩ [skip] Core Schemas         ← 已存在，跳过
  [3/24] ▶ [leaf] MCP                  ← 新模块，开始生成
  [3/24] ✓ [leaf] MCP (42.1s)          ← 完成
```

### 在网页中查看生成的文档

CodeWiki 输出标准 Markdown 文件，以下是推荐的 Web 查看方式：

#### 方式一 — 内置 HTML 查看器（最快）

生成时加上 `--github-pages` 参数，会在输出目录生成一个自包含的 `index.html`：

```bash
codewiki generate --github-pages
# 用浏览器打开 docs/codewiki/index.html 即可
```

#### 方式二 — GitHub Pages（零配置在线托管）

```bash
# 1. 生成带 HTML 查看器的文档
codewiki generate --github-pages --create-branch

# 2. 推送到 GitHub
git push origin <分支名>

# 3. 在 GitHub 仓库 Settings → Pages → 选择推送的分支 + /docs/codewiki 文件夹
# 文档将发布到: https://<org>.github.io/<repo>/
```

#### 方式三 — MkDocs（精美本地/远程站点）

```bash
pip install mkdocs mkdocs-material

# 在项目根目录创建 mkdocs.yml
cat > mkdocs.yml << 'EOF'
site_name: 我的项目 Wiki
docs_dir: docs/codewiki
theme:
  name: material
EOF

mkdocs serve          # 本地预览，访问 http://localhost:8000
mkdocs gh-deploy      # 自动部署到 GitHub Pages
```

#### 方式四 — Docsify（无构建，只需 index.html）

```bash
# 在文档目录下创建 index.html
cat > docs/codewiki/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>文档</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>window.$docsify = { name: '我的项目', loadSidebar: false }</script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
</body>
</html>
EOF

# 本地运行
npx serve docs/codewiki
# 或: python3 -m http.server 8000 --directory docs/codewiki
```

#### 方式五 — 快速本地预览

```bash
# Python 内置（无需安装）
python3 -m http.server 8000 --directory docs/codewiki
# 打开 http://localhost:8000

# 或安装 grip（GitHub 风格渲染）
pip install grip && grip docs/codewiki/overview.md
```

### 测试及日志追踪相关
如面临语法树解析报错、API 瓶颈挂起等行为，通过下方方式定位：
```bash
# 获取极其详细的 Debugging 分析流信息
codewiki generate --verbose
# （或）在终端定义变量全局生效
export CODEWIKI_LOG_LEVEL=DEBUG

# 验证代码稳定性，运行测试大盘
pytest -v --cov=codewiki --cov-report=term-missing
```

### Web 文档平台与任务队列

CodeDoc 内置 FastAPI Web 服务，提供任务提交、排队执行、进度追踪、管理面板等完整功能。

#### 启动 Web 服务

```bash
# 方式一：直接运行
python codewiki/run_web_app.py --host 127.0.0.1 --port 8000

# 方式二：模块方式
python -m codewiki.run_web_app --host 0.0.0.0 --port 8000
```

服务启动后访问：
- **首页**：http://localhost:8000/ —— 提交文档生成任务
- **管理面板**：http://localhost:8000/admin —— 任务管理（带图标界面）
- **文档查看**：http://localhost:8000/docs/{job_id} —— 查看生成的文档

#### 功能特性

| 特性 | 说明 |
|------|------|
| **任务队列** | 提交任务自动进入队列，后台串行执行 |
| **自动标题** | 从仓库 URL 自动生成标题，格式：`<host>/<group>/<repo>` |
| **进度追踪** | 实时显示任务状态（queued → processing → completed/failed） |
| **管理面板** | 带 FontAwesome 图标的 Web 界面，支持任务查看、删除 |
| **无认证** | 开放访问，无需登录 |

#### RESTful API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tasks` | GET | 获取任务列表，支持 `?status_filter=` 过滤 |
| `/api/tasks` | POST | 提交新任务，参数：`repo_url`, `commit_id`(可选), `priority`(可选) |
| `/api/tasks/{job_id}` | DELETE | 删除指定任务 |
| `/api/job/{job_id}` | GET | 获取单个任务状态 |

**API 使用示例：**

```bash
# 提交任务
curl -X POST "http://localhost:8000/api/tasks?repo_url=https://github.com/owner/repo"

# 查询任务列表
curl "http://localhost:8000/api/tasks"

# 按状态过滤
curl "http://localhost:8000/api/tasks?status_filter=completed"

# 删除任务
curl -X DELETE "http://localhost:8000/api/tasks/owner--repo"
```

#### 自动标题生成规则

系统自动从仓库 URL 提取标题，格式为 `<host>/<group>/<repo>`：

| URL 类型 | 生成标题示例 |
|----------|-------------|
| `https://github.com/owner/repo` | `github.com/owner/repo` |
| `ssh://git@szgit.gs.com:36001/gsbase/gsdr.git` | `szgit.gs.com/gsbase/gsdr` |
| `git@gitlab.com:group/subgroup/repo.git` | `gitlab.com/group/subgroup/repo` |

---

> 💡 **给新接手 AI Agent 的直接导览建议**: 
> 亲爱的 Agent 协作者，在探索此代码仓库时，强推荐您第一时间聚焦于 `src/be/agent_orchestrator.py` 的多 Agent 机制执行路线。如果你受到的指令涉及了上下文扩展、或是重组底层 Prompt 提示体系，请您深入解剖 `prompt_template.py` 内部封装的结构、以及它是如何协同 `ast_parser.py` 进行跨模块传递分工的。若要处理渲染方面的反馈，则直接查看前端业务域 `src/fe/` 以及 `templates/` 下相关的视图服务逻辑。

---

## 附录：新增 CLI 参数速查表

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--with-agent-cmd CMD` | 用 CLI Agent 子进程替代 API 调用 | 无（使用 API） |
| `-j N` / `--concurrency N` | 并行处理叶模块数 | 4 |
| `--output-lang LANG` | 生成后自动翻译到指定语言 | 无 |
| `--fallback-models M1,M2` | fallback 模型列表（逗号分隔） | 同 main_model |
| `--output-dir DIR` / `-o DIR` | 输出目录 | `docs/codewiki` |
| `--max-tokens N` | LLM 输出最大 token 数 | 32768 |
| `--max-token-per-module N` | 模块聚类输入 token 阈值 | 36369 |
| `--max-token-per-leaf-module N` | 叶模块输入 token 阈值 | 16000 |
| `--max-depth N` | 层次分解最大深度 | 2 |

---

## 附录：架构技术原理 Q&A

### Q1: 代码分析生成 Wiki 的完整流程是什么？

CodeWiki 通过 **5 个阶段** 将源代码转化为全局结构化文档：

```
源代码仓库
    │
    ▼
┌──────────────────────────────────────┐
│ 阶段 1: AST 解析 + 依赖图构建        │  dependency_analyzer/
│   tree-sitter 多语言语法树解析        │  → components + leaf_nodes
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 阶段 2: 层次化模块聚类               │  cluster_modules.py
│   LLM 驱动的功能分组（递归分治）      │  → module_tree.json
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 阶段 3: 叶模块文档生成（可并行）      │  agent_orchestrator.py
│   pydantic-ai Agent / cmd_agent      │  → 每个叶模块一个 .md
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 阶段 4: 父模块 + 全局概览生成         │  documentation_generator.py
│   自底向上聚合子文档 → overview.md    │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 阶段 5: 后处理（翻译 / HTML 视图）    │  --output-lang / --github-pages
└──────────────────────────────────────┘
```

**模块关系图：**

```
CLI 层                          后端业务层
─────────                       ──────────

generate.py                     documentation_generator.py
    │                               │ (总编排器)
    ▼                               │
doc_generator.py ──────────────────▶├→ dependency_analyzer/
  (构建 Config,                     │     (AST 解析 + 组件提取)
   调用后端,                        ├→ cluster_modules.py
   处理翻译)                        │     (LLM 驱动的层次聚类)
                                    ├→ agent_orchestrator.py
config_manager.py                   │     (pydantic-ai Agent 编排)
  (加载/保存配置,                   │   ── 或 ──
   API Key 优先级)                  ├→ cmd_agent_orchestrator.py
                                    │     (CLI 子进程模式)
                                    ├→ llm_services.py
                                    │     (OpenAI 客户端, FallbackModel)
                                    └→ prompt_template.py
                                          (所有 LLM 提示词模板)
```

---

### Q2: 每个阶段的输入和输出分别是什么？

#### 阶段 1：AST 解析与依赖图构建

**输入：** 整个代码仓库的文件系统（经 `--include`/`--exclude` 过滤后的源代码文件）。

**处理：** tree-sitter 对每个文件做语法树解析，提取出所有函数、类、方法的签名 + 源代码 + 文件路径 + 依赖关系。

**输出：**

| 输出项 | 类型 | 内容 |
|--------|------|------|
| `components` | `Dict[str, Node]` | 所有代码组件的字典（ID → 节点信息），每个 Node 含源代码、文件路径、行号、依赖列表 |
| `leaf_nodes` | `List[str]` | 所有可文档化组件的 ID 列表 |

示例（简化）：
```python
components = {
    "core.providers.openai.OpenAIProvider": Node(
        type="class",
        relative_path="core/providers/openai.py",
        source_code="class OpenAIProvider:\n    ...",
        dependencies=["core.schemas.responses.ChatResponse"],
    ),
    "core.schemas.responses.ChatResponse": Node(
        type="class",
        source_code="class ChatResponse:\n    ...",
        dependencies=[],
    ),
    # ... 几百到几千个
}

leaf_nodes = [
    "core.providers.openai.OpenAIProvider",
    "core.schemas.responses.ChatResponse",
    # ...
]
```

---

#### 阶段 2：层次化模块聚类

**输入：** 来自阶段 1 的 `components` + `leaf_nodes` + 配置参数（`max_token_per_module`, `max_depth`, `cluster_model`）。

**处理（递归分治）：**

1. 计算所有组件的文本总 Token 数
2. 若 Token 数 ≤ 阈值 → 直接作为一个叶模块，停止
3. 若 Token 数 > 阈值 → 构造聚类 Prompt，发给 LLM：
   - 输入：所有组件的 ID 列表（按文件分组）
   - LLM 输出：按功能语义分成 N 个子组
4. 对每个子组递归执行步骤 1-3，直到所有子组都在阈值内 或 达到最大深度

**输出：**

| 输出项 | 文件 | 内容 |
|--------|------|------|
| `module_tree` | `first_module_tree.json` | 层级模块树 JSON |
| `module_tree` | `module_tree.json` | 同上（运行时副本） |

示例：
```json
{
  "LLM Providers - OpenAI": {
    "components": ["core.providers.openai.OpenAIProvider", "..."],
    "children": {}
  },
  "LLM Providers - Anthropic": {
    "components": ["core.providers.anthropic.AnthropicProvider"],
    "children": {}
  },
  "Core Schemas": {
    "components": ["core.schemas.responses.ChatResponse"],
    "children": {}
  }
}
```

> `children: {}` 表示叶模块。若某模块被递归拆分，children 内嵌套子模块树。

---

#### 阶段 3：叶模块文档生成

**输入（每个叶模块独立构造）：**

| 输入项 | 内容 |
|--------|------|
| `module_name` | 模块名（如 `"LLM Providers - OpenAI"`） |
| `core_component_ids` | 该模块包含的组件 ID 列表 |
| `components` | 阶段 1 输出的完整 Dict（用于读取源代码） |
| `module_tree` | 阶段 2 的完整模块树（提供全局上下文） |
| `system_prompt` | 提示词模板（写文档的格式要求 + 可用工具说明） |

实际发给 LLM 的 Prompt 包含：
- 模块在全局中的位置（简化的模块树）
- 该模块所有组件的**完整源代码**
- 文档格式要求（Markdown + Mermaid 图）

**处理：** pydantic-ai Agent 或 CLI Agent 子进程生成文档。Agent 可调用工具递归生成子文档。

**输出：** 每个叶模块一个 `.md` 文件（含文字描述 + Mermaid 架构图 + 数据流图）。

---

### Q3: 全局文档和模块间关联是怎么生成的？

核心机制是 **自底向上聚合** + **将子文档全文喂给 LLM**。

#### 处理顺序：拓扑排序（叶先、父后）

```
[1] OpenAI.md            ← 叶模块（并行）
[2] Anthropic.md         ← 叶模块（并行）
[3] Core Schemas.md      ← 叶模块（并行）
────── 以上全部完成后 ──────
[4] LLM Providers.md     ← 父模块（串行，读取 [1]+[2] 的全文）
────── 以上全部完成后 ──────
[5] overview.md          ← 全局概览（读取所有模块的全文）
```

#### 关键步骤：`build_overview_structure()`

生成父模块文档时，`build_overview_structure()` 做了一件关键的事——**把子模块的 .md 文件全文注入到模块树 JSON 中**：

```json
{
  "LLM Providers": {
    "is_target_for_overview_generation": true,
    "children": {
      "OpenAI": {
        "components": ["..."],
        "docs": "# OpenAI Provider\n\n## Overview\n..."
      },
      "Anthropic": {
        "components": ["..."],
        "docs": "# Anthropic Provider\n\n## Overview\n..."
      }
    }
  },
  "Core Schemas": { "components": ["..."] },
  "MCP": { "components": ["..."] }
}
```

- **目标模块的子文档**：注入全文 → LLM 可以总结、提炼共性、描述组件间交互
- **其他模块**：只保留组件列表（不含全文） → 提供全局位置上下文
- **`is_target_for_overview_generation`** 标记 → 告诉 LLM 只为这个模块写概览

#### 全局 overview.md

当生成最终 `overview.md` 时，所有顶层模块的 `.md` 全文都被注入。LLM 拿到全部文档后能够：

- 识别跨模块的依赖（如 OpenAI Provider 使用了 Core Schemas 的 ChatResponse）
- 画出端到端架构图
- 描述各模块之间的协作关系

#### 关联信息的三层来源

| 层级 | 阶段 | 信息来源 |
|------|------|---------|
| ① 叶模块文档内 | 阶段 3 | LLM 输入里包含整棵 module_tree 的简要结构 → 叶文档里已可提到"依赖 Core Schemas 模块" |
| ② 父模块概览 | 阶段 4 | LLM 输入里包含所有子模块文档的**全文** → 可以总结共性、描述子模块间交互 |
| ③ 全局 overview | 阶段 4 | LLM 输入里包含所有顶层模块文档的**全文** → 生成端到端架构图 + 模块间交互描述 |

> **一句话总结：** 关联文档不是通过代码分析直接产出的，而是通过**逐层把子文档全文喂给 LLM**，让 LLM 读懂模块之间的关系后，自己写出跨模块的架构描述和 Mermaid 图。这就是"自底向上合成"的核心含义。

---

### Q4: 核心设计思想

| 设计 | 解决的问题 | 实现机制 |
|------|-----------|---------|
| **层次化分治** | 代码库太大，超出上下文窗口 | 递归聚类 → 把大问题拆成 LLM 能处理的小块 |
| **自底向上合成** | 需要全局视角，但只能看局部 | 先生成叶文档 → 逐层聚合 → 最终产出全局概览 |
| **递归 Agent 委派** | 单个模块内部也可能很复杂 | Agent 可调用工具递归生成子文档（`generate_sub_module_documentation`） |
| **多模态输出** | 纯文字不够直观 | Prompt 要求 Agent 输出 Mermaid 架构图、数据流图、序列图 |
| **策略模式** | 需支持多种语言 | 每种语言一个 Analyzer 子类（`BaseAnalyzer` 继承），注册即用 |
