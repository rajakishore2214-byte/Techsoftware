"""
TechSoftware — AI Content Automation Pipeline
==============================================

Run:
    python main.py

What happens:
    1. Fetch the highest-impact trending topic (Google Trends / fallback)
    2. Simulate (or accept) a viral post for that topic
    3. Deep-analyse the viral content → extract repeatable formula
    4. Generate improved content baseline
    5. Generate all content assets (hooks, reel script, carousel, caption)
    6. Run quality-control review
    7. Build video generation prompts (Runway ML / Pika Labs)
    8. Build design / image generation prompts (Midjourney / DALL-E 3 / Canva)
    9. Save everything to output/
"""

import sys
import time
from pathlib import Path

# ── Make sure project root is on PYTHONPATH ───────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from config import QC_ENABLED, SIMULATE_VIRAL_DATA
from services.trends_service   import get_trending_topic
from services.viral_analyzer   import (
    simulate_viral_content,
    analyze_viral_content,
    generate_improvement,
)
from services.content_generator import generate_all_content, run_quality_check
from services.video_service     import build_video_prompts
from services.design_service    import build_design_prompts
from utils.file_utils           import save_pipeline_outputs
from utils.logger               import get_logger

logger = get_logger("pipeline")

# ─────────────────────────────────────────────────────────────────────────────

def _banner(step: int, total: int, title: str) -> None:
    logger.info("")
    logger.info("─" * 60)
    logger.info("  STEP %d/%d │ %s", step, total, title)
    logger.info("─" * 60)


def run_pipeline(viral_input: dict | None = None) -> dict:
    """
    Execute the full content automation pipeline.

    Parameters
    ----------
    viral_input : dict, optional
        Real viral post data (caption, hook, visuals, etc.).
        If None, the pipeline simulates viral content automatically.

    Returns
    -------
    dict
        All pipeline outputs including saved file paths.
    """
    total_steps = 8
    start_time  = time.time()

    logger.info("=" * 60)
    logger.info("  TechSoftware — Content Automation Pipeline")
    logger.info("=" * 60)

    # ── Step 1: Trending Topic ────────────────────────────────────────────────
    _banner(1, total_steps, "FETCH TRENDING TOPIC")
    topic = get_trending_topic()
    logger.info("Topic   : %s", topic["topic"])
    logger.info("Category: %s", topic.get("category", "—"))
    logger.info("Score   : %s/100", topic.get("score", "—"))
    logger.info("Source  : %s", topic.get("source", "—"))

    # ── Step 2: Viral Content ─────────────────────────────────────────────────
    _banner(2, total_steps, "FETCH / SIMULATE VIRAL CONTENT")
    if viral_input:
        viral_content = viral_input
        logger.info("Using provided real viral content")
    elif SIMULATE_VIRAL_DATA:
        viral_content = simulate_viral_content(topic)
        logger.info(
            "Simulated viral post | views=%s | likes=%s",
            viral_content.get("estimated_views", "—"),
            viral_content.get("estimated_likes", "—"),
        )
    else:
        raise ValueError(
            "SIMULATE_VIRAL_DATA=False but no viral_input provided. "
            "Either pass viral_input or enable simulation."
        )

    # ── Step 3: Viral Analysis ────────────────────────────────────────────────
    _banner(3, total_steps, "ANALYSE VIRAL CONTENT")
    analysis = analyze_viral_content(viral_content)
    logger.info("Hook type      : %s", analysis.get("hook_type", "—"))
    logger.info("Formula name   : %s", analysis.get("viral_formula_name", "—"))
    logger.info("Emotional trigger: %s", analysis.get("emotional_trigger", "—"))
    logger.info("Pain point     : %s", analysis.get("audience_pain_point", "—"))

    # ── Step 4: Content Improvement ──────────────────────────────────────────
    _banner(4, total_steps, "GENERATE CONTENT IMPROVEMENT")
    improvement = generate_improvement(topic, analysis)
    logger.info("Improved hook  : %s", improvement.get("improved_hook", "—"))
    logger.info("Why it wins    : %s", improvement.get("why_this_version_wins", "—"))

    # ── Step 5: Content Generation ───────────────────────────────────────────
    _banner(5, total_steps, "GENERATE ALL CONTENT ASSETS")
    generated = generate_all_content(topic, analysis, improvement)

    hooks      = generated["hooks"]
    script     = generated["reel_script"]
    carousel   = generated["carousel"]
    caption    = generated["caption"]

    logger.info(
        "Hooks       : %d generated | recommended=%d",
        len(hooks.get("hooks", [])),
        hooks.get("recommended_hook_id", "—"),
    )
    logger.info("Script      : %s | %d scenes",
                script.get("total_duration", "—"),
                len(script.get("scenes", [])))
    logger.info("Carousel    : %d slides", len(carousel.get("slides", [])))
    logger.info("Hashtags    : %d tags", len(caption.get("hashtags", [])))

    # ── Step 6: Quality Control ───────────────────────────────────────────────
    _banner(6, total_steps, "QUALITY CONTROL REVIEW")
    if QC_ENABLED:
        qc_result = run_quality_check(generated, topic)
        logger.info(
            "QC verdict  : %s | overall=%s/10",
            qc_result.get("qc_verdict", "—"),
            qc_result.get("scores", {}).get("overall", "—"),
        )
        if qc_result.get("issues_found"):
            logger.info("Issues found : %s", "; ".join(qc_result["issues_found"]))
    else:
        qc_result = {"qc_verdict": "SKIPPED", "passes_qc": True, "scores": {}}
        logger.info("QC skipped (QC_ENABLED=False)")

    # ── Step 7: Video Prompts ─────────────────────────────────────────────────
    _banner(7, total_steps, "BUILD VIDEO GENERATION PROMPTS")
    video_prompts = build_video_prompts(script, topic)
    logger.info(
        "Video prompts: %d Runway + %d Pika scenes | status=%s",
        len(video_prompts.get("runway_prompts", [])),
        len(video_prompts.get("pika_prompts", [])),
        video_prompts.get("status", "—"),
    )

    # ── Step 8: Design Prompts ────────────────────────────────────────────────
    _banner(8, total_steps, "BUILD DESIGN / IMAGE GENERATION PROMPTS")
    design_prompts = build_design_prompts(carousel, hooks, topic)
    logger.info(
        "Design prompts: %d slides + thumbnail | status=%s",
        len(design_prompts.get("slide_prompts", [])),
        design_prompts.get("status", "—"),
    )

    # ── Save Outputs ──────────────────────────────────────────────────────────
    logger.info("")
    logger.info("─" * 60)
    logger.info("  SAVING ALL OUTPUTS")
    logger.info("─" * 60)

    saved_paths = save_pipeline_outputs(
        topic         = topic,
        viral_analysis= {**analysis, "improvement": improvement},
        generated_content = generated,
        qc_result     = qc_result,
        video_prompts = video_prompts,
        design_prompts= design_prompts,
    )

    elapsed = time.time() - start_time

    # ── Summary ───────────────────────────────────────────────────────────────
    logger.info("")
    logger.info("=" * 60)
    logger.info("  PIPELINE COMPLETE  (%.1f seconds)", elapsed)
    logger.info("=" * 60)
    logger.info("Trending topic  : %s", topic["topic"])
    logger.info("Viral formula   : %s", analysis.get("viral_formula_name", "—"))
    logger.info("QC verdict      : %s", qc_result.get("qc_verdict", "—"))
    logger.info("Files saved     : %d", len(saved_paths))
    for label, path in saved_paths.items():
        logger.info("  %-20s %s", label, path)
    logger.info("=" * 60)

    return {
        "topic":          topic,
        "viral_content":  viral_content,
        "analysis":       analysis,
        "improvement":    improvement,
        "generated":      generated,
        "qc_result":      qc_result,
        "video_prompts":  video_prompts,
        "design_prompts": design_prompts,
        "saved_paths":    saved_paths,
        "elapsed_seconds": round(elapsed, 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Example: run with real viral content data instead of simulation
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_VIRAL_INPUT = {
    "platform": "Instagram Reels",
    "topic": "Meta Ads are wasting your budget",
    "estimated_views": "1.8M",
    "estimated_likes": "62K",
    "hook_text": "Stop. Your Meta ads are lying to you.",
    "caption": (
        "Stop. Your Meta ads are lying to you.\n\n"
        "Here's what your dashboard hides:\n"
        "→ 40% of 'conversions' are duplicated\n"
        "→ iOS 17 broke last-click attribution\n"
        "→ Your ROAS is inflated by organic buyers\n\n"
        "I fixed this for 3 clients last month. Revenue stayed the same. "
        "Reported ROAS dropped 30%. Real profit went up 22%.\n\n"
        "DM me 'AUDIT' for a free 15-min ad account review."
    ),
    "visual_description": "Phone screen recording of Meta Ads Manager with red annotations",
    "audio_description": "Calm authoritative voiceover, minimal background music",
    "content_structure": [
        {"second_range": "0–3",  "what_happens": "Bold text: 'Your ads are lying to you'"},
        {"second_range": "3–15", "what_happens": "3 bullet points revealed one by one"},
        {"second_range": "15–35","what_happens": "Screen recording showing real client data"},
        {"second_range": "35–50","what_happens": "Results before/after fix"},
        {"second_range": "50–60","what_happens": "CTA: DM AUDIT"},
    ],
    "hashtags": ["#metaads", "#facebookads", "#digitalmarketing"],
    "cta_in_video": "DM me 'AUDIT' for a free ad account review",
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="TechSoftware Content Automation Pipeline")
    parser.add_argument(
        "--use-real-viral",
        action="store_true",
        help="Use the built-in SAMPLE_VIRAL_INPUT instead of AI simulation",
    )
    args = parser.parse_args()

    viral_data = SAMPLE_VIRAL_INPUT if args.use_real_viral else None

    try:
        results = run_pipeline(viral_input=viral_data)
        sys.exit(0)
    except EnvironmentError as exc:
        logger.error("Configuration error: %s", exc)
        logger.error("Make sure ANTHROPIC_API_KEY is set in your .env file")
        sys.exit(1)
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        sys.exit(1)
