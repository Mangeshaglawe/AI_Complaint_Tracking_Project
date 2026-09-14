
import logging
import os
from dataclasses import dataclass
from typing import Any, Optional

from openai import AzureOpenAI, OpenAI

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    api_key: str
    model: str = "gpt-4o-mini"
    api_version: Optional[str] = None
    base_url: Optional[str] = None


def load_config() -> LLMConfig:
    return LLMConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        base_url=os.getenv("OPENAI_BASE_URL") or os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


def _build_client(cfg: LLMConfig):
    """Initiate the correct OpenAI client based on the config."""
    if cfg.api_version:
        logger.info("Using AzureOpenAI client - base_url=%s", cfg.base_url)
        return AzureOpenAI(
            api_key=cfg.api_key,
            azure_endpoint=cfg.base_url or "",
            api_version=cfg.api_version,
        )

    kwargs: dict[str, Any] = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
        logger.info("Using OpenAI-compatible client - base_url=%s", cfg.base_url)
    else:
        logger.info("Using standard OpenAI client")
    return OpenAI(**kwargs)


class LLMClient:
    """High-level LLM client wrapping OpenAI chat completions."""

    def __init__(self) -> None:
        self._cfg = load_config()
        self._client = _build_client(self._cfg)

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2048,
        response_format: Optional[Any] = None,
    ) -> str:
        """Send the chat completion and return the assistant reply as a string."""
        kwargs: dict[str, Any] = {
            "model": self._cfg.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format is not None:
            kwargs["response_format"] = response_format

        logger.debug(
            "LLM call --> model=%s temp=%.1f max_tokens=%d",
            self._cfg.model,
            temperature,
            max_tokens,
        )

        try:
            response = self._client.chat.completions.create(**kwargs)
        except Exception as exc:
            logger.error("LLM API call failed: %s", exc)
            raise

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("LLM returned an empty response - check your model & prompt.")
        return content
