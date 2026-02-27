import os
from functools import lru_cache
from typing import Optional


def _get_env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key)
    if value is None:
        if default is not None:
            return default
        raise RuntimeError(f"Required environment variable {key} is not set.")
    return value


@lru_cache(maxsize=1)
def get_settings() -> dict:
    """
    Return immutable settings for the backend.
    """
    return {
        "openai_api_key": _get_env("OPENAI_API_KEY"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "openai_timeout_seconds": float(os.getenv("OPENAI_TIMEOUT_SECONDS", "20")),
    }

