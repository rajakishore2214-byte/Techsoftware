"""
Service to load and manage skill files (SOPs) for the LLM.
"""

import os
from pathlib import Path
from typing import Dict

from utils.logger import get_logger

logger = get_logger(__name__)

SKILLS_DIR = Path(__file__).parent.parent / "skills"

_cache: Dict[str, str] = {}

def get_skill(skill_name: str) -> str:
    """
    Load a skill by its name (without extension).
    Caches the loaded skill.
    """
    if skill_name in _cache:
        return _cache[skill_name]

    skill_path = SKILLS_DIR / f"{skill_name}.md"
    if not skill_path.exists():
        logger.warning(f"Skill file not found: {skill_path}")
        return ""

    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        _cache[skill_name] = content
        return content
    except Exception as e:
        logger.error(f"Failed to load skill {skill_name}: {e}")
        return ""

def get_digital_marketing_skill() -> str:
    return get_skill("digital-marketing-content")

def get_social_media_skill() -> str:
    return get_skill("social-media-marketing")

def get_kendrithm_visuals_skill() -> str:
    return get_skill("kendrithm-visuals")
