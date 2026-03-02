"""
Post-generation translation step for `codewiki generate --output-lang`.

Reads every .md file from the English output directory, asks the LLM to
translate the content into the target language, and writes the result to
output_dir/<lang_code>/ keeping the same filenames.

Non-markdown files (JSON, etc.) are copied as-is so that tooling that depends
on metadata continues to work.
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

logger = logging.getLogger(__name__)

# Human-readable language names keyed by common lang codes
LANGUAGE_NAMES: Dict[str, str] = {
    "zh": "Simplified Chinese (简体中文)",
    "zh-tw": "Traditional Chinese (繁體中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "es": "Spanish (Español)",
    "pt": "Portuguese (Português)",
    "ru": "Russian (Русский)",
    "ar": "Arabic (العربية)",
    "hi": "Hindi (हिन्दी)",
    "it": "Italian (Italiano)",
}

TRANSLATION_PROMPT = """You are a professional technical documentation translator.

Translate the following Markdown documentation into {language_name}.

Rules:
- Preserve ALL Markdown formatting (headers, bold, italics, code blocks, tables, links, mermaid diagrams).
- Do NOT translate code block contents, command names, file paths, or proper nouns (model names, package names, etc.).
- Keep mermaid diagram source code EXACTLY as-is (only translate the surrounding text if any).
- Do NOT add any extra commentary, preamble, or explanation — output ONLY the translated markdown.

--- BEGIN DOCUMENT ---
{content}
--- END DOCUMENT ---"""


class DocTranslator:
    """
    Translates generated markdown documentation into another language using
    the same LLM and credentials used for documentation generation.

    Translation cascade (first success wins):
    1. CLI agent subprocess (--with-agent-cmd) — no timeout / context limits
    2. Main model via API
    3. Fallback models via API
    4. Error → stop
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: Same dict passed to CLIDocumentationGenerator
                    (must contain base_url, api_key, main_model, max_tokens).
                    Optional: agent_cmd, fallback_models.
        """
        self.config = config
        self.agent_cmd: str = config.get("agent_cmd", "")
        self.fallback_models: List[str] = config.get("fallback_models", [])
        self._backend_config = None

    def _get_backend_config(self):
        """Lazily create a BackendConfig from the CLI config dict."""
        if self._backend_config is None:
            from codewiki.src.config import Config as BackendConfig
            self._backend_config = BackendConfig.from_cli(
                repo_path=".",           # not used for translation
                output_dir=".",          # not used for translation
                llm_base_url=self.config.get("base_url"),
                llm_api_key=self.config.get("api_key"),
                main_model=self.config.get("main_model"),
                cluster_model=self.config.get("cluster_model", self.config.get("main_model")),
                fallback_model=self.config.get("fallback_model", self.config.get("main_model")),
                max_tokens=self.config.get("max_tokens", 4096),
                max_token_per_module=self.config.get("max_token_per_module", 36369),
                max_token_per_leaf_module=self.config.get("max_token_per_leaf_module", 16000),
                max_depth=self.config.get("max_depth", 2),
            )
        return self._backend_config

    def _translate_content(self, content: str, lang_code: str, filename: str = "") -> str:
        """
        Translate a single markdown string.

        Cascade order:
        1. agent_cmd (if set)
        2. main_model via API (timeout=300s) 
        3. each fallback model via API
        4. raise on total failure
        """
        language_name = LANGUAGE_NAMES.get(lang_code.lower(), lang_code)
        prompt = TRANSLATION_PROMPT.format(
            language_name=language_name,
            content=content,
        )
        errors: List[str] = []

        # -- 1. CLI agent subprocess --
        if self.agent_cmd:
            try:
                from codewiki.src.be.cmd_agent import run_agent_cmd
                result = run_agent_cmd(self.agent_cmd, prompt)
                if result and result.strip():
                    return result
                errors.append("agent_cmd returned empty output")
            except Exception as e:
                errors.append(f"agent_cmd: {e}")
                logger.warning(f"  agent_cmd failed for {filename}: {e}")

        # -- 2. Main model via API --
        try:
            from codewiki.src.be.llm_services import call_llm
            return call_llm(prompt, self._get_backend_config(), timeout=300)
        except Exception as e:
            errors.append(f"main_model ({self.config.get('main_model')}): {e}")
            logger.warning(f"  main_model failed for {filename}: {e}")

        # -- 3. Fallback models --
        for fb_model in self.fallback_models:
            try:
                from codewiki.src.be.llm_services import call_llm
                return call_llm(
                    prompt, self._get_backend_config(),
                    model=fb_model, timeout=300,
                )
            except Exception as e:
                errors.append(f"fallback ({fb_model}): {e}")
                logger.warning(f"  fallback {fb_model} failed for {filename}: {e}")

        # -- All failed --
        all_errors = "\n    ".join(errors)
        raise RuntimeError(
            f"Translation failed for {filename}. All backends exhausted:\n    {all_errors}"
        )

    def translate_docs(
        self,
        output_dir: Path,
        lang_code: str,
        progress_callback=None,
        concurrency: int = 4,
    ) -> Path:
        """
        Translate all .md files in *output_dir* into *lang_code* and write
        results to *output_dir/<lang_code>/*.

        Stops on first unrecoverable translation failure.

        Args:
            output_dir:        Root docs directory (e.g. /tmp/bifrost/docs)
            lang_code:         Target language code (e.g. 'zh', 'ja')
            progress_callback: Optional callable(current, total, filename)
            concurrency:       Number of parallel translation workers (default 4)

        Returns:
            Path to the translated output directory.

        Raises:
            RuntimeError: If any file fails to translate after all fallbacks.
        """
        lang_dir = output_dir / lang_code
        lang_dir.mkdir(parents=True, exist_ok=True)

        # Collect markdown files (top-level only, same structure as generated docs)
        md_files: List[Path] = sorted(output_dir.glob("*.md"))
        total = len(md_files)

        logger.info(f"Translating {total} markdown files -> {lang_dir} (concurrency={concurrency})")

        # Thread-safe progress counter
        progress_lock = threading.Lock()
        progress_counter = [0]

        def _translate_one(md_path: Path) -> None:
            """Translate a single file (runs inside a thread)."""
            dest = lang_dir / md_path.name

            # Skip already-translated files (checkpoint resume)
            if dest.exists():
                with progress_lock:
                    progress_counter[0] += 1
                    idx = progress_counter[0]
                if progress_callback:
                    progress_callback(idx, total, f"\u21a9 {md_path.name} (skip)")
                return

            with progress_lock:
                progress_counter[0] += 1
                idx = progress_counter[0]
            if progress_callback:
                progress_callback(idx, total, md_path.name)

            content = md_path.read_text(encoding="utf-8")
            translated = self._translate_content(content, lang_code, md_path.name)
            dest.write_text(translated, encoding="utf-8")

        # Run translations in parallel
        workers = max(1, min(concurrency, total))
        if workers == 1:
            # Serial path — no thread overhead
            for md_path in md_files:
                _translate_one(md_path)
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {pool.submit(_translate_one, p): p for p in md_files}
                for future in as_completed(futures):
                    # Re-raise any translation error immediately
                    future.result()

        # Copy non-markdown artefacts (JSON metadata, etc.) unchanged
        for other in output_dir.iterdir():
            if other.is_file() and not other.suffix == ".md" and other.name not in {"index.html"}:
                try:
                    shutil.copy2(other, lang_dir / other.name)
                except Exception:
                    pass

        return lang_dir
