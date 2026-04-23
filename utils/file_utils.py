import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s_-]", "", text)
    slug = re.sub(r"\s+", "_", slug.strip()).lower()
    return slug[:max_len]


def save_json(data: Any, directory: Path, filename: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Saved JSON  → %s", path)
    return path


def save_text(text: str, directory: Path, filename: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(text, encoding="utf-8")
    logger.info("Saved text  → %s", path)
    return path


def save_pipeline_outputs(
    topic: dict,
    viral_analysis: dict,
    generated_content: dict,
    qc_result: dict,
    video_prompts: dict,
    design_prompts: dict,
) -> dict:
    """Persist all pipeline artefacts and return a map of saved paths."""
    from config import SCRIPTS_DIR, IMAGES_DIR, VIDEOS_DIR, OUTPUT_DIR

    ts    = _timestamp()
    slug  = _slugify(topic.get("topic", "content"))
    base  = f"{ts}_{slug}"

    saved: dict[str, str] = {}

    # ── Full pipeline bundle ──────────────────────────────────────────────────
    bundle = {
        "trending_topic":    topic,
        "viral_analysis":    viral_analysis,
        "generated_content": generated_content,
        "qc_result":         qc_result,
        "video_prompts":     video_prompts,
        "design_prompts":    design_prompts,
    }
    p = save_json(bundle, OUTPUT_DIR, f"{base}_full_pipeline.json")
    saved["full_pipeline"] = str(p)

    # ── Reel script (plain text) ──────────────────────────────────────────────
    script_data = generated_content.get("reel_script", {})
    script_text = _build_script_text(script_data, topic)
    p = save_text(script_text, SCRIPTS_DIR, f"{base}_reel_script.txt")
    saved["reel_script"] = str(p)

    # ── Content JSON (hooks, carousel, caption, hashtags, cta) ───────────────
    content_clean = {k: v for k, v in generated_content.items() if k != "reel_script"}
    p = save_json(content_clean, OUTPUT_DIR, f"{base}_content.json")
    saved["content_json"] = str(p)

    # ── Video prompts ─────────────────────────────────────────────────────────
    p = save_json(video_prompts, VIDEOS_DIR, f"{base}_video_prompts.json")
    saved["video_prompts"] = str(p)

    # ── Design prompts ────────────────────────────────────────────────────────
    p = save_json(design_prompts, IMAGES_DIR, f"{base}_design_prompts.json")
    saved["design_prompts"] = str(p)

    # ── QC report ────────────────────────────────────────────────────────────
    p = save_json(qc_result, OUTPUT_DIR, f"{base}_qc_report.json")
    saved["qc_report"] = str(p)

    logger.info("All outputs saved. Files: %d", len(saved))
    return saved


def _build_script_text(script_data: dict, topic: dict) -> str:
    lines = [
        "=" * 60,
        f"REEL SCRIPT — {topic.get('topic', 'Content')}",
        "=" * 60,
    ]

    hook = script_data.get("hook", "")
    if hook:
        lines += ["", "HOOK (0–3 sec)", "-" * 30, hook]

    scenes = script_data.get("scenes", [])
    if scenes:
        lines += ["", "SCENE BREAKDOWN", "-" * 30]
        for i, scene in enumerate(scenes, 1):
            lines.append(f"\nScene {i}: {scene.get('title', '')}")
            lines.append(f"  Duration : {scene.get('duration', '')}")
            lines.append(f"  Voiceover: {scene.get('voiceover', '')}")
            lines.append(f"  Visual   : {scene.get('visual', '')}")
            lines.append(f"  Text     : {scene.get('on_screen_text', '')}")

    cta = script_data.get("cta", "")
    if cta:
        lines += ["", "CALL TO ACTION", "-" * 30, cta]

    total = script_data.get("total_duration", "")
    if total:
        lines += ["", f"Total Duration: {total}"]

    lines.append("=" * 60)
    return "\n".join(lines)
