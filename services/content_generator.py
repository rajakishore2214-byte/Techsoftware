"""
Content Generation Engine.

Generates all content assets for a trending topic using the viral formula
extracted by the audit engine.

Assets produced:
  - 3 high-converting hooks
  - Full reel script (30–60 sec, scene-by-scene)
  - Visual prompts per scene
  - Carousel / poster slides (5–7)
  - SEO-optimised caption
  - Hashtag set (10–15)
  - Lead-focused CTA variants
"""

from typing import Any

from services.llm_service import call_llm_json, call_qc
from config import PRIMARY_MODEL, AGENCY_NAME, AGENCY_SERVICES, TARGET_AUDIENCE, CONTENT_GOAL
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Prompt builders ───────────────────────────────────────────────────────────

def _hooks_prompt(topic: dict, analysis: dict, improvement: dict) -> str:
    return f"""
Generate 3 elite, high-converting hooks for a social media reel.

Topic         : {topic['topic']}
Hook Type     : {analysis.get('hook_type', 'pain_point')}
Viral Formula : {analysis.get('viral_formula_name', '')}
Pain Point    : {analysis.get('audience_pain_point', '')}
Hook Formula  : {analysis.get('repeatable_pattern', {}).get('hook_formula', '')}
Best Hook Lead: {improvement.get('improved_hook', '')}
Audience      : {', '.join(TARGET_AUDIENCE)}

Rules:
- Each hook must be under 10 words
- Must instantly address a pain point or create strong curiosity
- Must NOT start with "Are you", "In today's world", or "Have you ever"
- Hook 1 = Pain-point-based
- Hook 2 = Curiosity/mystery-based
- Hook 3 = Authority/result-based

Return STRICT JSON:
{{
  "hooks": [
    {{
      "id": 1,
      "type": "pain_point",
      "text": "<hook text>",
      "why_it_works": "<one sentence explanation>"
    }},
    {{
      "id": 2,
      "type": "curiosity",
      "text": "<hook text>",
      "why_it_works": "<one sentence explanation>"
    }},
    {{
      "id": 3,
      "type": "authority_result",
      "text": "<hook text>",
      "why_it_works": "<one sentence explanation>"
    }}
  ],
  "recommended_hook_id": <1, 2, or 3>,
  "recommended_reason": "<why this hook will outperform>"
}}
"""


def _reel_script_prompt(topic: dict, analysis: dict, hooks: dict) -> str:
    best_hook_id = hooks.get("recommended_hook_id", 1)
    best_hook = next(
        (h["text"] for h in hooks.get("hooks", []) if h["id"] == best_hook_id),
        hooks.get("hooks", [{}])[0].get("text", ""),
    )
    return f"""
Write a complete, production-ready Instagram/TikTok reel script (30–60 seconds).

Topic         : {topic['topic']}
Hook          : {best_hook}
Pain Point    : {analysis.get('audience_pain_point', '')}
Content Format: {analysis.get('content_structure', 'problem-agitate-solve')}
Value          : {analysis.get('value_delivered', '')}
Agency        : {AGENCY_NAME}
Services      : {', '.join(AGENCY_SERVICES[:4])}

Script requirements:
- Conversational but authoritative tone
- Each scene has a clear visual direction
- No filler phrases
- End with a lead-generation CTA

Return STRICT JSON:
{{
  "hook": "<opening 1–3 seconds — the exact words spoken AND shown on screen>",
  "total_duration": "<e.g. 52 seconds>",
  "scenes": [
    {{
      "scene_number": 1,
      "title": "<scene label>",
      "duration": "<e.g. 0–3 sec>",
      "voiceover": "<exact words spoken>",
      "on_screen_text": "<text overlay if any>",
      "visual": "<precise visual direction for the video editor/AI video tool>",
      "b_roll_suggestion": "<specific b-roll or stock footage description>",
      "transition": "<cut | zoom | swipe | fade>"
    }}
  ],
  "cta": "<exact CTA spoken + shown at end>",
  "music_mood": "<e.g. upbeat corporate, lo-fi focus, urgent cinematic>",
  "caption_line": "<one punchy line to use as Instagram caption opener>"
}}
"""


def _carousel_prompt(topic: dict, analysis: dict, hooks: dict) -> str:
    best_hook_id = hooks.get("recommended_hook_id", 1)
    best_hook = next(
        (h["text"] for h in hooks.get("hooks", []) if h["id"] == best_hook_id),
        "",
    )
    return f"""
Design a 6-slide Instagram/LinkedIn carousel for the following topic.

Topic     : {topic['topic']}
Hook      : {best_hook}
Pain Point: {analysis.get('audience_pain_point', '')}
Formula   : {analysis.get('content_structure', '')}
Agency    : {AGENCY_NAME}

Carousel rules:
- Slide 1 = Hook slide (stops the scroll)
- Slides 2–5 = Value slides (one insight each, scannable)
- Slide 6 = CTA slide (lead generation)
- Each slide: bold headline + 1–2 supporting lines + visual direction

Return STRICT JSON:
{{
  "carousel_theme": "<overall visual theme>",
  "slides": [
    {{
      "slide_number": 1,
      "type": "hook",
      "headline": "<big bold text — the hook>",
      "subtext": "<supporting line, max 15 words>",
      "visual_direction": "<background, colours, imagery>",
      "design_tip": "<specific layout tip for the designer>"
    }}
  ],
  "colour_palette": ["<hex or colour name>", "<hex>", "<hex>"],
  "font_pairing": "<heading font + body font>",
  "overall_design_style": "<minimalist | bold-gradient | clean-corporate | etc>"
}}
"""


def _caption_prompt(topic: dict, analysis: dict, hooks: dict, reel_script: dict) -> str:
    best_hook_id = hooks.get("recommended_hook_id", 1)
    best_hook = next(
        (h["text"] for h in hooks.get("hooks", []) if h["id"] == best_hook_id),
        "",
    )
    return f"""
Write a complete, SEO-optimised Instagram/LinkedIn caption for the following content.

Topic         : {topic['topic']}
Hook          : {best_hook}
Pain Point    : {analysis.get('audience_pain_point', '')}
Value Delivered: {analysis.get('value_delivered', '')}
Agency        : {AGENCY_NAME}
Services      : {', '.join(AGENCY_SERVICES)}
Audience      : {', '.join(TARGET_AUDIENCE)}
Goal          : {CONTENT_GOAL}

Caption requirements:
- Opens with the hook (first line must force the "more" tap)
- 150–250 words
- Uses line breaks and spacing for readability
- Includes 1 data point or statistic
- Ends with a lead-gen CTA (comment, DM, or link in bio)
- Naturally includes 3–5 SEO keywords

Also generate:
- 12–15 hashtags (mix of niche, mid-range, and broad)
- 3 CTA variants (soft, medium, hard)

Return STRICT JSON:
{{
  "caption": "<full caption text with line breaks as \\n>",
  "seo_keywords_used": ["<kw1>", "<kw2>", "<kw3>"],
  "hashtags": ["#tag1", "#tag2"],
  "cta_variants": {{
    "soft":   "<low-friction CTA — e.g. save this post>",
    "medium": "<mid-friction CTA — e.g. comment X>",
    "hard":   "<direct lead CTA — e.g. DM us 'GROW' for a free strategy call>"
  }},
  "first_comment_hashtags": ["#tag13", "#tag14", "#tag15"]
}}
"""


def _qc_prompt(generated: dict, topic: dict) -> str:
    import json
    summary = {
        "hooks": generated.get("hooks", {}).get("hooks", []),
        "reel_hook": generated.get("reel_script", {}).get("hook", ""),
        "caption_preview": generated.get("caption", {}).get("caption", "")[:300],
        "carousel_slides": [
            s.get("headline") for s in generated.get("carousel", {}).get("slides", [])
        ],
    }
    return f"""
You are a senior content quality reviewer. Review the following generated marketing content.

Topic : {topic['topic']}
Content Summary:
{json.dumps(summary, indent=2)}

Evaluate on these criteria:
1. Is any hook generic or clichéd? (score 1–10)
2. Is the caption opener strong enough to force the "more" tap? (score 1–10)
3. Are the carousel headlines scannable and value-dense? (score 1–10)
4. Is there a clear, specific lead-generation CTA? (score 1–10)
5. Overall quality (score 1–10)

Then provide specific, actionable improvements.

Return STRICT JSON:
{{
  "scores": {{
    "hooks":     <1–10>,
    "caption":   <1–10>,
    "carousel":  <1–10>,
    "cta":       <1–10>,
    "overall":   <1–10>
  }},
  "passes_qc": <true if overall >= 7, else false>,
  "issues_found": ["<issue 1>", "<issue 2>"],
  "improvements": [
    {{
      "field": "<hooks | caption | carousel | cta>",
      "original": "<original text>",
      "improved": "<improved text>",
      "reason": "<why this is better>"
    }}
  ],
  "qc_verdict": "<APPROVED | NEEDS_REVISION>",
  "reviewer_note": "<one sentence overall verdict>"
}}
"""


# ── Public API ────────────────────────────────────────────────────────────────

def generate_hooks(
    topic: dict[str, Any],
    analysis: dict[str, Any],
    improvement: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Generating hooks...")
    result = call_llm_json(_hooks_prompt(topic, analysis, improvement))
    logger.info("Hooks generated | recommended=%d", result.get("recommended_hook_id", -1))
    return result


def generate_reel_script(
    topic: dict[str, Any],
    analysis: dict[str, Any],
    hooks: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Generating reel script...")
    result = call_llm_json(_reel_script_prompt(topic, analysis, hooks))
    logger.info(
        "Script generated | duration=%s | scenes=%d",
        result.get("total_duration"),
        len(result.get("scenes", [])),
    )
    return result


def generate_carousel(
    topic: dict[str, Any],
    analysis: dict[str, Any],
    hooks: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Generating carousel...")
    result = call_llm_json(_carousel_prompt(topic, analysis, hooks))
    logger.info("Carousel generated | slides=%d", len(result.get("slides", [])))
    return result


def generate_caption_and_hashtags(
    topic: dict[str, Any],
    analysis: dict[str, Any],
    hooks: dict[str, Any],
    reel_script: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Generating caption & hashtags...")
    result = call_llm_json(_caption_prompt(topic, analysis, hooks, reel_script))
    logger.info(
        "Caption generated | hashtags=%d", len(result.get("hashtags", []))
    )
    return result


def run_quality_check(
    generated: dict[str, Any],
    topic: dict[str, Any],
) -> dict[str, Any]:
    logger.info("Running quality control check...")
    result = call_qc(_qc_prompt(generated, topic))
    verdict = result.get("qc_verdict", "UNKNOWN")
    score   = result.get("scores", {}).get("overall", 0)
    logger.info("QC complete | verdict=%s | overall_score=%s", verdict, score)
    return result


def generate_all_content(
    topic: dict[str, Any],
    analysis: dict[str, Any],
    improvement: dict[str, Any],
) -> dict[str, Any]:
    """
    Full content generation pass.
    Returns a dict with all content assets.
    """
    hooks       = generate_hooks(topic, analysis, improvement)
    reel_script = generate_reel_script(topic, analysis, hooks)
    carousel    = generate_carousel(topic, analysis, hooks)
    caption     = generate_caption_and_hashtags(topic, analysis, hooks, reel_script)

    return {
        "topic":       topic,
        "hooks":       hooks,
        "reel_script": reel_script,
        "carousel":    carousel,
        "caption":     caption,
    }
