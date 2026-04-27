# TechSoftware — AI Content Automation Platform

## Quick Start (3 steps)

### 1. Install dependencies

```bash
cd "E:\Agentic Model\Techsoftware"
pip install -r requirements.txt
```

### 2. Set your API key

```bash
copy .env.example .env
# Now edit .env and replace your_gemini_api_key_here with your real key
```

Get your key at: https://aistudio.google.com/app/apikey

### 3. Run the pipeline

```bash
# Auto-simulation mode (no real viral data needed)
python main.py

# Use the built-in real viral post example
python main.py --use-real-viral
```

---

## Project Structure

```
Techsoftware/
├── main.py                    # Pipeline orchestrator — run this
├── config.py                  # All settings (models, paths, flags)
├── requirements.txt
├── .env.example               # Copy to .env and add your keys
│
├── services/
│   ├── llm_service.py         # Claude API wrapper with prompt caching
│   ├── trends_service.py      # Google Trends + fallback topic bank
│   ├── viral_analyzer.py      # Viral content audit & intelligence
│   ├── content_generator.py   # Hooks, scripts, carousels, captions, QC
│   ├── video_service.py       # Video prompt builder (Runway ML / Pika)
│   └── design_service.py      # Design prompt builder (Midjourney / DALL-E 3)
│
├── utils/
│   ├── logger.py              # Structured logging to stdout + file
│   └── file_utils.py          # Output saving utilities
│
└── output/
    ├── scripts/               # Reel scripts (.txt)
    ├── images/                # Design prompts (.json)
    ├── videos/                # Video prompts (.json)
    ├── *_full_pipeline.json   # Complete pipeline output bundle
    ├── *_content.json         # Content assets (hooks, carousel, caption)
    ├── *_qc_report.json       # Quality control review
    └── pipeline.log           # Run logs
```

---

## Pipeline Steps

| Step | Module | What Happens |
|------|--------|-------------|
| 1 | `trends_service` | Fetch top trending topic (Google Trends or curated fallback) |
| 2 | `viral_analyzer` | Simulate or accept real viral content |
| 3 | `viral_analyzer` | Deep-analyse hook, structure, emotional triggers, formula |
| 4 | `viral_analyzer` | Generate improved content baseline |
| 5 | `content_generator` | Generate hooks, reel script, carousel, caption, hashtags |
| 6 | `content_generator` | QC review — score and improve all assets |
| 7 | `video_service` | Build per-scene prompts for Runway ML and Pika Labs |
| 8 | `design_service` | Build per-slide prompts for Midjourney, DALL-E 3, and Canva |
| 9 | `file_utils` | Save everything to `output/` |

---

## Configuration Options (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `PRIMARY_MODEL` | `gemini-1.5-pro` | Main generation model |
| `QC_MODEL` | `gemini-1.5-pro` | Quality control model |
| `FAST_MODEL` | `gemini-1.5-flash` | Lightweight tasks |
| `QC_ENABLED` | `True` | Run quality control pass |
| `SIMULATE_VIRAL_DATA` | `True` | Auto-simulate viral content |
| `MOCK_MEDIA_APIS` | `True` | Produce prompts instead of calling video/image APIs |
| `TRENDS_GEO` | `""` (global) | Set to `"US"`, `"IN"`, etc. for country-specific trends |

---

## Passing Real Viral Content

Instead of simulation, pass real post data:

```python
from main import run_pipeline

viral_data = {
    "platform": "Instagram Reels",
    "topic": "Why your Google Ads are losing money",
    "estimated_views": "980K",
    "hook_text": "Stop boosting posts. Here's why.",
    "caption": "Full caption text here...",
    "visual_description": "Presenter on camera with screen recording",
    "audio_description": "Direct, fast-paced voiceover",
    "content_structure": [
        {"second_range": "0-3", "what_happens": "Hook delivered to camera"},
        {"second_range": "3-20", "what_happens": "3 common mistakes shown"},
    ],
    "hashtags": ["#googleads", "#ppc"],
    "cta_in_video": "DM me AUDIT"
}

results = run_pipeline(viral_input=viral_data)
```

---

## Enabling Real Media APIs

### DALL-E 3 (images)

1. Add `OPENAI_API_KEY` to `.env`
2. Set `MOCK_MEDIA_APIS = False` in `config.py`
3. Uncomment OpenAI code in `services/design_service.py`

### Runway ML (video)

1. Add `RUNWAY_API_KEY` to `.env`
2. Set `MOCK_MEDIA_APIS = False` in `config.py`
3. Uncomment Runway code in `services/video_service.py`

---

## Sample API Call (programmatic)

```python
from main import run_pipeline

# Run with auto-simulation
results = run_pipeline()

# Access specific outputs
print(results["topic"]["topic"])
print(results["analysis"]["viral_formula_name"])
print(results["generated"]["hooks"]["hooks"][0]["text"])
print(results["generated"]["reel_script"]["total_duration"])
print(results["qc_result"]["qc_verdict"])
print(results["saved_paths"])
```

---

## Output Files Explained

| File | Contents |
|------|----------|
| `*_full_pipeline.json` | Everything in one bundle |
| `*_content.json` | Hooks, carousel slides, caption, hashtags, CTAs |
| `*_reel_script.txt` | Human-readable reel script with scene breakdown |
| `*_video_prompts.json` | Per-scene Runway ML and Pika prompts |
| `*_design_prompts.json` | Per-slide Midjourney / DALL-E 3 / Canva specs |
| `*_qc_report.json` | Scores, issues, and improvements from QC pass |
| `pipeline.log` | Full execution log |

See `output/sample_output.json` for a complete example.

---

## Troubleshooting

**`GEMINI_API_KEY is not set`**
→ Copy `.env.example` to `.env` and add your key.

**`pytrends` rate limit / empty data**
→ Normal. The pipeline automatically uses the curated fallback topic bank.

**`json.JSONDecodeError`**
→ Rare. Retry — the LLM occasionally wraps JSON in markdown. The parser handles it, but edge cases may slip through on very long outputs.

**Slow pipeline (>2 minutes)**
→ Each step makes a Gemini API call. Normal total run time: 45–90 seconds.
