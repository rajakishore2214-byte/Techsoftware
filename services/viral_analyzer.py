"""
Viral Content Audit & Intelligence Engine.

Two entry points:
  - simulate_viral_content()  →  build a realistic viral post example for a topic
  - analyze_viral_content()   →  deep-analyse any post, extract the repeatable formula
"""

from typing import Any

from services.llm_service import call_llm_json
from config import PRIMARY_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Prompt builders ───────────────────────────────────────────────────────────

def _simulation_prompt(topic: dict[str, Any]) -> str:
    return f"""
You are simulating a real high-performing Instagram reel/post that went viral in the digital marketing niche.

Topic     : {topic['topic']}
Category  : {topic.get('category', 'Digital Marketing')}
Insight   : {topic.get('insight', '')}
Keywords  : {', '.join(topic.get('keywords', []))}

Simulate a realistic viral post with the following structure and return STRICT JSON:

{{
  "platform": "Instagram Reels",
  "topic": "<same topic>",
  "estimated_views": "<realistic view count, e.g. 2.3M>",
  "estimated_likes": "<e.g. 87K>",
  "hook_text": "<the first 3–5 words that stop the scroll>",
  "caption": "<full caption 150–200 words, includes hook, value, CTA>",
  "visual_description": "<describe what appears on screen — text overlays, b-roll, transitions>",
  "audio_description": "<voiceover tone + background music type>",
  "content_structure": [
    {{"second_range": "0–3",  "what_happens": ""}},
    {{"second_range": "3–10", "what_happens": ""}},
    {{"second_range": "10–25","what_happens": ""}},
    {{"second_range": "25–45","what_happens": ""}},
    {{"second_range": "45–60","what_happens": ""}}
  ],
  "hashtags": ["<tag1>", "<tag2>", "<tag3>"],
  "cta_in_video": "<the verbal or text CTA used in the reel>"
}}
"""


def _analysis_prompt(viral_content: dict[str, Any]) -> str:
    content_json = str(viral_content)[:3000]  # guard against huge inputs
    return f"""
You are a viral content intelligence analyst. Deeply analyse the following viral post data and extract the precise formula that drove its performance.

VIRAL POST DATA:
{content_json}

Return STRICT JSON with exactly this structure:

{{
  "hook_type": "<curiosity | fear | authority | social_proof | shock | FOMO | pain_point | aspiration>",
  "hook_analysis": "<why this specific hook stops the scroll in 2–3 sentences>",
  "emotional_trigger": "<primary emotion activated: fear / hope / frustration / inspiration / urgency / curiosity>",
  "emotional_trigger_explanation": "<how and where this emotion is triggered>",
  "content_structure": "<problem-agitate-solve | listicle | before-after | story-reveal | myth-bust | how-to>",
  "structure_breakdown": "<step-by-step explanation of how the structure plays out>",
  "topic_category": "<Paid Ads | SEO | AI Automation | Website | Social Media | Lead Generation>",
  "audience_pain_point": "<the exact pain point this post addresses>",
  "value_delivered": "<what actionable value the viewer gets>",
  "why_it_performed_well": [
    "<reason 1>",
    "<reason 2>",
    "<reason 3>"
  ],
  "repeatable_pattern": {{
    "hook_formula": "<template: e.g. '[PAIN POINT] is costing you [SPECIFIC LOSS]'>",
    "body_formula": "<structure template>",
    "cta_formula": "<CTA template>"
  }},
  "viral_formula_name": "<give this formula a memorable name, e.g. 'The Silent Killer Reveal'>",
  "improvement_opportunities": [
    "<specific thing that could make this content 2x better>",
    "<second improvement>",
    "<third improvement>"
  ]
}}
"""


def _improvement_prompt(
    topic: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    return f"""
Based on the viral content analysis below, generate an IMPROVED version of the content that fixes all weaknesses and amplifies all strengths.

TOPIC: {topic['topic']}
VIRAL FORMULA: {analysis.get('viral_formula_name', '')}
HOOK TYPE: {analysis.get('hook_type', '')}
PAIN POINT: {analysis.get('audience_pain_point', '')}
IMPROVEMENTS NEEDED: {analysis.get('improvement_opportunities', [])}

Return STRICT JSON:

{{
  "improved_hook": "<improved hook — more specific, more pain-point-sharp>",
  "improved_caption_preview": "<first 3 sentences of improved caption>",
  "improved_visual_concept": "<concrete visual improvement — what to film/design differently>",
  "why_this_version_wins": "<1–2 sentences explaining why the improved version outperforms the original>"
}}
"""


# ── Public API ────────────────────────────────────────────────────────────────

def simulate_viral_content(topic: dict[str, Any]) -> dict[str, Any]:
    """
    Simulate a realistic viral post for a given trending topic.
    Used when no real scraped data is available.
    """
    logger.info("Simulating viral content for: '%s'", topic["topic"])
    prompt  = _simulation_prompt(topic)
    result  = call_llm_json(prompt)
    result["_simulated"] = True
    logger.info("Viral simulation complete | platform=%s | views=%s",
                result.get("platform"), result.get("estimated_views"))
    return result


def analyze_viral_content(viral_content: dict[str, Any]) -> dict[str, Any]:
    """
    Perform deep analysis on a viral post.
    Accepts real or simulated content.
    Returns analysis + improvement suggestions.
    """
    logger.info("Analysing viral content...")
    prompt   = _analysis_prompt(viral_content)
    analysis = call_llm_json(prompt)
    logger.info(
        "Viral analysis done | hook_type=%s | formula=%s",
        analysis.get("hook_type"),
        analysis.get("viral_formula_name"),
    )
    return analysis


def generate_improvement(
    topic: dict[str, Any],
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a concrete improved version based on the analysis.
    """
    logger.info("Generating content improvement...")
    prompt  = _improvement_prompt(topic, analysis)
    result  = call_llm_json(prompt)
    logger.info("Improvement generated")
    return result
