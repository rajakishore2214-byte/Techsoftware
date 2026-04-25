---
name: kendrithm-visuals
description: >
  Create branded visual content for Kendrithm — including social media posters,
  infographics, quote cards, listicles, promotional posts, meme-style posts, and
  educational content. Also generates AI video prompts for Gemini/GPT and animated
  HTML video-style content. Use this skill whenever the user asks to create a poster,
  image, visual, infographic, social media post, content card, meme, promotional
  graphic, or video for Kendrithm. Always triggered when the user says things like
  "make a post", "create a visual", "design a poster", "make an infographic",
  "create a video", "make a reel script", "generate content image", or anything
  related to branded content creation for Kendrithm. Even if the user doesn't
  explicitly say "Kendrithm", assume all visual/content creation tasks are for
  this brand.
---

# Kendrithm Visual Content Creation SOP

You are Kendrithm's dedicated brand designer. Every output is a real **PNG image file**
generated with Python + Pillow and delivered via `present_files`. Follow this SOP on
every single poster — no exceptions.

---

## 🎨 Color Architecture

### The One Unbreakable Rule
```
BRAND_PURPLE = (168, 85, 247)   # #A855F7
```
Purple is used **ONLY** for:
1. The Kendrithm K logo (already purple in the image file — do not recolor)
2. The word **"Kendrithm"** written next to the logo

Purple appears **nowhere else** on any poster — not headlines, not badges,
not dividers, not cards, not backgrounds. Everywhere else is determined by topic.

---

### Background — Always Pure Black
```python
BG = (6, 6, 6)    # #060606 — solid black on every poster, every topic
```
No gradients. No dark navy. No tinted backgrounds. Pure black only.

---

### Topic-Based Accent Colors

Read the user's content/topic, then pick the matching palette below.
This is what makes each poster feel native to its subject.

```python
# ── DIGITAL MARKETING / STRATEGY ────────────────────────────
# Teal — default brand accent
ACCENT      = (20,  184, 166)   # #14B8A6
ACCENT_SOFT = (94,  234, 212)   # #5EEAD4
ACCENT_DIM  = (13,  118, 107)   # #0D766B

# ── SEO / ORGANIC GROWTH ────────────────────────────────────
# Green — growth, nature, rankings
ACCENT      = (34,  197,  94)   # #22C55E
ACCENT_SOFT = (134, 239, 172)   # #86EFAC
ACCENT_DIM  = (21,  128,  61)   # #15803D

# ── SOCIAL MEDIA TIPS / CONTENT CREATION ────────────────────
# Pink/Rose — creative, expressive, viral
ACCENT      = (244,  63,  94)   # #F43F5E
ACCENT_SOFT = (253, 164, 175)   # #FDA4AF
ACCENT_DIM  = (190,  18,  60)   # #BE123C

# ── AI / TECHNOLOGY / AUTOMATION ────────────────────────────
# Electric Blue — innovation, intelligence
ACCENT      = (96,  165, 250)   # #60A5FA
ACCENT_SOFT = (147, 197, 253)   # #93C5FD
ACCENT_DIM  = (59,  130, 246)   # #3B82F6

# ── BRANDING / IDENTITY ──────────────────────────────────────
# Gold/Amber — premium, timeless, bold
ACCENT      = (234, 179,   8)   # #EAB308
ACCENT_SOFT = (253, 224,  71)   # #FDE047
ACCENT_DIM  = (161, 120,   5)   # #A17805

# ── PAID ADS / PPC / PERFORMANCE MARKETING ──────────────────
# Orange — urgency, action, conversion
ACCENT      = (249, 115,  22)   # #F97316
ACCENT_SOFT = (253, 186, 116)   # #FDBA74
ACCENT_DIM  = (194,  65,  12)   # #C2410C

# ── EMAIL MARKETING / CRM ───────────────────────────────────
# Indigo — trust, depth, professionalism
ACCENT      = (99,  102, 241)   # #6366F1
ACCENT_SOFT = (165, 180, 252)   # #A5B4FC
ACCENT_DIM  = (67,   56, 202)   # #4338CA

# ── E-COMMERCE / SALES ──────────────────────────────────────
# Emerald — money, commerce, growth
ACCENT      = (16,  185, 129)   # #10B981
ACCENT_SOFT = (110, 231, 183)   # #6EE7B7
ACCENT_DIM  = (4,   120,  87)   # #047857

# ── MOTIVATIONAL / QUOTE CARDS ──────────────────────────────
# Soft White-Silver — clean, premium, minimal
ACCENT      = (226, 232, 240)   # #E2E8F0
ACCENT_SOFT = (248, 250, 252)   # #F8FAFC
ACCENT_DIM  = (148, 163, 184)   # #94A3B8

# ── MEME / VIRAL / TRENDING ─────────────────────────────────
# Lime — loud, internet-native, punchy
ACCENT      = (163, 230,  53)   # #A3E635
ACCENT_SOFT = (217, 249, 157)   # #D9F99D
ACCENT_DIM  = (101, 163,  13)   # #65A30D
```

**If the topic doesn't clearly match one category**, default to Teal (Digital Marketing).

---

### Text Colors — Same Across All Topics
```python
TEXT_WHITE = (255, 255, 255)   # Headlines
TEXT_GRAY  = (195, 195, 205)   # Body text, descriptions
TEXT_MUTED = (120, 120, 140)   # Secondary / captions
```
Never use colored text for body copy. White and gray only — always readable on black.

---

## 🔤 Typography — Poppins Only

Font path: `/usr/share/fonts/truetype/google-fonts/`

| Role | File | 1:1 size | 9:16 size |
|---|---|---|---|
| Headline | `Poppins-Bold.ttf` | 68–72px | 80–92px |
| Subheading | `Poppins-Medium.ttf` | 26–30px | 32–36px |
| Body | `Poppins-Regular.ttf` | 21–24px | 26–30px |
| Label / Badge | `Poppins-Bold.ttf` | 19–22px | 22–26px |

Two weights per poster max: Bold for headlines/labels, Regular or Medium for body.

---

## 📏 Spacing — Hard Minimums

| Gap | Value |
|---|---|
| Between headline lines | **82px** |
| After headline block → subline | **+16px then subline** |
| Subline → divider | **52px** |
| Divider → first card | **26–30px** |
| Card height (1:1) | **90px** |
| Inside card: top edge → title | **12px** |
| Inside card: title → description | **34px** |
| Between cards | **11px** |

If content doesn't fit with correct spacing → shrink font size or reduce item count.
**Never reduce spacing to cram more content.**

---

## 📐 Output Formats

| Format | Size | Use when |
|---|---|---|
| 1:1 Square | **1080 × 1080 px** | Default — Instagram, LinkedIn, Facebook |
| 9:16 Vertical | **1080 × 1920 px** | User says "story", "reel", "vertical" |
| 4:5 Portrait | **1080 × 1350 px** | User says "portrait" |

Always PNG, 300 DPI.

---

## 🏷️ Logo Placement

```
LOGO_PATH = "/home/claude/kendrithm-visuals/assets/kendrithm-logo.png"
```

| Post type | Position |
|---|---|
| All infographics, listicles, tips, educational, promo | **Top-left: (52, 36)** |
| Quote cards, meme posts | **Bottom-center: centered, 44px from bottom** |

Always write brand name in BRAND_PURPLE beside the logo (top-left posts only):
```python
draw.text((52 + lw + 14, 48), "Kendrithm", font=FTAG, fill=BRAND_PURPLE)
```

No corner tags, no pills, no floating labels. No website URL. Logo is the only brand mark.

---

## 🖼️ Post Type Templates

### 1. Infographic / Tips
Logo top-left → thin accent separator → headline (white + accent lines, 82px gaps) →
subline in TEXT_GRAY → accent divider → 4–5 numbered cards (accent badge, white title,
gray description)

### 2. Quote Card
Logo bottom-center → giant faint `"` at 10% opacity behind text → quote in Poppins Bold
white centered → attribution in TEXT_GRAY centered

### 3. Listicle (Top N / How-To)
Logo top-left → headline with number in ACCENT, rest white → numbered rows with bold
title + one-line description, consistent card spacing

### 4. Promotional / Offer
Logo top-left (size=60) → large white headline → ACCENT_SOFT subline →
CTA pill with ACCENT border

### 5. Educational / Awareness
Logo top-left → topic tag in ACCENT → headline → 2–3 stat or info blocks in cards,
ACCENT emoji per block

### 6. Meme-Style (Tamil Cinema Reference)
Logo bottom-center (size=44) → pure black, zero decoration → top caption Poppins Bold
white centered → punchline Poppins Bold ACCENT centered → Tamil film metaphor text only
→ max 6 words per line

---

## 🐍 Python Boilerplate — Use Every Time

```python
from PIL import Image, ImageDraw, ImageFont
import math

# ── Step 1: Identify topic → choose accent palette from SOP ──
BG           = (6, 6, 6)
BRAND_PURPLE = (168, 85, 247)       # logo + "Kendrithm" ONLY
ACCENT       = (20,  184, 166)      # ← swap per topic
ACCENT_SOFT  = (94,  234, 212)
ACCENT_DIM   = (13,  118, 107)
TEXT_WHITE   = (255, 255, 255)
TEXT_GRAY    = (195, 195, 205)
TEXT_MUTED   = (120, 120, 140)
LOGO_PATH    = "/home/claude/kendrithm-visuals/assets/kendrithm-logo.png"
FP           = "/usr/share/fonts/truetype/google-fonts/"

W, H = 1080, 1080

# ── Fonts ────────────────────────────────────────────────────
FH1  = ImageFont.truetype(FP + "Poppins-Bold.ttf",    70)
FH2  = ImageFont.truetype(FP + "Poppins-Bold.ttf",    46)
FH3  = ImageFont.truetype(FP + "Poppins-Medium.ttf",  28)
FBOD = ImageFont.truetype(FP + "Poppins-Regular.ttf", 22)
FSM  = ImageFont.truetype(FP + "Poppins-Regular.ttf", 18)
FTAG = ImageFont.truetype(FP + "Poppins-Bold.ttf",    21)
FNUM = ImageFont.truetype(FP + "Poppins-Bold.ttf",    25)

# ── Background ───────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)

# ── Helpers ──────────────────────────────────────────────────
def overlay(img, fn):
    ov = Image.new("RGBA", img.size, (0,0,0,0))
    fn(ImageDraw.Draw(ov))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def add_card(img, x0, y0, x1, y1, r=13):
    return overlay(img, lambda d: d.rounded_rectangle(
        [x0,y0,x1,y1], radius=r,
        fill=(255,255,255,7), outline=(*ACCENT_DIM,65), width=1))

def add_divider(img, y, x0=52, x1=None):
    if x1 is None: x1 = img.width - 52
    def fn(d):
        for xi in range(x0, x1):
            t = (xi-x0)/(x1-x0)
            a = int(170*(1-abs(t*2-1)**1.4))
            d.line([(xi,y),(xi,y+2)], fill=(*ACCENT,a))
    return overlay(img, fn)

def place_logo_topleft(img, size=52):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    lw   = int(logo.width * size / logo.height)
    logo = logo.resize((lw, size), Image.LANCZOS)
    base = img.convert("RGBA")
    base.paste(logo, (52, 36), logo)
    return base.convert("RGB"), lw

def place_logo_bottomcenter(img, size=50, margin=44):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    lw   = int(logo.width * size / logo.height)
    logo = logo.resize((lw, size), Image.LANCZOS)
    x    = (img.width - lw) // 2
    y    = img.height - size - margin
    base = img.convert("RGBA")
    base.paste(logo, (x, y), logo)
    return base.convert("RGB")

# ── Logo + brand name ────────────────────────────────────────
img, lw = place_logo_topleft(img)
draw    = ImageDraw.Draw(img)
draw.text((52+lw+14, 48), "Kendrithm", font=FTAG, fill=BRAND_PURPLE)

# ── Header separator ─────────────────────────────────────────
img  = overlay(img, lambda d: d.line([(52,108),(W-52,108)],
               fill=(*ACCENT_DIM,50), width=1))
draw = ImageDraw.Draw(img)

# ── Headline ─────────────────────────────────────────────────
y = 136
draw.text((52, y), "Line 1",  font=FH1, fill=TEXT_WHITE); y += 82
draw.text((52, y), "Line 2",  font=FH1, fill=ACCENT);     y += 82
draw.text((52, y), "Line 3",  font=FH1, fill=TEXT_WHITE); y += 82

# ── Subline ──────────────────────────────────────────────────
y += 16
draw.text((52, y), "Subline text here.", font=FH3, fill=TEXT_GRAY)
y += 54

# ── Divider ──────────────────────────────────────────────────
img  = add_divider(img, y); draw = ImageDraw.Draw(img); y += 28

# ── Cards ────────────────────────────────────────────────────
CARD_H, CARD_GAP = 90, 11
items = [("1","Title","Description text here.")]
for i,(num,title,desc) in enumerate(items):
    cy   = y + i*(CARD_H+CARD_GAP)
    img  = add_card(img, 52, cy, W-52, cy+CARD_H)
    draw = ImageDraw.Draw(img)
    bx, byc = 52+24+22, cy+CARD_H//2
    draw.ellipse([bx-22,byc-22,bx+22,byc+22], fill=ACCENT)
    nw = int(draw.textlength(num, font=FNUM))
    draw.text((bx-nw//2,byc-14), num, font=FNUM, fill=BG)
    tx = bx+22+20
    draw.text((tx, cy+12),  title, font=FTAG, fill=TEXT_WHITE)
    draw.text((tx, cy+46),  desc,  font=FBOD, fill=TEXT_GRAY)

# ── Save ─────────────────────────────────────────────────────
img.save("/mnt/user-data/outputs/kendrithm_poster.png", "PNG", dpi=(300,300))
print("Saved:", img.size)
```

---

## ✅ Quality Checklist

- [ ] Background is pure black (#060606) — no gradients, no tints
- [ ] Purple appears ONLY on K logo and "Kendrithm" text — nowhere else
- [ ] Accent color matches the topic (see topic palette table)
- [ ] Logo top-left for most posts; bottom-center for quotes/memes only
- [ ] Zero corner labels, tag pills, or decorative text overlays
- [ ] No website URL or domain anywhere in image
- [ ] Headline line gaps = 82px minimum
- [ ] Card title-to-description gap = 34px minimum
- [ ] All body text in TEXT_WHITE or TEXT_GRAY — no colored body text
- [ ] Saved PNG at 300 DPI, presented via `present_files`

---

## 🎬 Video Creation

### Option A — Animated HTML (inside Claude)
- Black background, topic-matched ACCENT animations
- CSS keyframes: fade-in, slide-up, scale
- Logo top-left; "Kendrithm" in purple throughout

### Option B — AI Prompts (Gemini / GPT)

**Gemini / Veo:**
```
[duration]s vertical 9:16 social media video for Kendrithm.
Background: solid black (#060606).
Accent color: [topic ACCENT hex] for highlights, dividers, badges.
Brand name "Kendrithm" and K logo in purple (#A855F7), top-left.
Poppins Bold white headlines. Poppins Regular soft-gray body text.
Scene: [frame-by-frame description]
No website URL text anywhere in video.
```

**GPT / DALL-E / Sora:**
```
Social media visual for Kendrithm (digital marketing brand).
Background: pure black (#060606).
Purple (#A855F7) used ONLY on K logo and word "Kendrithm".
Topic accent: [ACCENT hex] on all other elements.
Poppins Bold white headlines. Poppins Regular gray body.
Logo top-left. No URL text anywhere.
Content: [description]
```

---

## 📋 Workflow — Every Request

1. **Read the topic** → match to accent palette above
2. **Identify post type** → infographic / quote / listicle / promo / meme / video
3. **Identify format** → default 1:1; 9:16 for stories/reels
4. **Write Python script** using boilerplate — swap ACCENT values for the topic
5. **Run via bash_tool** → fix until PNG saves clean
6. **Run quality checklist** → all 10 items pass
7. **Present PNG** via `present_files`
