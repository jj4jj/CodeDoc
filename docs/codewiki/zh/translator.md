# 翻译器

翻译器负责将文档在生成后翻译成多种语言。

## 概览

翻译器：
1. 从英文输出中读取 Markdown 文件
2. 使用 LLM 翻译内容
3. 将翻译后的文件写入特定语言的目录

## 类定义

```python
class DocTranslator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agent_cmd = config.get("agent_cmd", "")
        self.fallback_models = config.get("fallback_models", [])
```

## 支持的语言

```python
LANGUAGE_NAMES = {
    "zh": "Simplified Chinese (简体中文)",
    "zh-tw": "Traditional Chinese (繁體中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "es": "Spanish (Español)",
    # ... more languages
}
```

## 翻译提示词

```python
TRANSLATION_PROMPT = """You are a professional technical documentation translator.

Translate the following Markdown documentation into {language_name}.

Rules:
- Preserve ALL Markdown formatting (headers, bold, italics, code blocks, tables, links, mermaid diagrams).
- Do NOT translate code block contents, command names, file paths, or proper nouns.
- Keep mermaid diagram source code EXACTLY as-is.
- Do NOT add any extra commentary.

--- BEGIN DOCUMENT ---
{content}
--- END DOCUMENT ---"""
```

## 方法

### translate_docs()

```python
def translate_docs(
    self,
    output_dir: Path,
    lang_code: str,
    progress_callback=None,
    concurrency: int = 4,
) -> Path:
    """Translate all .md files to target language."""

    lang_dir = output_dir / lang_code
    lang_dir.mkdir(parents=True, exist_ok=True)

    # Collect markdown files
    md_files = sorted(output_dir.glob("*.md"))

    # Translate in parallel
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(_translate_one, p): p for p in md_files}
        for future in as_completed(futures):
            future.result()

    # Copy non-markdown files
    for other in output_dir.iterdir():
        if not other.suffix == ".md":
            shutil.copy2(other, lang_dir / other.name)

    return lang_dir
```

## 翻译级联

翻译器采用级联方法：

1. CLI agent 子进程 (`--with-agent-cmd`)
2. 通过 API 调用主模型
3. 通过 API 调用备用模型

## 用法

```bash
# Generate and translate to Chinese
codewiki generate /path/to/repo --output-lang zh

# Generate, translate to Japanese, with HTML
codewiki generate /path/to/repo --output-lang ja --github-pages
```

## 输出结构

```
docs/
├── overview.md           # English
├── module_tree.json
├── core.md
├── zh/                  # Chinese translation
│   ├── overview.md
│   ├── core.md
│   └── module_tree.json
├── ja/                  # Japanese translation
│   └── ...
```

## 相关文档

- [CLI 概览](cli_overview.md)