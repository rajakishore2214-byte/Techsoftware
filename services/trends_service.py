"""
Fetches the highest-impact trending topic for the agency's niche.
Falls back to a curated list when pytrends is unavailable or rate-limited.
"""

import random
from typing import Any

from config import TRENDS_KEYWORDS, TRENDS_TIMEFRAME, TRENDS_GEO
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Fallback topic bank ───────────────────────────────────────────────────────
_FALLBACK_TOPICS: list[dict[str, Any]] = [
    {
        "topic": "AI Automation for Small Business Growth",
        "category": "AI in Business",
        "score": 97,
        "keywords": ["AI automation", "small business AI", "business growth automation"],
        "insight": "Businesses adopting AI tools report 40% faster operations — owners are searching for affordable entry points.",
        "source": "fallback",
    },
    {
        "topic": "Meta Ads Attribution Crisis: What Business Owners Must Know",
        "category": "Paid Ads Performance",
        "score": 94,
        "keywords": ["Meta ads attribution", "iOS 17 tracking", "ROAS accuracy"],
        "insight": "Post-iOS 17 privacy changes broke legacy attribution — advertisers are scrambling for server-side solutions.",
        "source": "fallback",
    },
    {
        "topic": "SEO Is Dying — Here's What Replaces It",
        "category": "Digital Marketing",
        "score": 91,
        "keywords": ["SEO future", "AI search", "GEO optimization", "Google SGE"],
        "insight": "Google SGE is reducing organic clicks; smart marketers are pivoting to Generative Engine Optimisation.",
        "source": "fallback",
    },
    {
        "topic": "LinkedIn Organic Reach Is at an All-Time High — Use It Now",
        "category": "Social Media Marketing",
        "score": 89,
        "keywords": ["LinkedIn organic", "B2B content", "thought leadership"],
        "insight": "LinkedIn's algorithm rewards native video and text posts more than ever — B2B brands seeing 3x reach.",
        "source": "fallback",
    },
    {
        "topic": "Why Your Website Is Losing Leads (And the Fix Takes 48 Hours)",
        "category": "Website Development",
        "score": 88,
        "keywords": ["conversion rate optimisation", "landing page", "lead capture"],
        "insight": "Most SMB websites have zero CRO — fixing one CTA placement can double inquiry volume.",
        "source": "fallback",
    },
    {
        "topic": "The 3-Step AI Content Engine Replacing Entire Marketing Teams",
        "category": "AI Automation",
        "score": 95,
        "keywords": ["AI content creation", "marketing automation", "AI agency"],
        "insight": "Agencies using AI pipelines deliver 10x output at 30% cost — clients are demanding this now.",
        "source": "fallback",
    },
]


def _fetch_pytrends() -> dict[str, Any] | None:
    """Attempt to fetch live data from Google Trends."""
    try:
        from pytrends.request import TrendReq  # noqa: PLC0415

        pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25), retries=1)
        pytrends.build_payload(
            kw_list=TRENDS_KEYWORDS[:5],
            timeframe=TRENDS_TIMEFRAME,
            geo=TRENDS_GEO,
        )
        interest_df = pytrends.interest_over_time()

        if interest_df.empty:
            logger.warning("pytrends returned an empty dataframe")
            return None

        # Drop 'isPartial' column if present
        if "isPartial" in interest_df.columns:
            interest_df = interest_df.drop(columns=["isPartial"])

        # Average score per keyword over the period
        avg_scores = interest_df.mean().sort_values(ascending=False)
        top_keyword = avg_scores.index[0]
        top_score   = int(avg_scores.iloc[0])

        logger.info("Trending topic from pytrends: '%s' (score %d)", top_keyword, top_score)
        return {
            "topic":    top_keyword,
            "category": "Google Trends",
            "score":    top_score,
            "keywords": list(avg_scores.index[:3]),
            "insight":  f"'{top_keyword}' is trending strongly in your niche with a relative score of {top_score}/100.",
            "source":   "pytrends",
        }

    except ImportError:
        logger.warning("pytrends not installed — using fallback topics")
    except Exception as exc:  # noqa: BLE001
        logger.warning("pytrends error (%s) — using fallback topics", exc)

    return None


def get_trending_topic() -> dict[str, Any]:
    """
    Return the single highest-impact trending topic.
    Tries pytrends first; falls back to curated list if unavailable.
    """
    live = _fetch_pytrends()
    if live:
        return live

    chosen = max(_FALLBACK_TOPICS, key=lambda t: t["score"])
    logger.info("Using fallback topic: '%s'", chosen["topic"])
    return chosen


def get_related_topics(topic: dict[str, Any]) -> list[str]:
    """Return secondary angle suggestions for the main topic."""
    return topic.get("keywords", [])[:3]
