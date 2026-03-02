"""
cmd_agent_orchestrator.py

Drop-in replacement for AgentOrchestrator + generate_parent_module_docs()
that routes every LLM call through a CLI agent subprocess instead of the
OpenAI API.  This removes all context-window limits from the generation stage.

The CLI agent receives a prompt on **stdin** and is expected to return the
full markdown content on **stdout**.  The caller writes that content to the
appropriate `.md` file.

Example CLI agent:
    claude --dangerously-skip-permissions -p
"""

import json
import logging
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional

from codewiki.src.be.cmd_agent import run_agent_cmd
from codewiki.src.be.prompt_template import (
    format_user_prompt,
    format_system_prompt,
    format_leaf_system_prompt,
    REPO_OVERVIEW_PROMPT,
    MODULE_OVERVIEW_PROMPT,
)
from codewiki.src.be.utils import is_complex_module
from codewiki.src.config import Config, MODULE_TREE_FILENAME, OVERVIEW_FILENAME
from codewiki.src.utils import file_manager
from codewiki.src.be.dependency_analyzer.models.core import Node

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Prompt footer injected so the agent writes docs to stdout rather than files
# ─────────────────────────────────────────────────────────────────────────────
CMD_AGENT_FOOTER = """

---
IMPORTANT OUTPUT INSTRUCTIONS:
- Output ONLY the complete markdown content for the documentation file.
- Do NOT add any preamble, explanation, or commentary before or after the markdown.
- Do NOT use XML/JSON wrappers.  Just raw markdown starting from the first heading.
- Mermaid diagrams are welcome; make sure they are well-formed.
"""

CMD_OVERVIEW_FOOTER = """

---
IMPORTANT OUTPUT INSTRUCTIONS:
Return ONLY the markdown content wrapped exactly as shown:
<OVERVIEW>
…your markdown here…
</OVERVIEW>
"""


def _build_leaf_prompt(
    module_name: str,
    core_component_ids: List[str],
    components: Dict[str, Node],
    module_tree: Dict[str, Any],
    custom_instructions: Optional[str],
    is_complex: bool,
) -> str:
    """Combine system + user prompt into a single string for the CLI agent."""
    if is_complex:
        sys_prompt = format_system_prompt(module_name, custom_instructions)
    else:
        sys_prompt = format_leaf_system_prompt(module_name, custom_instructions)

    user_prompt = format_user_prompt(
        module_name=module_name,
        core_component_ids=core_component_ids,
        components=components,
        module_tree=module_tree,
    )

    return f"{sys_prompt}\n\n{user_prompt}{CMD_AGENT_FOOTER}"


# ─────────────────────────────────────────────────────────────────────────────
class CmdAgentOrchestrator:
    """
    Generates module documentation by piping prompts to a CLI agent subprocess.

    Mirrors the public interface used by DocumentationGenerator so it can be
    used as a drop-in replacement for AgentOrchestrator.
    """

    def __init__(self, config: Config, agent_cmd: str):
        self.config = config
        self.agent_cmd = agent_cmd
        self.custom_instructions = config.get_prompt_addition() if config else None

    # ── leaf / complex module docs ────────────────────────────────────────────
    async def process_module(
        self,
        module_name: str,
        components: Dict[str, Node],
        core_component_ids: List[str],
        module_path: List[str],
        working_dir: str,
    ) -> Dict[str, Any]:
        """Process a single module and write its markdown doc to working_dir."""
        logger.info(f"[CmdAgent] Processing module: {module_name}")

        # Load or create module tree
        module_tree_path = os.path.join(working_dir, MODULE_TREE_FILENAME)
        module_tree = file_manager.load_json(module_tree_path)

        # Skip if already done
        overview_path = os.path.join(working_dir, OVERVIEW_FILENAME)
        if os.path.exists(overview_path):
            logger.info(f"✓ Overview already exists, skipping {module_name}")
            return module_tree

        docs_path = os.path.join(working_dir, f"{module_name}.md")
        if os.path.exists(docs_path):
            logger.info(f"✓ Docs already exist for {module_name} at {docs_path}")
            return module_tree

        try:
            is_complex = is_complex_module(components, core_component_ids)
            prompt = _build_leaf_prompt(
                module_name=module_name,
                core_component_ids=core_component_ids,
                components=components,
                module_tree=module_tree,
                custom_instructions=self.custom_instructions,
                is_complex=is_complex,
            )

            logger.debug(
                f"[CmdAgent] Sending prompt ({len(prompt)} chars) for {module_name}"
            )
            markdown = run_agent_cmd(self.agent_cmd, prompt, cwd=working_dir)

            # Strip accidental wrappers the agent might add
            markdown = _strip_code_fence(markdown)

            file_manager.save_text(markdown, docs_path)
            logger.info(f"[CmdAgent] ✓ Wrote {len(markdown)} chars → {docs_path}")

        except Exception:
            logger.exception(f"[CmdAgent] Failed to process module {module_name}")
            raise

        return module_tree

    # ── parent / overview docs ────────────────────────────────────────────────
    async def generate_parent_module_docs(
        self,
        module_path: List[str],
        working_dir: str,
        module_tree: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate overview docs for a parent module or the whole repo."""
        module_name = (
            module_path[-1]
            if module_path
            else os.path.basename(os.path.normpath(self.config.repo_path))
        )
        logger.info(f"[CmdAgent] Generating parent docs for: {module_name}")

        # Skip if already done
        overview_path = os.path.join(working_dir, OVERVIEW_FILENAME)
        if os.path.exists(overview_path):
            return module_tree

        parent_docs_path = (
            os.path.join(working_dir, f"{module_name}.md")
            if module_path
            else os.path.join(working_dir, OVERVIEW_FILENAME)
        )
        if os.path.exists(parent_docs_path):
            return module_tree

        # Build repo structure with children docs
        repo_structure = _build_overview_structure(
            module_tree, module_path, working_dir
        )

        if module_path:
            prompt = (
                MODULE_OVERVIEW_PROMPT.format(
                    module_name=module_name,
                    repo_structure=json.dumps(repo_structure, indent=4),
                )
                + CMD_OVERVIEW_FOOTER
            )
        else:
            prompt = (
                REPO_OVERVIEW_PROMPT.format(
                    repo_name=module_name,
                    repo_structure=json.dumps(repo_structure, indent=4),
                )
                + CMD_OVERVIEW_FOOTER
            )

        try:
            raw_output = run_agent_cmd(self.agent_cmd, prompt, cwd=working_dir)
            content = _extract_overview(raw_output)
            file_manager.save_text(content, parent_docs_path)
            logger.info(f"[CmdAgent] ✓ Parent docs → {parent_docs_path}")
        except Exception:
            logger.exception(f"[CmdAgent] Failed to generate parent docs for {module_name}")
            raise

        return module_tree


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _strip_code_fence(text: str) -> str:
    """Remove ```markdown … ``` or ``` … ``` wrapper if the agent added one."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # Drop first line (```markdown / ```) and last line (```)
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        return "\n".join(inner).strip()
    return text


def _extract_overview(text: str) -> str:
    """Extract content between <OVERVIEW> … </OVERVIEW> tags, or return raw."""
    if "<OVERVIEW>" in text and "</OVERVIEW>" in text:
        return text.split("<OVERVIEW>")[1].split("</OVERVIEW>")[0].strip()
    return _strip_code_fence(text)


def _build_overview_structure(
    module_tree: Dict[str, Any],
    module_path: List[str],
    working_dir: str,
) -> Dict[str, Any]:
    """Attach children docs to repo structure (mirrors DocumentationGenerator logic)."""
    processed = deepcopy(module_tree)
    module_info = processed

    for part in module_path:
        module_info = module_info[part]
        if part != module_path[-1]:
            module_info = module_info.get("children", {})
        else:
            module_info["is_target_for_overview_generation"] = True

    if "children" in module_info:
        module_info = module_info["children"]

    for child_name, child_info in module_info.items():
        p = os.path.join(working_dir, f"{child_name}.md")
        child_info["docs"] = file_manager.load_text(p) if os.path.exists(p) else ""

    return processed
