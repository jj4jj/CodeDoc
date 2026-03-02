<h1 align="center">CodeWiki: Evaluating AI's Ability to Generate Holistic Documentation for Large-Scale Codebases</h1>

<p align="center">
  <strong>AI-Powered Repository Documentation Generation</strong> • <strong>Multi-Language Support</strong> • <strong>Architecture-Aware Analysis</strong>
</p>

<p align="center">
  Generate holistic, structured documentation for large-scale codebases • Cross-module interactions • Visual artifacts and diagrams
</p>

<p align="center">
  <a href="https://python.org/"><img alt="Python version" src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" /></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" /></a>
  <a href="https://github.com/FSoft-AI4Code/CodeWiki/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/FSoft-AI4Code/CodeWiki?style=flat-square" /></a>
  <a href="https://arxiv.org/abs/2510.24428"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2510.24428-b31b1b?style=flat-square" /></a>
</p>

<p align="center">
  <a href="#quick-start"><strong>Quick Start</strong></a> •
  <a href="#cli-commands"><strong>CLI Commands</strong></a> •
  <a href="#documentation-output"><strong>Output Structure</strong></a> •
  <a href="https://arxiv.org/abs/2510.24428"><strong>Paper</strong></a>
</p>

<p align="center">
  <img src="./img/framework-overview.png" alt="CodeWiki Framework" width="600" style="border: 2px solid #e1e4e8; border-radius: 12px; padding: 20px;"/>
</p>

> [!NOTE]
> **This is an enhanced fork of the original [FSoft-AI4Code/CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki).**  
> We have added significant new features to improve generation speed, bypass LLM API constraints, and support multi-language documentation mapping. See [✨ Features in this Fork](#-features-in-this-fork) below for details.

---

## Quick Start

### 1. Install CodeWiki

```bash
# Install from source
pip install git+https://github.com/FSoft-AI4Code/CodeWiki.git

# Verify installation
codewiki --version
```

### 2. Configure Your Environment

CodeWiki supports multiple models via an OpenAI-compatible SDK layer.

```bash
codewiki config set \
  --api-key YOUR_API_KEY \
  --base-url https://api.anthropic.com \
  --main-model claude-sonnet-4 \
  --cluster-model claude-sonnet-4 \
  --fallback-models claude-sonnet-4,gpt-4o
```

You can also use **environment variables** or store the API key directly in `~/.codewiki/config.json`:

```bash
# Environment variables (highest priority)
export CODEWIKI_API_KEY=sk-...
export CODEWIKI_BASE_URL=https://api.openai.com/v1
export CODEWIKI_MAIN_MODEL=gpt-4o
export CODEWIKI_CLUSTER_MODEL=gpt-4o
```

### 3. Generate Documentation

```bash
# Navigate to your project
cd /path/to/your/project

# Generate documentation
codewiki generate

# Generate with HTML viewer for GitHub Pages
codewiki generate --github-pages --create-branch
```

**That's it!** Your documentation will be generated in `./docs/codewiki/` with comprehensive repository-level analysis.

### Usage Example

![CLI Usage Example](https://github.com/FSoft-AI4Code/CodeWiki/releases/download/assets/cli-usage-example.gif)

---

## What is CodeWiki?

CodeWiki is an open-source framework for **automated repository-level documentation** across seven programming languages. It generates holistic, architecture-aware documentation that captures not only individual functions but also their cross-file, cross-module, and system-level interactions.

### Key Innovations

| Innovation | Description | Impact |
|------------|-------------|--------|
| **Hierarchical Decomposition** | Dynamic programming-inspired strategy that preserves architectural context | Handles codebases of arbitrary size (86K-1.4M LOC tested) |
| **Recursive Agentic System** | Adaptive multi-agent processing with dynamic delegation capabilities | Maintains quality while scaling to repository-level scope |
| **Multi-Modal Synthesis** | Generates textual documentation, architecture diagrams, data flows, and sequence diagrams | Comprehensive understanding from multiple perspectives |

### Supported Languages

**🐍 Python** • **☕ Java** • **🟨 JavaScript** • **🔷 TypeScript** • **⚙️ C** • **🔧 C++** • **🪟 C#** • **🐹 Go** *(Added in this fork)*

---

## ✨ Features in this Fork

This fork significantly extends the original CodeWiki project with tools focused on developer ergonomics, scale, and internationalization:

- **🤖 CLI Agent Execution Mode (`--with-agent-cmd`)**: Bypasses strict API context window limitations and gateway timeouts by piping LLM prompts directly through CLI agents (e.g., Claude Code, OpenCode).
- **⚡ Parallel Processing (`-j`)**: Dramatically speeds up documentation generation by parsing and generating independent leaf modules in parallel.
- **🌍 Multi-Language Translation (`--output-lang`)**: Seamlessly translates the generated Markdown documentation into any BCP-47 language code (e.g., `zh`, `ja`, `es`) while maintaining the identical folder structure.
- **🌐 Dynamic GitHub Pages Viewer**: The generated `index.html` viewer now includes a built-in dropdown to dynamically switch between documentation languages on the fly without duplicating HTML files.
- **🐹 Golang Support**: Integrated native AST parsing and dependency analysis for Go (`.go`) projects.

---

## CLI Commands

### Configuration Management

```bash
# Set up your API configuration
codewiki config set \
  --api-key <your-api-key> \
  --base-url <provider-url> \
  --main-model <model-name> \
  --cluster-model <model-name> \
  --fallback-models <model1,model2,...>

# Configure max token settings
codewiki config set --max-tokens 32768 --max-token-per-module 36369 --max-token-per-leaf-module 16000

# Configure max depth for hierarchical decomposition
codewiki config set --max-depth 3

# Show current configuration
codewiki config show

# Validate your configuration (tests API connectivity)
codewiki config validate

# Quick validation (skip API connectivity test)
codewiki config validate --quick
```

### Documentation Generation

```bash
# Basic generation
codewiki generate

# Custom output directory
codewiki generate --output ./documentation

# Create git branch for documentation
codewiki generate --create-branch

# Generate HTML viewer for GitHub Pages
codewiki generate --github-pages

# Enable verbose logging
codewiki generate --verbose

# Full-featured generation
codewiki generate --create-branch --github-pages --verbose
```

### CLI Agent Mode

Bypass LLM API context window limits by routing prompts through a **CLI agent subprocess** (e.g. Claude Code, OpenCode):

```bash
# Use Claude CLI as the generation backend (no context window limits!)
codewiki generate --with-agent-cmd "claude --dangerously-skip-permissions -p"

# Combine with parallel processing for speed
codewiki generate \
  --with-agent-cmd "claude --dangerously-skip-permissions -p" \
  -j 4
```

The prompt is piped via **stdin**, and the agent's **stdout** is captured as the documentation. This completely bypasses API gateway timeouts and context window constraints.

### Multi-Language Translation

Generate documentation and translate into another language:

```bash
# Generate docs + Chinese translation
codewiki generate --output-lang zh

# Generate docs + Japanese translation
codewiki generate --output-lang ja

# Any BCP-47 / common lang code: zh, zh-tw, ja, ko, fr, de, es …
codewiki generate --output-lang fr
```

Translated output is written to `<output-dir>/<lang>/` with the same file structure.

### Parallel Processing

Leaf modules are independent and safe to process in parallel:

```bash
# Default: 4 parallel workers
codewiki generate

# Increase parallelism
codewiki generate -j 8

# Serial mode (if hitting API rate limits)
codewiki generate -j 1
```

### Checkpoint & Resume

If generation is interrupted, simply re-run the same command. CodeWiki detects existing `.md` files and **resumes from where it left off**:

```bash
# First run (interrupted mid-way)
codewiki generate --with-agent-cmd "claude -p"
# ^C  (Ctrl-C)

# Re-run: automatically resumes from last checkpoint
codewiki generate --with-agent-cmd "claude -p"
# Choose [r] Resume when prompted
```

### Viewing Documentation on the Web

CodeWiki generates Markdown files. Here are the recommended ways to view them as a web wiki:

#### Option 1 — Built-in HTML Viewer (quickest)

Add `--github-pages` when generating to get a self-contained `index.html` that renders the wiki in browser:

```bash
codewiki generate --github-pages
# Open docs/codewiki/index.html in your browser
```

#### Option 2 — GitHub Pages (zero config hosting)

```bash
# 1. Generate with HTML viewer
codewiki generate --github-pages --create-branch

# 2. Push to GitHub
git push origin docs/codewiki-<timestamp>

# 3. In repo Settings → Pages → select the branch + /docs/codewiki folder
# Your wiki will be live at: https://<org>.github.io/<repo>/
```

#### Option 3 — MkDocs (polished local / hosted site)

```bash
pip install mkdocs mkdocs-material

# Create minimal mkdocs.yml at project root
cat > mkdocs.yml << 'EOF'
site_name: My Project Wiki
docs_dir: docs/codewiki
theme:
  name: material
EOF

mkdocs serve          # Live preview at http://localhost:8000
mkdocs gh-deploy      # Deploy to GitHub Pages automatically
```

#### Option 4 — Docsify (zero-build, just drop index.html)

```bash
# Create a minimal index.html in your docs directory
cat > docs/codewiki/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Docs</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>window.$docsify = { name: 'My Project', loadSidebar: false }</script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/docsify.min.js"></script>
</body>
</html>
EOF

# Serve locally
npx serve docs/codewiki
# Or: python3 -m http.server 8000 --directory docs/codewiki
```

#### Option 5 — Quick local preview

```bash
# Python (built-in, no extra install)
python3 -m http.server 8000 --directory docs/codewiki
# Open http://localhost:8000

# Or install grip for GitHub-flavored rendering
pip install grip && grip docs/codewiki/overview.md
```

### Customization Options

CodeWiki supports customization for language-specific projects and documentation styles:

```bash
# C# project: only analyze .cs files, exclude test directories
codewiki generate --include "*.cs" --exclude "Tests,Specs,*.test.cs"

# Focus on specific modules with architecture-style docs
codewiki generate --focus "src/core,src/api" --doc-type architecture

# Add custom instructions for the AI agent
codewiki generate --instructions "Focus on public APIs and include usage examples"
```

#### Pattern Behavior (Important!)

- **`--include`**: When specified, **ONLY** these patterns are used (replaces defaults completely)
  - Example: `--include "*.cs"` will analyze ONLY `.cs` files
  - If omitted, all supported file types are analyzed
  - Supports glob patterns: `*.py`, `src/**/*.ts`, `*.{js,jsx}`
  
- **`--exclude`**: When specified, patterns are **MERGED** with default ignore patterns
  - Example: `--exclude "Tests,Specs"` will exclude these directories AND still exclude `.git`, `__pycache__`, `node_modules`, etc.
  - Default patterns include: `.git`, `node_modules`, `__pycache__`, `*.pyc`, `bin/`, `dist/`, and many more
  - Supports multiple formats:
    - Exact names: `Tests`, `.env`, `config.local`
    - Glob patterns: `*.test.js`, `*_test.py`, `*.min.*`
    - Directory patterns: `build/`, `dist/`, `coverage/`

#### Setting Persistent Defaults

Save your preferred settings as defaults:

```bash
# Set include patterns for C# projects
codewiki config agent --include "*.cs"

# Exclude test projects by default (merged with default excludes)
codewiki config agent --exclude "Tests,Specs,*.test.cs"

# Set focus modules
codewiki config agent --focus "src/core,src/api"

# Set default documentation type
codewiki config agent --doc-type architecture

# View current agent settings
codewiki config agent

# Clear all agent settings
codewiki config agent --clear
```

| Option | Description | Behavior | Example |
|--------|-------------|----------|---------|
| `--include` | File patterns to include | **Replaces** defaults | `*.cs`, `*.py`, `src/**/*.ts` |
| `--exclude` | Patterns to exclude | **Merges** with defaults | `Tests,Specs`, `*.test.js`, `build/` |
| `--focus` | Modules to document in detail | Standalone option | `src/core,src/api` |
| `--doc-type` | Documentation style | Standalone option | `api`, `architecture`, `user-guide`, `developer` |
| `--instructions` | Custom agent instructions | Standalone option | Free-form text |

### Token Settings

CodeWiki allows you to configure maximum token limits for LLM calls. This is useful for:
- Adapting to different model context windows
- Controlling costs by limiting response sizes
- Optimizing for faster response times

```bash
# Set max tokens for LLM responses (default: 32768)
codewiki config set --max-tokens 16384

# Set max tokens for module clustering (default: 36369)
codewiki config set --max-token-per-module 40000

# Set max tokens for leaf modules (default: 16000)
codewiki config set --max-token-per-leaf-module 20000

# Set max depth for hierarchical decomposition (default: 2)
codewiki config set --max-depth 3

# Override at runtime for a single generation
codewiki generate --max-tokens 16384 --max-token-per-module 40000 --max-depth 3
```

| Option | Description | Default |
|--------|-------------|---------|
| `--max-tokens` | Maximum output tokens for LLM response | 32768 |
| `--max-token-per-module` | Input tokens threshold for module clustering | 36369 |
| `--max-token-per-leaf-module` | Input tokens threshold for leaf modules | 16000 |
| `--max-depth` | Maximum depth for hierarchical decomposition | 2 |

### Configuration Storage & Priority

**API key resolution order** (highest → lowest):

1. `CODEWIKI_API_KEY` environment variable
2. `api_key` field in `~/.codewiki/config.json`
3. System keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)

| Source | Where | Notes |
|--------|-------|-------|
| Environment variables | Shell / CI | Highest priority, `CODEWIKI_API_KEY`, `CODEWIKI_BASE_URL`, `CODEWIKI_MAIN_MODEL`, `CODEWIKI_CLUSTER_MODEL` |
| Config file | `~/.codewiki/config.json` | Editable directly, supports `api_key` field |
| System keychain | OS keychain | Set via `codewiki config set --api-key` |
| Config file (forced) | `~/.codewiki/config.json` | `codewiki config set --api-key KEY --save-key-to-file` |

---

## Documentation Output

Generated documentation includes both **textual descriptions** and **visual artifacts** for comprehensive understanding.

### Textual Documentation
- Repository overview with architecture guide
- Module-level documentation with API references
- Usage examples and implementation patterns
- Cross-module interaction analysis

### Visual Artifacts
- System architecture diagrams (Mermaid)
- Data flow visualizations
- Dependency graphs and module relationships
- Sequence diagrams for complex interactions

### Output Structure

```
./docs/codewiki/
├── overview.md              # Repository overview (start here!)
├── module1.md               # Module documentation
├── module2.md               # Additional modules...
├── module_tree.json         # Hierarchical module structure
├── first_module_tree.json   # Initial clustering result
├── metadata.json            # Generation metadata
├── index.html               # Interactive viewer (with --github-pages)
└── zh/                      # Translation output (with --output-lang zh)
    ├── overview.md
    └── ...
```

---

## Experimental Results

CodeWiki has been evaluated on **CodeWikiBench**, the first benchmark specifically designed for repository-level documentation quality assessment.

### Performance by Language Category

| Language Category | CodeWiki (Sonnet-4) | DeepWiki | Improvement |
|-------------------|---------------------|----------|-------------|
| High-Level (Python, JS, TS) | **79.14%** | 68.67% | **+10.47%** |
| Managed (C#, Java) | **68.84%** | 64.80% | **+4.04%** |
| Systems (C, C++) | 53.24% | 56.39% | -3.15% |
| **Overall Average** | **68.79%** | **64.06%** | **+4.73%** |

### Results on Representative Repositories

| Repository | Language | LOC | CodeWiki-Sonnet-4 | DeepWiki | Improvement |
|------------|----------|-----|-------------------|----------|-------------|
| All-Hands-AI--OpenHands | Python | 229K | **82.45%** | 73.04% | **+9.41%** |
| puppeteer--puppeteer | TypeScript | 136K | **83.00%** | 64.46% | **+18.54%** |
| sveltejs--svelte | JavaScript | 125K | **71.96%** | 68.51% | **+3.45%** |
| Unity-Technologies--ml-agents | C# | 86K | **79.78%** | 74.80% | **+4.98%** |
| elastic--logstash | Java | 117K | **57.90%** | 54.80% | **+3.10%** |

**View comprehensive results:** See [paper](https://arxiv.org/abs/2510.24428) for complete evaluation on 21 repositories spanning all supported languages.

---

## How It Works

### Architecture Overview

CodeWiki employs a three-stage process for comprehensive documentation generation:

1. **Hierarchical Decomposition**: Uses dynamic programming-inspired algorithms to partition repositories into coherent modules while preserving architectural context across multiple granularity levels.

2. **Recursive Multi-Agent Processing**: Implements adaptive multi-agent processing with dynamic task delegation, allowing the system to handle complex modules at scale while maintaining quality.

3. **Multi-Modal Synthesis**: Integrates textual descriptions with visual artifacts including architecture diagrams, data-flow representations, and sequence diagrams for comprehensive understanding.

### Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Codebase      │───▶│  Hierarchical    │───▶│  Multi-Agent    │
│   Analysis      │    │  Decomposition   │    │  Processing     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Visual        │◀───│  Multi-Modal     │◀───│  Structured     │
│   Artifacts     │    │  Synthesis       │    │  Content        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## Requirements

- **Python 3.12+**
- **Node.js** (for Mermaid diagram validation)
- **LLM API access** (Anthropic Claude, OpenAI, etc.)
- **Git** (for branch creation features)

---

## Additional Resources

### Documentation & Guides
- **[Docker Deployment](docker/DOCKER_README.md)** - Containerized deployment instructions
- **[Development Guide](DEVELOPMENT.md)** - Project structure, architecture, and contributing guidelines
- **[CodeWikiBench](https://github.com/FSoft-AI4Code/CodeWikiBench)** - Repository-level documentation benchmark
- **[Live Demo](https://fsoft-ai4code.github.io/codewiki-demo/)** - Interactive demo and examples

### Academic Resources
- **[Paper](https://arxiv.org/abs/2510.24428)** - Full research paper with detailed methodology and results
- **[Citation](#citation)** - How to cite CodeWiki in your research

---

## Citation

If you use CodeWiki in your research, please cite:

```bibtex
@misc{hoang2025codewikievaluatingaisability,
      title={CodeWiki: Evaluating AI's Ability to Generate Holistic Documentation for Large-Scale Codebases},
      author={Anh Nguyen Hoang and Minh Le-Anh and Bach Le and Nghi D. Q. Bui},
      year={2025},
      eprint={2510.24428},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2510.24428},
}
```

---

## Star History

<p align="center">
  <a href="https://star-history.com/#FSoft-AI4Code/CodeWiki&Date">
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=FSoft-AI4Code/CodeWiki&type=Date&theme=dark" />
     <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=FSoft-AI4Code/CodeWiki&type=Date" />
     <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=FSoft-AI4Code/CodeWiki&type=Date" />
   </picture>
  </a>
</p>

---

## License

This project is licensed under the MIT License.
