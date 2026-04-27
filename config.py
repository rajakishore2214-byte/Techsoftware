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

# ── Gemini / Google ───────────────────────────────────────────────────────────
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
PRIMARY_MODEL      = "gemini-2.5-flash"           # main generation & QC
FAST_MODEL         = "gemini-2.5-flash"           # lightweight tasks
QC_MODEL           = "gemini-2.5-flash"

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
QC_ENABLED          = False
MOCK_MEDIA_APIS     = False   # set False when real Runway/Canva keys are ready
SIMULATE_VIRAL_DATA = True   # set False to pass real scraped data
