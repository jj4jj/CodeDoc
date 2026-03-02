"""
Configuration manager with flexible credential storage.

Priority order for credentials and settings:
  1. Environment variables  (CODEWIKI_API_KEY, CODEWIKI_BASE_URL, etc.)
  2. Config file            (~/.codewiki/config.json  – api_key field)
  3. System keychain        (macOS Keychain / Linux Secret Service)

This allows headless / CI environments to work without a GUI keychain.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional

import keyring
from keyring.errors import KeyringError

from codewiki.cli.models.config import Configuration
from codewiki.cli.utils.errors import ConfigurationError, FileSystemError
from codewiki.cli.utils.fs import ensure_directory, safe_write, safe_read

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment variable names
# ---------------------------------------------------------------------------
ENV_API_KEY       = "CODEWIKI_API_KEY"
ENV_BASE_URL      = "CODEWIKI_BASE_URL"
ENV_MAIN_MODEL    = "CODEWIKI_MAIN_MODEL"
ENV_CLUSTER_MODEL = "CODEWIKI_CLUSTER_MODEL"
ENV_FALLBACK_MODEL = "CODEWIKI_FALLBACK_MODEL"

# ---------------------------------------------------------------------------
# Keyring & file paths
# ---------------------------------------------------------------------------
KEYRING_SERVICE          = "codewiki"
KEYRING_API_KEY_ACCOUNT  = "api_key"

CONFIG_DIR     = Path.home() / ".codewiki"
CONFIG_FILE    = CONFIG_DIR / "config.json"
CONFIG_VERSION = "1.0"


class ConfigManager:
    """
    Manages CodeWiki configuration with a triple-fallback credential chain:

      1. Environment variables  →  highest priority, no file system required
      2. Config file            →  api_key stored plaintext in config.json
                                   (used when keychain is unavailable)
      3. System keychain        →  secure storage when available

    Other settings (base_url, models, tokens) can also be overridden at
    runtime via environment variables without running `codewiki config set`.
    """

    def __init__(self):
        self._api_key: Optional[str] = None
        self._config: Optional[Configuration] = None
        self._keyring_available = self._check_keyring_available()

    # ------------------------------------------------------------------
    # Keyring helper
    # ------------------------------------------------------------------

    def _check_keyring_available(self) -> bool:
        """Return True if the system keyring is usable."""
        try:
            keyring.get_password(KEYRING_SERVICE, "__test__")
            return True
        except KeyringError:
            return False

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    def load(self) -> bool:
        """
        Load configuration from file and resolve credentials.

        Returns True if a config file exists (even if credentials come from
        env vars), False if no config file is present at all.
        """
        if not CONFIG_FILE.exists():
            # Config file absent – but env vars might still make us functional
            return False

        try:
            content = safe_read(CONFIG_FILE)
            data = json.loads(content)
            self._config = Configuration.from_dict(data)

            # ── API key resolution (highest → lowest priority) ──────────────
            # 1. Environment variable (always wins)
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except:
                pass
            env_key = os.environ.get(ENV_API_KEY)
            if env_key:
                self._api_key = env_key
                return True

            # 2. Explicit api_key field in config.json (user edited the file)
            if self._config.api_key:
                self._api_key = self._config.api_key
                return True

            # 3. System keychain (set via `codewiki config set`)
            if self._keyring_available:
                try:
                    keyring_key = keyring.get_password(KEYRING_SERVICE, KEYRING_API_KEY_ACCOUNT)
                    if keyring_key:
                        self._api_key = keyring_key
                except KeyringError:
                    pass

            return True
        except (json.JSONDecodeError, FileSystemError) as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def save(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        main_model: Optional[str] = None,
        cluster_model: Optional[str] = None,
        fallback_model: Optional[str] = None,
        fallback_models: Optional[list] = None,
        default_output: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_token_per_module: Optional[int] = None,
        max_token_per_leaf_module: Optional[int] = None,
        max_depth: Optional[int] = None,
        force_key_to_file: bool = False,
    ):
        """
        Persist configuration.

        API key storage:
          - If force_key_to_file=True: always saved to config.json (plaintext)
          - Primary:  system keychain  (when available and force_key_to_file=False)
          - Fallback: api_key field in config.json  (plaintext, CI-friendly)
        """
        try:
            ensure_directory(CONFIG_DIR)
        except FileSystemError as e:
            raise ConfigurationError(f"Cannot create config directory: {e}")

        # Bootstrap config object if needed
        if self._config is None:
            if CONFIG_FILE.exists():
                self.load()
            else:
                from codewiki.cli.models.config import AgentInstructions
                self._config = Configuration(
                    base_url="",
                    main_model="",
                    cluster_model="",
                    fallback_model="glm-4p5",
                    default_output="docs",
                    agent_instructions=AgentInstructions(),
                )

        # Update fields
        if base_url       is not None: self._config.base_url       = base_url
        if main_model     is not None: self._config.main_model     = main_model
        if cluster_model  is not None: self._config.cluster_model  = cluster_model
        if fallback_model is not None:
            self._config.fallback_model = fallback_model
            # Also update the list if not explicitly provided
            if fallback_models is None:
                self._config.fallback_models = [fallback_model]
        if fallback_models is not None:
            self._config.fallback_models = fallback_models
            if fallback_models:
                self._config.fallback_model = fallback_models[0]
        if default_output  is not None: self._config.default_output  = default_output
        if max_tokens      is not None: self._config.max_tokens      = max_tokens
        if max_token_per_module      is not None: self._config.max_token_per_module      = max_token_per_module
        if max_token_per_leaf_module is not None: self._config.max_token_per_leaf_module = max_token_per_leaf_module
        if max_depth is not None: self._config.max_depth = max_depth

        # Validate when essential fields are present
        if self._config.base_url and self._config.main_model and self._config.cluster_model:
            self._config.validate()

        # Persist API key
        if api_key is not None:
            self._api_key = api_key
            stored_in_keychain = False

            if self._keyring_available and not force_key_to_file:
                try:
                    keyring.set_password(KEYRING_SERVICE, KEYRING_API_KEY_ACCOUNT, api_key)
                    stored_in_keychain = True
                except KeyringError:
                    pass

            if not stored_in_keychain:
                # Fallback or forced: store in config file (plaintext)
                self._config.api_key = api_key

        # Write JSON
        config_data = {"version": CONFIG_VERSION, **self._config.to_dict()}
        try:
            safe_write(CONFIG_FILE, json.dumps(config_data, indent=2))
        except FileSystemError as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")

    # ------------------------------------------------------------------
    # Credential resolution
    # ------------------------------------------------------------------

    def get_api_key(self) -> Optional[str]:
        """
        Resolve the API key using the priority chain:
          1. CODEWIKI_API_KEY env var
          2. In-memory cache (set during save / load)
          3. config.json  api_key field
          4. System keychain
        """
        # 1. Environment variable
        env_key = os.environ.get(ENV_API_KEY)
        if env_key:
            return env_key

        # 2. In-memory
        if self._api_key:
            return self._api_key

        # 3. Config file field
        if self._config and self._config.api_key:
            self._api_key = self._config.api_key
            return self._api_key

        # 4. Keychain
        if self._keyring_available:
            try:
                self._api_key = keyring.get_password(KEYRING_SERVICE, KEYRING_API_KEY_ACCOUNT)
            except KeyringError:
                pass

        return self._api_key

    def get_config(self) -> Optional[Configuration]:
        """Return the current configuration, with env var overrides applied."""
        if self._config is None:
            return None
        return self._apply_env_overrides(self._config)

    def _apply_env_overrides(self, config: Configuration) -> Configuration:
        """
        Return a copy of *config* with any CODEWIKI_* env vars applied on top.
        Original object is not mutated.
        """
        from dataclasses import replace
        overrides = {}
        if os.environ.get(ENV_BASE_URL):
            overrides["base_url"] = os.environ[ENV_BASE_URL]
        if os.environ.get(ENV_MAIN_MODEL):
            overrides["main_model"] = os.environ[ENV_MAIN_MODEL]
        if os.environ.get(ENV_CLUSTER_MODEL):
            overrides["cluster_model"] = os.environ[ENV_CLUSTER_MODEL]
        if os.environ.get(ENV_FALLBACK_MODEL):
            overrides["fallback_model"] = os.environ[ENV_FALLBACK_MODEL]
        if overrides:
            return replace(config, **overrides)
        return config

    def _env_only_config(self) -> Optional[Configuration]:
        """
        Build a minimal Configuration purely from env vars (no file required).
        Returns None if essential env vars are absent.
        """
        base_url      = os.environ.get(ENV_BASE_URL)
        main_model    = os.environ.get(ENV_MAIN_MODEL)
        cluster_model = os.environ.get(ENV_CLUSTER_MODEL)

        if not (base_url and main_model and cluster_model):
            return None

        from codewiki.cli.models.config import AgentInstructions
        return Configuration(
            base_url=base_url,
            main_model=main_model,
            cluster_model=os.environ.get(ENV_CLUSTER_MODEL, main_model),
            fallback_model=os.environ.get(ENV_FALLBACK_MODEL, main_model),
            agent_instructions=AgentInstructions(),
        )

    # ------------------------------------------------------------------
    # Status checks
    # ------------------------------------------------------------------

    def is_configured(self) -> bool:
        """
        Return True if a complete, usable configuration is available from
        *any* source (env vars, config file, or keychain).
        """
        # Try env-only path first
        if self._env_only_config() and self.get_api_key():
            return True

        if self._config is None:
            return False

        effective = self._apply_env_overrides(self._config)
        return bool(self.get_api_key() and effective.is_complete())

    def load_or_env(self) -> bool:
        """
        Like load(), but also returns True when full configuration is
        available purely via environment variables (no file needed).
        """
        file_loaded = self.load() if CONFIG_FILE.exists() else False
        return file_loaded or self.is_configured()

    # ------------------------------------------------------------------
    # Keychain helpers
    # ------------------------------------------------------------------

    def delete_api_key(self):
        """Delete API key from keychain and config file."""
        if self._keyring_available:
            try:
                keyring.delete_password(KEYRING_SERVICE, KEYRING_API_KEY_ACCOUNT)
            except KeyringError:
                pass
        if self._config:
            self._config.api_key = None
        self._api_key = None

    def clear(self):
        """Clear all configuration (file and keychain)."""
        self.delete_api_key()
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        self._config = None
        self._api_key = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def keyring_available(self) -> bool:
        return self._keyring_available

    @property
    def config_file_path(self) -> Path:
        return CONFIG_FILE
