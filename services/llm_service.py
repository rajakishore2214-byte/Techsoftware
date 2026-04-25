"""
Thin wrapper around the Anthropic SDK.
Uses prompt caching on the shared system context to reduce token costs.
"""

import json
import re
import time
from typing import Any

import anthropic

from config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_BASE_URL,
    AGENCY_NAME,
    AGENCY_SERVICES,
    TARGET_AUDIENCE,
    CONTENT_GOAL,
    MAX_TOKENS,
    QC_MAX_TOKENS,
    PRIMARY_MODEL,
    QC_MODEL,
)
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Shared system prompt (cached) ─────────────────────────────────────────────
_SYSTEM_PROMPT = f"""You are a world-class digital marketing strategist and viral content architect.
You create high-converting, platform-native content for social media.

Agency : {AGENCY_NAME}
Services: {", ".join(AGENCY_SERVICES)}
Audience: {", ".join(TARGET_AUDIENCE)}
Goal    : {CONTENT_GOAL}

RULES — follow without exception:
1. Respond ONLY with valid JSON. No prose, no markdown fences, no explanations.
2. All text must be practical, problem-solving, and non-generic.
3. Never use filler phrases like "In today's digital world" or "As we all know".
4. Every hook must create instant curiosity or surface a real pain point.
5. CTAs must be direct lead-generation calls to action.
"""

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not ANTHROPIC_API_KEY:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file."
            )
        
        kwargs = {"api_key": ANTHROPIC_API_KEY}
        if ANTHROPIC_BASE_URL:
            kwargs["base_url"] = ANTHROPIC_BASE_URL
            
        _client = anthropic.Anthropic(**kwargs)
    return _client


def _call(
    prompt: str,
    model: str = PRIMARY_MODEL,
    max_tokens: int = MAX_TOKENS,
    retries: int = 2,
    system_prompt: str | None = None,
) -> str:
    """
    Call the Claude API with prompt caching on the system context.
    Returns raw response text.
    """
    client = _get_client()

    sys_prompt_text = system_prompt if system_prompt else _SYSTEM_PROMPT

    system_block = [
        {
            "type": "text",
            "text": sys_prompt_text,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    for attempt in range(retries + 1):
        try:
            logger.debug("LLM call | model=%s | attempt=%d", model, attempt + 1)
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_block,
                messages=[{"role": "user", "content": prompt}],
            )
            usage = response.usage
            logger.info(
                "LLM usage | in=%d cached_in=%d out=%d",
                usage.input_tokens,
                getattr(usage, "cache_read_input_tokens", 0),
                usage.output_tokens,
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            wait = 2 ** attempt * 5
            logger.warning("Rate limit hit — waiting %ds", wait)
            time.sleep(wait)
        except anthropic.APIStatusError as exc:
            logger.error("API error: %s", exc)
            if attempt == retries:
                raise

    raise RuntimeError("LLM call failed after all retries")


def _strip_fences(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def call_llm_json(
    prompt: str,
    model: str = PRIMARY_MODEL,
    max_tokens: int = MAX_TOKENS,
    system_prompt: str | None = None,
) -> dict[str, Any]:
    """Call LLM and return a parsed JSON dict."""
    raw = _call(prompt, model=model, max_tokens=max_tokens, system_prompt=system_prompt)
    raw = _strip_fences(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse failed. Raw response:\n%s", raw[:500])
        raise ValueError(f"LLM returned invalid JSON: {exc}") from exc


def call_llm_text(
    prompt: str,
    model: str = PRIMARY_MODEL,
    max_tokens: int = MAX_TOKENS,
    system_prompt: str | None = None,
) -> str:
    """Call LLM and return plain text."""
    return _call(prompt, model=model, max_tokens=max_tokens, system_prompt=system_prompt)


def call_qc(prompt: str) -> dict[str, Any]:
    """Convenience wrapper for the quality-control pass."""
    return call_llm_json(prompt, model=QC_MODEL, max_tokens=QC_MAX_TOKENS)
