"""
LLM service factory for creating configured LLM clients.
"""
from typing import List
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModelSettings
from pydantic_ai.models.fallback import FallbackModel
from openai import OpenAI

from codewiki.src.config import Config


def _make_model(model_name: str, config: Config) -> OpenAIModel:
    """Create a single OpenAIModel with the shared provider and settings."""
    return OpenAIModel(
        model_name=model_name,
        provider=OpenAIProvider(
            base_url=config.llm_base_url,
            api_key=config.llm_api_key
        ),
        settings=OpenAIModelSettings(
            temperature=0.0,
            max_tokens=config.max_tokens
        )
    )


def create_main_model(config: Config) -> OpenAIModel:
    """Create the main LLM model from configuration."""
    return _make_model(config.main_model, config)


def create_fallback_model(config: Config) -> OpenAIModel:
    """Create a single fallback model (first in the fallback_models list, or main_model)."""
    model_name = config.fallback_models[0] if config.fallback_models else config.main_model
    return _make_model(model_name, config)


def create_fallback_models(config: Config) -> FallbackModel:
    """
    Build a FallbackModel chain from config.fallback_models.

    The chain is: main_model → fallback_models[0] → fallback_models[1] → …

    If fallback_models contains only the same model as main_model, a single
    entry chain is used (pydantic-ai handles it gracefully).
    """
    main = create_main_model(config)

    # Build fallback chain, deduplicating consecutive identical names
    seen = {config.main_model}
    extras: List[OpenAIModel] = []
    for name in config.fallback_models:
        if name and name not in seen:
            extras.append(_make_model(name, config))
            seen.add(name)

    if not extras:
        # No distinct fallback — use main as sole model (FallbackModel still works)
        return FallbackModel(main, main)

    return FallbackModel(main, *extras)


def create_openai_client(config: Config, timeout: int = 300) -> OpenAI:
    """Create OpenAI client from configuration."""
    return OpenAI(
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        timeout=timeout,
    )


def call_llm(
    prompt: str,
    config: Config,
    model: str = None,
    temperature: float = 0.0,
    timeout: int = 300,
) -> str:
    """
    Call LLM with the given prompt.

    Args:
        prompt: The prompt to send
        config: Configuration containing LLM settings
        model: Model name (defaults to config.main_model)
        temperature: Temperature setting

    Returns:
        LLM response text
    """
    if model is None:
        model = config.main_model

    client = create_openai_client(config, timeout=timeout)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=config.max_tokens
    )
    return response.choices[0].message.content