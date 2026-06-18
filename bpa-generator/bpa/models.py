"""Model-provider abstraction.

A single ``get_model(role, config)`` is the only place that knows about a
concrete provider. Everything downstream asks for a *role* and gets a
LangChain chat model pointed at the configured AI Gateway. Swapping providers
(or the Gateway) is a change here and nowhere else.
"""
from __future__ import annotations

from functools import lru_cache

from langchain_core.language_models import BaseChatModel

from .config import RunConfig


def get_model(role: str, config: RunConfig) -> BaseChatModel:
    """Return a chat model for a pipeline role (gate/classify/normalize/...)."""
    model_id = config.model_for(role)
    return _build(model_id, config.gateway.base_url, config.gateway.api_key)


@lru_cache(maxsize=None)
def _build(model_id: str, base_url: str | None, api_key: str | None) -> BaseChatModel:
    """Construct (and cache) a chat model bound to the AI Gateway endpoint.

    Uses langchain-anthropic by default. Because the abstraction is centralised,
    pointing at a different Anthropic-compatible gateway only requires changing
    ``base_url``; switching ecosystems entirely means editing this function.
    """
    from langchain_anthropic import ChatAnthropic

    kwargs: dict = {"model": model_id, "temperature": 0, "max_tokens": 4096}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        # ChatAnthropic forwards base_url to the underlying SDK client.
        kwargs["base_url"] = base_url
    return ChatAnthropic(**kwargs)
