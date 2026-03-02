"""
Configuration commands for CodeWiki CLI.
"""

import json
import os
import sys
import click
from typing import Optional, List

from codewiki.cli.config_manager import (
    ConfigManager,
    CONFIG_FILE,
    ENV_API_KEY, ENV_BASE_URL, ENV_MAIN_MODEL, ENV_CLUSTER_MODEL, ENV_FALLBACK_MODEL,
)
from codewiki.cli.models.config import AgentInstructions
from codewiki.cli.utils.errors import (
    ConfigurationError, 
    handle_error, 
    EXIT_SUCCESS,
    EXIT_CONFIG_ERROR
)
from codewiki.cli.utils.validation import (
    validate_url,
    validate_api_key,
    validate_model_name,
    is_top_tier_model,
    mask_api_key
)


def parse_patterns(patterns_str: str) -> List[str]:
    """Parse comma-separated patterns into a list."""
    if not patterns_str:
        return []
    return [p.strip() for p in patterns_str.split(',') if p.strip()]


@click.group(name="config")
def config_group():
    """Manage CodeWiki configuration (API credentials and settings)."""
    pass


@config_group.command(name="set")
@click.option(
    "--api-key",
    type=str,
    help=(
        "LLM API key. Stored in system keychain if available, "
        "otherwise saved in ~/.codewiki/config.json. "
        "Can also be set via CODEWIKI_API_KEY env var."
    )
)
@click.option(
    "--base-url",
    type=str,
    help="LLM API base URL (e.g., https://api.deepseek.com). Env: CODEWIKI_BASE_URL"
)
@click.option(
    "--main-model",
    type=str,
    help="Primary model for documentation generation. Env: CODEWIKI_MAIN_MODEL"
)
@click.option(
    "--cluster-model",
    type=str,
    help="Model for module clustering (recommend top-tier). Env: CODEWIKI_CLUSTER_MODEL"
)
@click.option(
    "--fallback-models",
    type=str,
    default=None,
    help=(
        "Comma-separated ordered list of fallback models to try when the main model fails. "
        "Example: 'deepseek-chat,deepseek-reasoner'. Env: CODEWIKI_FALLBACK_MODEL"
    ),
)
@click.option(
    "--save-key-to-file",
    is_flag=True,
    default=False,
    help=(
        "Force API key to be saved in ~/.codewiki/config.json "
        "instead of the system keychain. Useful in CI or headless environments."
    ),
)
@click.option(
    "--max-tokens",
    type=int,
    help="Maximum tokens for LLM response (default: 32768)"
)
@click.option(
    "--max-token-per-module",
    type=int,
    help="Maximum tokens per module for clustering (default: 36369)"
)
@click.option(
    "--max-token-per-leaf-module",
    type=int,
    help="Maximum tokens per leaf module (default: 16000)"
)
@click.option(
    "--max-depth",
    type=int,
    help="Maximum depth for hierarchical decomposition (default: 2)"
)
def config_set(
    api_key: Optional[str],
    base_url: Optional[str],
    main_model: Optional[str],
    cluster_model: Optional[str],
    fallback_models: Optional[str],
    max_tokens: Optional[int],
    max_token_per_module: Optional[int],
    max_token_per_leaf_module: Optional[int],
    max_depth: Optional[int],
    save_key_to_file: bool,
):
    """
    Set configuration values for CodeWiki.
    
    API keys are resolved in priority order:
      1. Environment variable  CODEWIKI_API_KEY
      2. Config file           ~/.codewiki/config.json  (api_key field)
      3. System keychain       (macOS Keychain / GNOME Keyring / KWallet)
    
    Other overridable env vars:
      CODEWIKI_BASE_URL, CODEWIKI_MAIN_MODEL,
      CODEWIKI_CLUSTER_MODEL, CODEWIKI_FALLBACK_MODEL
    
    Examples:
    
    \b
    # Set via CLI (stores to keychain or config file)
    $ codewiki config set --api-key sk-abc123 --base-url https://api.deepseek.com \\
        --main-model deepseek-chat --cluster-model deepseek-chat --fallback-models deepseek-chat
    
    \b
    # Use environment variables instead (no config set needed)
    $ export CODEWIKI_API_KEY=sk-abc123
    $ export CODEWIKI_BASE_URL=https://api.deepseek.com
    $ export CODEWIKI_MAIN_MODEL=deepseek-chat
    $ export CODEWIKI_CLUSTER_MODEL=deepseek-chat
    $ codewiki generate
    
    \b
    # Update only max tokens
    $ codewiki config set --max-tokens 4096

    \b
    # Force API key into config file (no keychain)
    $ codewiki config set --api-key sk-xxx --save-key-to-file
    """
    try:
        # Check if at least one option is provided
        if not any([api_key, base_url, main_model, cluster_model, fallback_models, max_tokens, max_token_per_module, max_token_per_leaf_module, max_depth]):
            click.echo("No options provided. Use --help for usage information.")
            sys.exit(EXIT_CONFIG_ERROR)

        # Validate inputs before saving
        validated_data = {}
        fallback_models_list: Optional[List[str]] = None
        
        if api_key:
            validated_data['api_key'] = validate_api_key(api_key)
        
        if base_url:
            validated_data['base_url'] = validate_url(base_url)
        
        if main_model:
            validated_data['main_model'] = validate_model_name(main_model)
        
        if cluster_model:
            validated_data['cluster_model'] = validate_model_name(cluster_model)

        if fallback_models:
            fallback_models_list = [m.strip() for m in fallback_models.split(',') if m.strip()]
            if not fallback_models_list:
                raise ConfigurationError("fallback_models must contain at least one valid model name")
            validated_data['fallback_models'] = [validate_model_name(m) for m in fallback_models_list]
        
        if max_tokens is not None:
            if max_tokens < 1:
                raise ConfigurationError("max_tokens must be a positive integer")
            validated_data['max_tokens'] = max_tokens
        
        if max_token_per_module is not None:
            if max_token_per_module < 1:
                raise ConfigurationError("max_token_per_module must be a positive integer")
            validated_data['max_token_per_module'] = max_token_per_module
        
        if max_token_per_leaf_module is not None:
            if max_token_per_leaf_module < 1:
                raise ConfigurationError("max_token_per_leaf_module must be a positive integer")
            validated_data['max_token_per_leaf_module'] = max_token_per_leaf_module
        
        if max_depth is not None:
            if max_depth < 1:
                raise ConfigurationError("max_depth must be a positive integer")
            validated_data['max_depth'] = max_depth
        
        # Create config manager and save
        manager = ConfigManager()
        manager.load()  # Load existing config if present

        manager.save(
            api_key=validated_data.get('api_key'),
            base_url=validated_data.get('base_url'),
            main_model=validated_data.get('main_model'),
            cluster_model=validated_data.get('cluster_model'),
            fallback_models=validated_data.get('fallback_models'),
            max_tokens=validated_data.get('max_tokens'),
            max_token_per_module=validated_data.get('max_token_per_module'),
            max_token_per_leaf_module=validated_data.get('max_token_per_leaf_module'),
            max_depth=validated_data.get('max_depth'),
            force_key_to_file=save_key_to_file,
        )
        
        # Display success messages
        click.echo()
        if api_key:
            if save_key_to_file:
                click.secho("✓ API key saved to config file (~/.codewiki/config.json)", fg="green")
            elif manager.keyring_available:
                click.secho("✓ API key saved to system keychain", fg="green")
            else:
                click.secho(
                    "⚠️  System keychain unavailable. API key saved to config file (~/.codewiki/config.json).",
                    fg="yellow"
                )
        
        if base_url:
            click.secho(f"✓ Base URL: {base_url}", fg="green")
        
        if main_model:
            click.secho(f"✓ Main model: {main_model}", fg="green")
        
        if cluster_model:
            click.secho(f"✓ Cluster model: {cluster_model}", fg="green")
            
            # Warn if not using top-tier model for clustering
            if not is_top_tier_model(cluster_model):
                click.secho(
                    "\n⚠️  Cluster model is not a top-tier LLM. "
                    "Documentation quality may be suboptimal.",
                    fg="yellow"
                )
                click.echo(
                    "   Recommended models: claude-opus, claude-sonnet-4, gpt-4, gpt-4-turbo"
                )
        
        if validated_data.get('fallback_models'):
            click.secho(
                f"✓ Fallback models: {', '.join(validated_data['fallback_models'])}",
                fg="green",
            )
        
        if max_tokens:
            click.secho(f"✓ Max tokens: {max_tokens}", fg="green")
        
        if max_token_per_module:
            click.secho(f"✓ Max token per module: {max_token_per_module}", fg="green")
        
        if max_token_per_leaf_module:
            click.secho(f"✓ Max token per leaf module: {max_token_per_leaf_module}", fg="green")
        
        if max_depth:
            click.secho(f"✓ Max depth: {max_depth}", fg="green")
        
        click.echo("\n" + click.style("Configuration updated successfully.", fg="green", bold=True))
        
    except ConfigurationError as e:
        click.secho(f"\n✗ Configuration error: {e.message}", fg="red", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        sys.exit(handle_error(e))


@config_group.command(name="show")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output in JSON format"
)
def config_show(output_json: bool):
    """
    Display current configuration.
    
    API keys are masked for security (showing only first and last 4 characters).
    
    Examples:
    
    \b
    # Display configuration
    $ codewiki config show
    
    \b
    # Display as JSON
    $ codewiki config show --json
    """
    try:
        manager = ConfigManager()
        
        if not manager.load_or_env():
            click.secho("\n✗ Configuration not found.", fg="red", err=True)
            click.echo("\nPlease run 'codewiki config set' or set environment variables:")
            click.echo(f"  export {ENV_API_KEY}=<your-api-key>")
            click.echo(f"  export {ENV_BASE_URL}=<api-url>")
            click.echo(f"  export {ENV_MAIN_MODEL}=<model>")
            click.echo(f"  export {ENV_CLUSTER_MODEL}=<model>")
            click.echo("\nFor more help: codewiki config set --help")
            sys.exit(EXIT_CONFIG_ERROR)
        
        config = manager.get_config()
        api_key = manager.get_api_key()
        
        if output_json:
            # JSON output
            output = {
                "api_key": mask_api_key(api_key) if api_key else "Not set",
                "api_key_storage": "keychain" if manager.keyring_available else "encrypted_file",
                "base_url": config.base_url if config else "",
                "main_model": config.main_model if config else "",
                "cluster_model": config.cluster_model if config else "",
                "fallback_model": config.fallback_model if config else "glm-4p5",
                "default_output": config.default_output if config else "docs",
                "max_tokens": config.max_tokens if config else 32768,
                "max_token_per_module": config.max_token_per_module if config else 36369,
                "max_token_per_leaf_module": config.max_token_per_leaf_module if config else 16000,
                "max_depth": config.max_depth if config else 2,
                "agent_instructions": config.agent_instructions.to_dict() if config and config.agent_instructions else {},
                "config_file": str(manager.config_file_path)
            }
            click.echo(json.dumps(output, indent=2))
        else:
            # Human-readable output
            click.echo()
            click.secho("CodeWiki Configuration", fg="blue", bold=True)
            click.echo("━" * 40)
            click.echo()
            
            click.secho("Credentials", fg="cyan", bold=True)
            if api_key:
                # Show source using the same priority as load()
                if os.environ.get(ENV_API_KEY):
                    source = "env var (CODEWIKI_API_KEY)"
                elif config and getattr(config, 'api_key', None):
                    source = "config file (~/.codewiki/config.json)"
                elif manager.keyring_available:
                    source = "system keychain"
                else:
                    source = "config file"
                click.echo(f"  API Key:          {mask_api_key(api_key)} ({source})")
            else:
                click.secho("  API Key:          Not set", fg="yellow")
            
            click.echo()
            click.secho("API Settings", fg="cyan", bold=True)
            if config:
                def _src(env_var, val):
                    return f"{val}  [env]" if os.environ.get(env_var) else val
                click.echo(f"  Base URL:         {_src(ENV_BASE_URL, config.base_url or 'Not set')}")
                click.echo(f"  Main Model:       {_src(ENV_MAIN_MODEL, config.main_model or 'Not set')}")
                click.echo(f"  Cluster Model:    {_src(ENV_CLUSTER_MODEL, config.cluster_model or 'Not set')}")
                fallback_display = ', '.join(config.fallback_models) if config.fallback_models else (config.fallback_model or 'same as main')
                click.echo(f"  Fallback Models:  {_src(ENV_FALLBACK_MODEL, fallback_display)}")
            else:
                click.secho("  Not configured", fg="yellow")
            
            click.echo()
            click.secho("Output Settings", fg="cyan", bold=True)
            if config:
                click.echo(f"  Default Output:   {config.default_output}")
            
            click.echo()
            click.secho("Token Settings", fg="cyan", bold=True)
            if config:
                click.echo(f"  Max Tokens:              {config.max_tokens}")
                click.echo(f"  Max Token/Module:        {config.max_token_per_module}")
                click.echo(f"  Max Token/Leaf Module:   {config.max_token_per_leaf_module}")
            
            click.echo()
            click.secho("Decomposition Settings", fg="cyan", bold=True)
            if config:
                click.echo(f"  Max Depth:               {config.max_depth}")
            
            click.echo()
            click.secho("Agent Instructions", fg="cyan", bold=True)
            if config and config.agent_instructions and not config.agent_instructions.is_empty():
                agent = config.agent_instructions
                if agent.include_patterns:
                    click.echo(f"  Include patterns:   {', '.join(agent.include_patterns)}")
                if agent.exclude_patterns:
                    click.echo(f"  Exclude patterns:   {', '.join(agent.exclude_patterns)}")
                if agent.focus_modules:
                    click.echo(f"  Focus modules:      {', '.join(agent.focus_modules)}")
                if agent.doc_type:
                    click.echo(f"  Doc type:           {agent.doc_type}")
                if agent.custom_instructions:
                    click.echo(f"  Custom instructions: {agent.custom_instructions[:50]}...")
            else:
                click.secho("  Using defaults (no custom settings)", fg="yellow")
            
            click.echo()
            click.echo(f"Configuration file: {manager.config_file_path}")
            click.echo()
        
    except Exception as e:
        sys.exit(handle_error(e))


@config_group.command(name="validate")
@click.option(
    "--quick",
    is_flag=True,
    help="Skip API connectivity test"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed validation steps"
)
def config_validate(quick: bool, verbose: bool):
    """
    Validate configuration and test LLM API connectivity.
    
    Checks:
      • Configuration file exists and is valid
      • API key is present
      • API settings are correctly formatted
      • (Optional) API connectivity test
    
    Examples:
    
    \b
    # Full validation with API test
    $ codewiki config validate
    
    \b
    # Quick validation (config only)
    $ codewiki config validate --quick
    
    \b
    # Verbose output
    $ codewiki config validate --verbose
    """
    try:
        click.echo()
        click.secho("Validating configuration...", fg="blue", bold=True)
        click.echo()
        
        manager = ConfigManager()
        
        # Step 1: Check config file or env vars
        if verbose:
            click.echo("[1/5] Checking configuration source...")
            click.echo(f"      Config file: {manager.config_file_path}")
        
        file_loaded = CONFIG_FILE.exists() and manager.load()
        env_complete = manager._env_only_config() is not None
        
        if not file_loaded and not env_complete:
            click.secho("✗ Configuration file not found and no env vars set", fg="red")
            click.echo()
            click.echo(f"  Set env vars: {ENV_API_KEY}, {ENV_BASE_URL}, {ENV_MAIN_MODEL}, {ENV_CLUSTER_MODEL}")
            click.echo("  Or run: codewiki config set --help")
            sys.exit(EXIT_CONFIG_ERROR)
        
        if not file_loaded and env_complete:
            # Env-var-only mode: synthesize config from env
            manager._config = manager._env_only_config()
        
        if verbose:
            src = "env vars" if not file_loaded else "config file"
            click.secho(f"      ✓ Config source: {src}", fg="green")
        else:
            click.secho("✓ Configuration file exists", fg="green")
        
        # Step 2: Check API key
        if verbose:
            click.echo()
            click.echo("[2/5] Checking API key...")
            storage = "system keychain" if manager.keyring_available else "encrypted file"
            click.echo(f"      Storage: {storage}")
        
        api_key = manager.get_api_key()
        if not api_key:
            click.secho("✗ API key missing", fg="red")
            click.echo()
            click.echo(f"Error: API key not set. Run 'codewiki config set --api-key <key>' or set {ENV_API_KEY} env var.")
            sys.exit(EXIT_CONFIG_ERROR)
        
        if verbose:
            src = f"env ({ENV_API_KEY})" if os.environ.get(ENV_API_KEY) else ("keychain" if manager.keyring_available else "config file")
            click.secho(f"      ✓ API key retrieved (source: {src})", fg="green")
            click.secho(f"      ✓ Length: {len(api_key)} characters", fg="green")
        else:
            src = f"env var" if os.environ.get(ENV_API_KEY) else ("keychain" if manager.keyring_available else "config file")
            click.secho(f"✓ API key present (source: {src})", fg="green")
        
        # Step 3: Check base URL
        config = manager.get_config()
        if verbose:
            click.echo()
            click.echo("[3/5] Checking base URL...")
            click.echo(f"      URL: {config.base_url}")
        
        if not config.base_url:
            click.secho("✗ Base URL not set", fg="red")
            sys.exit(EXIT_CONFIG_ERROR)
        
        try:
            validate_url(config.base_url)
            if verbose:
                click.secho("      ✓ Valid HTTPS URL", fg="green")
            else:
                click.secho(f"✓ Base URL valid: {config.base_url}", fg="green")
        except ConfigurationError as e:
            click.secho(f"✗ Invalid base URL: {e.message}", fg="red")
            sys.exit(EXIT_CONFIG_ERROR)
        
        # Step 4: Check models
        if verbose:
            click.echo()
            click.echo("[4/5] Checking model configuration...")
            click.echo(f"      main_model:    {config.main_model or '(not set)'}")
            click.echo(f"      cluster_model: {config.cluster_model or '(not set)'}")
            click.echo(f"      fallback_model:{config.fallback_model or '(not set, optional)'}")

        missing_models = []
        if not config.main_model:
            missing_models.append("main_model")
        if not config.cluster_model:
            missing_models.append("cluster_model")

        if missing_models:
            click.secho("✗ Models not configured. Missing keys:", fg="red")
            for key in missing_models:
                click.secho(f"    - {key}: not set", fg="red")
            click.echo()
            click.echo("  Fix with:")
            example_models = " \\\n    ".join(
                f"--{k.replace('_', '-')} <model-name>" for k in missing_models
            )
            click.secho(f"    codewiki config set {example_models}", fg="cyan")
            click.echo()
            click.echo("  Example (DeepSeek):")
            click.secho(
                "    codewiki config set --main-model deepseek-chat --cluster-model deepseek-chat",
                fg="cyan"
            )
            sys.exit(EXIT_CONFIG_ERROR)

        if verbose:
            click.secho("      ✓ Models configured", fg="green")
        else:
            click.secho(f"✓ Main model:    {config.main_model}", fg="green")
            click.secho(f"✓ Cluster model: {config.cluster_model}", fg="green")
            fb = ', '.join(config.fallback_models) if getattr(config, 'fallback_models', []) else config.fallback_model
            if fb:
                click.secho(f"✓ Fallback models: {fb}", fg="green")
            else:
                click.secho("  Fallback models: (same as main)", fg="bright_black")
        
        # Warn about non-top-tier cluster model
        if not is_top_tier_model(config.cluster_model):
            click.secho(
                "⚠️  Cluster model is not top-tier. Consider using claude-sonnet-4 or gpt-4.",
                fg="yellow"
            )
        
        # Step 5: API connectivity test (unless --quick)
        if not quick:
            click.echo("  Testing API connectivity... ", nl=False)
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key, base_url=config.base_url)
                # Use a minimal chat completion instead of models.list() because
                # many providers don't implement the /models endpoint.
                client.chat.completions.create(
                    model=config.main_model,
                    messages=[{"role": "user", "content": "hi"}],
                    max_tokens=1,
                )
                click.secho("✓ API connectivity test successful", fg="green")
            except Exception as e:
                err_msg = str(e)
                # Shorten very long openai error bodies
                if len(err_msg) > 300:
                    err_msg = err_msg[:300] + "…"
                click.secho("✗ failed", fg="red")
                click.secho(f"  Error: {err_msg}", fg="red")
                click.echo()
                click.echo("  Tip: use --quick to skip the connectivity test if")
                click.echo("       you trust your credentials are correct.")
                sys.exit(EXIT_CONFIG_ERROR)
        
        # Success
        click.echo()
        click.secho("✓ Configuration is valid!", fg="green", bold=True)
        click.echo()
        
    except ConfigurationError as e:
        click.secho(f"\n✗ Configuration error: {e.message}", fg="red", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        sys.exit(handle_error(e, verbose=verbose))


@config_group.command(name="agent")
@click.option(
    "--include",
    "-i",
    type=str,
    default=None,
    help="Comma-separated file patterns to include (e.g., '*.cs,*.py')",
)
@click.option(
    "--exclude",
    "-e",
    type=str,
    default=None,
    help="Comma-separated patterns to exclude (e.g., '*Tests*,*Specs*')",
)
@click.option(
    "--focus",
    "-f",
    type=str,
    default=None,
    help="Comma-separated modules/paths to focus on (e.g., 'src/core,src/api')",
)
@click.option(
    "--doc-type",
    "-t",
    type=click.Choice(['api', 'architecture', 'user-guide', 'developer'], case_sensitive=False),
    default=None,
    help="Default type of documentation to generate",
)
@click.option(
    "--instructions",
    type=str,
    default=None,
    help="Custom instructions for the documentation agent",
)
@click.option(
    "--clear",
    is_flag=True,
    help="Clear all agent instructions",
)
def config_agent(
    include: Optional[str],
    exclude: Optional[str],
    focus: Optional[str],
    doc_type: Optional[str],
    instructions: Optional[str],
    clear: bool
):
    """
    Configure default agent instructions for documentation generation.
    
    These settings are used as defaults when running 'codewiki generate'.
    Runtime options (--include, --exclude, etc.) override these defaults.
    
    Examples:
    
    \b
    # Set include patterns for C# projects
    $ codewiki config agent --include "*.cs"
    
    \b
    # Exclude test projects
    $ codewiki config agent --exclude "*Tests*,*Specs*,test_*"
    
    \b
    # Focus on specific modules
    $ codewiki config agent --focus "src/core,src/api"
    
    \b
    # Set default doc type
    $ codewiki config agent --doc-type architecture
    
    \b
    # Add custom instructions
    $ codewiki config agent --instructions "Focus on public APIs and include usage examples"
    
    \b
    # Clear all agent instructions
    $ codewiki config agent --clear
    """
    try:
        manager = ConfigManager()
        
        if not manager.load():
            click.secho("\n✗ Configuration not found.", fg="red", err=True)
            click.echo("\nPlease run 'codewiki config set' first to configure your API credentials.")
            sys.exit(EXIT_CONFIG_ERROR)
        
        config = manager.get_config()
        
        if clear:
            # Clear all agent instructions
            config.agent_instructions = AgentInstructions()
            manager.save()
            click.echo()
            click.secho("✓ Agent instructions cleared", fg="green")
            click.echo()
            return
        
        # Check if at least one option is provided
        if not any([include, exclude, focus, doc_type, instructions]):
            # Display current settings
            click.echo()
            click.secho("Agent Instructions", fg="blue", bold=True)
            click.echo("━" * 40)
            click.echo()
            
            agent = config.agent_instructions
            if agent and not agent.is_empty():
                if agent.include_patterns:
                    click.echo(f"  Include patterns:   {', '.join(agent.include_patterns)}")
                if agent.exclude_patterns:
                    click.echo(f"  Exclude patterns:   {', '.join(agent.exclude_patterns)}")
                if agent.focus_modules:
                    click.echo(f"  Focus modules:      {', '.join(agent.focus_modules)}")
                if agent.doc_type:
                    click.echo(f"  Doc type:           {agent.doc_type}")
                if agent.custom_instructions:
                    click.echo(f"  Custom instructions: {agent.custom_instructions}")
            else:
                click.secho("  No agent instructions configured (using defaults)", fg="yellow")
            
            click.echo()
            click.echo("Use 'codewiki config agent --help' for usage information.")
            click.echo()
            return
        
        # Update agent instructions
        current = config.agent_instructions or AgentInstructions()
        
        if include is not None:
            current.include_patterns = parse_patterns(include) if include else None
        if exclude is not None:
            current.exclude_patterns = parse_patterns(exclude) if exclude else None
        if focus is not None:
            current.focus_modules = parse_patterns(focus) if focus else None
        if doc_type is not None:
            current.doc_type = doc_type if doc_type else None
        if instructions is not None:
            current.custom_instructions = instructions if instructions else None
        
        config.agent_instructions = current
        manager.save()
        
        # Display success messages
        click.echo()
        if include:
            click.secho(f"✓ Include patterns: {parse_patterns(include)}", fg="green")
        if exclude:
            click.secho(f"✓ Exclude patterns: {parse_patterns(exclude)}", fg="green")
        if focus:
            click.secho(f"✓ Focus modules: {parse_patterns(focus)}", fg="green")
        if doc_type:
            click.secho(f"✓ Doc type: {doc_type}", fg="green")
        if instructions:
            click.secho(f"✓ Custom instructions set", fg="green")
        
        click.echo("\n" + click.style("Agent instructions updated successfully.", fg="green", bold=True))
        click.echo()
        
    except ConfigurationError as e:
        click.secho(f"\n✗ Configuration error: {e.message}", fg="red", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        sys.exit(handle_error(e))
