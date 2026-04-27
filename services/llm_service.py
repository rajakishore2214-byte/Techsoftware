"""
Thin wrapper around the Gemini SDK.
Uses prompt caching on the shared system context to reduce token costs.
"""

import json
import re
import time
from typing import Any

import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google.api_core import exceptions

from config import (
    GEMINI_API_KEY,
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

_client_configured = False

def _configure_client():
    global _client_configured
    if not _client_configured:
        if not GEMINI_API_KEY:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        genai.configure(api_key=GEMINI_API_KEY)
        _client_configured = True


def _call(
    prompt: str,
    model: str = PRIMARY_MODEL,
    max_tokens: int = MAX_TOKENS,
    retries: int = 2,
    system_prompt: str | None = None,
    response_mime_type: str | None = None,
) -> str:
    """
    Call the Gemini API.
    Returns raw response text.
    """
    _configure_client()

    sys_prompt_text = system_prompt if system_prompt else _SYSTEM_PROMPT

    # Initialize model with system instruction
    gemini_model = genai.GenerativeModel(
        model_name=model,
        system_instruction=sys_prompt_text
    )

    generation_config = GenerationConfig(
        max_output_tokens=max_tokens,
        response_mime_type=response_mime_type
    )

    for attempt in range(retries + 1):
        try:
            logger.debug("LLM call | model=%s | attempt=%d", model, attempt + 1)
            response = gemini_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            # Log usage if available
            try:
                usage = response.usage_metadata
                if usage:
                    logger.info(
                        "LLM usage | in=%d out=%d",
                        usage.prompt_token_count,
                        usage.candidates_token_count,
                    )
            except AttributeError:
                pass
                
            return response.text

        except exceptions.ResourceExhausted:
            wait = 2 ** attempt * 5
            logger.warning("Rate limit hit — waiting %ds", wait)
            time.sleep(wait)
        except exceptions.GoogleAPIError as exc:
            logger.error("API error: %s", exc)
            if attempt == retries:
                raise
        except Exception as exc:
            logger.error("Unexpected error: %s", exc)
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
    retries: int = 2,
) -> dict[str, Any]:
    """Call LLM and return a parsed JSON dict."""
    last_err = None
    for attempt in range(retries + 1):
        raw = _call(
            prompt, 
            model=model, 
            max_tokens=max_tokens, 
            system_prompt=system_prompt,
            response_mime_type="application/json"
        )
        raw = _strip_fences(raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error("JSON parse failed. Raw response:\n%s", raw[:500])
            last_err = exc
            if attempt < retries:
                logger.warning("Retrying JSON generation... (attempt %d)", attempt + 1)
                time.sleep(2)
    raise ValueError(f"LLM returned invalid JSON: {last_err}") from last_err


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
