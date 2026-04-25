"""
Design / Image Generation Service.

Converts carousel slides and visual directions into structured prompts for:
  - Midjourney / DALL-E 3 / Adobe Firefly  (AI image generation)
  - Canva API                              (template-based design)

When MOCK_MEDIA_APIS=True (default), produces ready-to-use prompt packages
saved to output/images/.
"""

from typing import Any

from config import MOCK_MEDIA_APIS, AGENCY_NAME
from utils.logger import get_logger
from services.llm_service import call_llm_json
from services.skill_service import get_kendrithm_visuals_skill

logger = get_logger(__name__)

# ── Style constants ───────────────────────────────────────────────────────────

_MJ_SUFFIX = (
    "--ar 4:5 --style raw --v 6 "
    "--no text, watermark, blur, cartoonish"
)

_DALLE_STYLE = "vivid"  # "vivid" | "natural"
_DALLE_QUALITY = "hd"
_DALLE_SIZE = "1024x1024"

_FIREFLY_SETTINGS = {
    "content_class": "photo",
    "styles": ["photography", "digital_art"],
    "negative_prompt": "text, watermark, logo, low quality, blurry",
}


# ── Per-slide prompt builders ─────────────────────────────────────────────────

def _slide_to_image_prompt(
    slide: dict[str, Any],
    theme: str,
    palette: list[str],
    style: str,
) -> dict[str, Any]:
    headline   = slide.get("headline", "")
    visual_dir = slide.get("visual_direction", "")
    design_tip = slide.get("design_tip", "")

    # Midjourney prompt
    mj_prompt = (
        f"{visual_dir}. "
        f"Background concept for a '{headline}' marketing slide. "
        f"Color palette: {', '.join(palette[:3])}. "
        f"Style: {style}, clean, professional. "
        f"{_MJ_SUFFIX}"
    )

    # DALL-E 3 prompt
    dalle_prompt = (
        f"Professional marketing image for a social media carousel slide. "
        f"Visual concept: {visual_dir}. "
        f"The image should evoke: {headline}. "
        f"Colours: {', '.join(palette[:3])}. "
        f"Style: modern, {style}, no text in image."
    )

    # Adobe Firefly
    firefly_prompt = {
        "prompt": f"{visual_dir}. Professional {style} marketing graphic. "
                  f"Color tone: {', '.join(palette[:2])}.",
        **_FIREFLY_SETTINGS,
    }

    return {
        "slide_number":    slide.get("slide_number", 1),
        "slide_type":      slide.get("type", "value"),
        "headline":        headline,
        "midjourney":      mj_prompt,
        "dalle3":          {"prompt": dalle_prompt, "style": _DALLE_STYLE,
                            "quality": _DALLE_QUALITY, "size": _DALLE_SIZE},
        "adobe_firefly":   firefly_prompt,
        "canva_hint":      f"{design_tip} Use headline: '{headline}'",
        "copy_overlay": {
            "headline":  headline,
            "subtext":   slide.get("subtext", ""),
            "font_size_headline": "48–64px",
            "font_size_subtext":  "18–22px",
            "text_align": "left" if slide.get("slide_number", 1) > 1 else "center",
        },
    }


def _thumbnail_prompt(topic: str, hook: str, palette: list[str]) -> dict[str, Any]:
    mj = (
        f"Cinematic thumbnail for a social media reel about '{topic}'. "
        f"Bold, eye-catching, conveys urgency. "
        f"Colour palette: {', '.join(palette[:3])}. "
        f"No faces, no text. Clean and professional. "
        f"{_MJ_SUFFIX}"
    )
    return {
        "type":         "reel_thumbnail",
        "midjourney":   mj,
        "dalle3":       {
            "prompt":  f"Eye-catching thumbnail image for a marketing video about {topic}. "
                       f"High contrast, bold colours {', '.join(palette[:2])}, no text.",
            "style":   _DALLE_STYLE,
            "quality": _DALLE_QUALITY,
            "size":    "1792x1024",
        },
        "copy_overlay": {
            "hook_text":  hook,
            "font":       "Montserrat ExtraBold",
            "font_size":  "72–96px",
            "text_colour": palette[0] if palette else "#FFFFFF",
        },
    }


# ── Public API ────────────────────────────────────────────────────────────────

def build_design_prompts(
    carousel: dict[str, Any],
    hooks: dict[str, Any],
    topic: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate structured image/design prompts for each carousel slide
    plus a reel thumbnail.
    """
    slides      = carousel.get("slides", [])
    palette     = carousel.get("colour_palette", ["#1A1A2E", "#E94560", "#FFFFFF"])
    font_pair   = carousel.get("font_pairing", "Montserrat + Inter")
    style       = carousel.get("overall_design_style", "clean-corporate")
    theme       = carousel.get("carousel_theme", "")
    best_hook   = ""

    best_id = hooks.get("recommended_hook_id", 1)
    for h in hooks.get("hooks", []):
        if h.get("id") == best_id:
            best_hook = h.get("text", "")
            break

    slide_prompts = [
        _slide_to_image_prompt(s, theme, palette, style) for s in slides
    ]

    thumbnail = _thumbnail_prompt(topic.get("topic", ""), best_hook, palette)

    canva_spec = {
        "template_search": f"{style} Instagram carousel {topic.get('category', 'marketing')}",
        "slide_count":     len(slides),
        "dimensions":      "1080 × 1350 px (4:5) for feed, 1080 × 1920 for Stories",
        "brand_colours":   palette,
        "fonts":           font_pair,
        "logo_placement":  "Bottom-left corner of each slide",
        "agency_name":     AGENCY_NAME,
        "export_format":   "PNG, 300 DPI",
    }

    pillow_prompt = f"""
Generate a complete, runnable Python script using the Pillow library to create the carousel slides.

Topic: {topic.get('topic', '')}
Carousel Content:
{str(slides)}

CRITICAL INSTRUCTION: You MUST apply all the color, typography, spacing, and Python boilerplate rules from your system instructions (Kendrithm Visuals Skill). 
Return a STRICT JSON response containing the full python code.

Return STRICT JSON:
{{
  "python_script": "import os\\nfrom PIL import Image..."
}}
"""
    skill_prompt = get_kendrithm_visuals_skill()
    try:
        logger.info("Generating Kendrithm Pillow script...")
        script_res = call_llm_json(pillow_prompt, system_prompt=skill_prompt, max_tokens=4000)
        pillow_script = script_res.get("python_script", "")
    except Exception as e:
        logger.error(f"Failed to generate Pillow script: {e}")
        pillow_script = ""

    result: dict[str, Any] = {
        "status":          "mocked" if MOCK_MEDIA_APIS else "live",
        "carousel_theme":  theme,
        "colour_palette":  palette,
        "font_pairing":    font_pair,
        "slide_prompts":   slide_prompts,
        "reel_thumbnail":  thumbnail,
        "canva_spec":      canva_spec,
        "pillow_script":   pillow_script,
        "manual_steps": [
            "1. Open Canva and search the template in canva_spec.template_search",
            "2. Apply colour_palette and font_pairing from this spec",
            "3. For each slide use copy_overlay.headline and copy_overlay.subtext",
            "4. For AI backgrounds: paste midjourney prompt into Midjourney or DALL-E 3",
            "5. Export all slides as PNG 300DPI",
            "6. For the reel thumbnail use reel_thumbnail prompts and add hook_text overlay",
        ],
    }

    if not MOCK_MEDIA_APIS:
        result = _call_modelslab_api(result, slide_prompts)

    logger.info(
        "Design prompts built | slides=%d | status=%s",
        len(slides),
        result["status"],
    )
    return result


def _call_modelslab_api(
    result: dict[str, Any],
    slide_prompts: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Real ModelsLab API integration.
    Activate by setting MOCK_MEDIA_APIS=False and providing MODELSLAB_API_KEY.
    """
    import os  # noqa: PLC0415
    import requests # noqa: PLC0415
    api_key = os.getenv("MODELSLAB_API_KEY", "")
    if not api_key:
        logger.warning("MODELSLAB_API_KEY not set — falling back to mock mode")
        result["status"] = "mocked"
        return result

    url = "https://modelslab.com/api/v7/images/text-to-image"
    headers = {"Content-Type": "application/json"}
    
    for sp in slide_prompts:
        data = {
            "key": api_key,
            "model_id": "gemini-3.1-t2i",
            "prompt": sp["dalle3"]["prompt"],
            "aspect_ratio": "4:5"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            res_json = response.json()
            
            # The API response typically contains the generated image link(s) in an 'output' array or similar.
            # You might need to adjust the parsing below based on the actual API response schema.
            if res_json.get("status") == "success" or "output" in res_json:
                sp["modelslab_url"] = res_json.get("output", [""])[0]
                logger.info(f"Generated image for slide {sp.get('slide_number')}")
            else:
                logger.error(f"Modelslab API error: {res_json}")
                sp["modelslab_url"] = None
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred during Modelslab generation: {http_err} - {response.text}")
            sp["modelslab_url"] = None
        except Exception as err:
            logger.error(f"Other error occurred during Modelslab generation: {err}")
            sp["modelslab_url"] = None

    result["status"] = "live"
    return result
