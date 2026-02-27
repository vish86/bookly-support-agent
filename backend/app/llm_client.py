from collections.abc import Sequence
from typing import Any

from openai import OpenAI

from .config import get_settings


def _build_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings["openai_api_key"])


def get_client() -> OpenAI:
    """
    Lazily construct and reuse a single OpenAI client instance.
    """
    # Simple module-level singleton is sufficient here; no need for classes.
    global _CLIENT  # type: ignore[assignment]

    try:
        client = _CLIENT  # type: ignore[name-defined]
    except NameError:
        client = _build_client()
        _CLIENT = client  # type: ignore[assignment]
    return client


def chat_completion(
    messages: Sequence[dict[str, Any]],
    temperature: float = 0.1,
) -> str:
    """
    Call OpenAI chat completion with the configured model and return the assistant content.
    """
    settings = get_settings()
    client = get_client()

    response = client.chat.completions.create(
        model=settings["openai_model"],
        messages=list(messages),
        temperature=temperature,
        timeout=settings["openai_timeout_seconds"],
    )

    choice = response.choices[0]
    content = choice.message.content or ""
    return content

