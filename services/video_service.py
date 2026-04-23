"""
Video Generation Service.

Converts reel script scenes into structured prompts for AI video tools.
Supported targets:
  - Runway ML Gen-3
  - Pika Labs 1.5
  - Kling AI

When MOCK_MEDIA_APIS=True (default), no real API calls are made.
Structured prompts are saved to output/videos/ ready for manual submission.
"""

from typing import Any

from config import MOCK_MEDIA_APIS, AGENCY_NAME
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Prompt templates per platform ─────────────────────────────────────────────

_RUNWAY_STYLE_GUIDE = (
    "Cinematic, 4K, professional corporate b-roll, "
    "smooth camera movements, natural lighting, no text overlays."
)

_PIKA_STYLE_GUIDE = (
    "Sleek motion graphics, modern UI elements, "
    "dynamic transitions, brand-safe colours, 16:9 or 9:16."
)

_KLING_STYLE_GUIDE = (
    "Hyper-realistic, human subjects, office/tech environments, "
    "confident professionals, minimal CGI."
)


def _scene_to_runway_prompt(scene: dict[str, Any], topic: str) -> dict[str, Any]:
    visual    = scene.get("visual", "")
    b_roll    = scene.get("b_roll_suggestion", "")
    duration  = scene.get("duration", "3–5 sec")

    prompt = (
        f"{visual}. {b_roll}. "
        f"Context: {topic}. "
        f"{_RUNWAY_STYLE_GUIDE}"
    ).strip()

    return {
        "scene_number":  scene.get("scene_number", 1),
        "platform":      "Runway ML Gen-3",
        "prompt":        prompt,
        "duration":      duration,
        "motion_hint":   "Slow push-in or steady tracking shot",
        "negative_prompt": "shaky cam, text, watermark, low quality, cartoon",
        "aspect_ratio":  "9:16",
        "style_preset":  "cinematic",
    }


def _scene_to_pika_prompt(scene: dict[str, Any], topic: str) -> dict[str, Any]:
    visual   = scene.get("visual", "")
    duration = scene.get("duration", "3–5 sec")

    prompt = (
        f"{visual}. Modern marketing aesthetic. "
        f"Topic: {topic}. "
        f"{_PIKA_STYLE_GUIDE}"
    ).strip()

    return {
        "scene_number": scene.get("scene_number", 1),
        "platform":     "Pika Labs 1.5",
        "prompt":       prompt,
        "duration":     duration,
        "camera_motion": "orbit",
        "guidance_scale": 16,
        "negative_prompt": "blurry, watermark, text overlay, amateur",
        "aspect_ratio":  "9:16",
    }


def build_video_prompts(
    reel_script: dict[str, Any],
    topic: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a reel script into per-scene prompts for video generation tools.
    """
    scenes     = reel_script.get("scenes", [])
    topic_name = topic.get("topic", "digital marketing")
    hook_text  = reel_script.get("hook", "")
    music_mood = reel_script.get("music_mood", "upbeat corporate")

    runway_prompts = [_scene_to_runway_prompt(s, topic_name) for s in scenes]
    pika_prompts   = [_scene_to_pika_prompt(s, topic_name) for s in scenes]

    # Full video brief
    brief = {
        "video_title":     topic_name,
        "hook":            hook_text,
        "total_duration":  reel_script.get("total_duration", "~45 seconds"),
        "music_mood":      music_mood,
        "aspect_ratio":    "9:16 (vertical / Reels)",
        "resolution":      "1080 × 1920",
        "fps":             30,
        "colour_grading":  "Warm, professional, slight de-saturation for authority",
        "text_overlay_font": "Inter Bold or Montserrat ExtraBold",
        "agency_watermark": f"{AGENCY_NAME} — bottom-right corner",
    }

    result: dict[str, Any] = {
        "status":         "mocked" if MOCK_MEDIA_APIS else "live",
        "video_brief":    brief,
        "runway_prompts": runway_prompts,
        "pika_prompts":   pika_prompts,
        "manual_steps": [
            "1. Copy each prompt from runway_prompts into Runway ML Gen-3 (runwayml.com)",
            "2. Set aspect ratio to 9:16, duration per scene, apply negative prompts",
            "3. Download rendered clips and stitch in CapCut / Premiere with music_mood track",
            "4. Add text overlays using on_screen_text from the reel script",
            f"5. Add {AGENCY_NAME} watermark and CTA card at the end",
        ],
    }

    if not MOCK_MEDIA_APIS:
        result = _call_runway_api(result, runway_prompts)

    logger.info(
        "Video prompts built | scenes=%d | status=%s",
        len(scenes),
        result["status"],
    )
    return result


def _call_runway_api(
    result: dict[str, Any],
    prompts: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Placeholder for real Runway ML API integration.
    Activate by setting MOCK_MEDIA_APIS=False and providing RUNWAY_API_KEY.
    """
    import os  # noqa: PLC0415
    api_key = os.getenv("RUNWAY_API_KEY", "")
    if not api_key:
        logger.warning("RUNWAY_API_KEY not set — falling back to mock mode")
        result["status"] = "mocked"
        return result

    # TODO: integrate runwayml Python SDK when available
    # from runwayml import RunwayML
    # client = RunwayML(api_key=api_key)
    # for prompt_data in prompts:
    #     task = client.image_to_video.create(...)
    #     result["runway_tasks"].append(task.id)

    logger.warning("Runway API integration not yet implemented — using mock")
    result["status"] = "mocked"
    return result
