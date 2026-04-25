import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ── Directory Layout ──────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
OUTPUT_DIR  = BASE_DIR / "output"
SCRIPTS_DIR = OUTPUT_DIR / "scripts"
IMAGES_DIR  = OUTPUT_DIR / "images"
VIDEOS_DIR  = OUTPUT_DIR / "videos"

for _dir in [OUTPUT_DIR, SCRIPTS_DIR, IMAGES_DIR, VIDEOS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ── Claude / Anthropic ────────────────────────────────────────────────────────
ANTHROPIC_API_KEY  = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", None)
PRIMARY_MODEL      = "claude-sonnet-4-6"          # main generation & QC
FAST_MODEL         = "claude-haiku-4-5-20251001"  # lightweight tasks
QC_MODEL          = "claude-sonnet-4-6"

MAX_TOKENS    = 4096
QC_MAX_TOKENS = 2048

# ── Google Trends ─────────────────────────────────────────────────────────────
TRENDS_KEYWORDS = [
    "digital marketing",
    "AI in business",
    "advertising ROI",
    "social media marketing",
    "lead generation automation",
    "AI automation agency",
    "paid ads strategy",
]
TRENDS_TIMEFRAME = "now 7-d"
TRENDS_GEO       = ""   # global; set to "US" / "IN" etc. if needed

# ── Agency / Brand Context ────────────────────────────────────────────────────
AGENCY_NAME     = "TechSoftware"
AGENCY_SERVICES = [
    "SEO",
    "Website Development",
    "Digital Marketing",
    "AI Automation",
    "Paid Ads (Meta, Google, LinkedIn, TikTok, Twitter/X)",
    "Social Media Marketing",
]
TARGET_AUDIENCE = ["Business owners", "Startups", "Entrepreneurs"]
CONTENT_GOAL    = "Build trust, generate leads, convert high-value clients"
CONTENT_PLATFORMS = ["Instagram", "LinkedIn", "TikTok", "Facebook", "Twitter/X"]

# ── Pipeline Flags ────────────────────────────────────────────────────────────
QC_ENABLED          = True
MOCK_MEDIA_APIS     = True   # set False when real Runway/Canva keys are ready
SIMULATE_VIRAL_DATA = True   # set False to pass real scraped data
