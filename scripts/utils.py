"""
utils.py
--------
Shared helper functions for the sports graphics pipeline.

Covers image I/O, text placement, logo loading, and resizing utilities
used by generate_single_pick.py and generate_daily_card.py.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Project root helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_settings() -> dict:
    """Load global settings from config/settings.json."""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------

def create_blank_card(width: int, height: int, color: Tuple[int, int, int]) -> Image.Image:
    """Create a blank RGBA card with the given dimensions and background color."""
    img = Image.new("RGBA", (width, height), (*color, 255))
    return img


def load_image(path: str | Path, size: Optional[Tuple[int, int]] = None) -> Image.Image:
    """
    Load an image from *path* and optionally resize it.

    If the file does not exist, returns a transparent placeholder of *size*
    (or 120×120 as a fallback) so the pipeline can still run without real assets.
    """
    path = Path(path)
    if path.exists():
        img = Image.open(path).convert("RGBA")
    else:
        fallback_size = size or (120, 120)
        img = Image.new("RGBA", fallback_size, (80, 80, 80, 180))

    if size:
        img = resize_image(img, size)
    return img


def resize_image(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Resize *img* to *size* while preserving aspect ratio (thumbnail)."""
    img = img.copy()
    img.thumbnail(size, Image.LANCZOS)
    return img


def paste_image(
    base: Image.Image,
    overlay: Image.Image,
    position: Tuple[int, int],
    center: bool = True,
) -> None:
    """
    Paste *overlay* onto *base* at *position*.

    If *center* is True, *position* is treated as the centre point of the overlay.
    Uses the overlay's alpha channel as the mask when available.
    """
    if center:
        x = position[0] - overlay.width // 2
        y = position[1] - overlay.height // 2
    else:
        x, y = position

    mask = overlay if overlay.mode == "RGBA" else None
    base.paste(overlay, (x, y), mask)


# ---------------------------------------------------------------------------
# Logo helpers
# ---------------------------------------------------------------------------

def load_team_logo(sport: str, team_name: str, size: Tuple[int, int]) -> Image.Image:
    """
    Load a team logo PNG from assets/<sport>/logos/<TeamName>.png.

    Falls back to a coloured placeholder if the file is not found.
    """
    logo_path = ASSETS_DIR / sport / "logos" / f"{team_name}.png"
    return load_image(logo_path, size=size)


# ---------------------------------------------------------------------------
# Background / template helpers
# ---------------------------------------------------------------------------

def load_background(sport: str, name: str = "default", size: Optional[Tuple[int, int]] = None) -> Image.Image:
    """
    Load a background image from assets/<sport>/backgrounds/<name>.png.

    Falls back to a dark solid colour if not found.
    """
    bg_path = ASSETS_DIR / sport / "backgrounds" / f"{name}.png"
    settings = load_settings()
    card_cfg = settings["card"]
    fallback_size = size or (card_cfg["width"], card_cfg["height"])

    if bg_path.exists():
        img = Image.open(bg_path).convert("RGBA")
        img = img.resize(fallback_size, Image.LANCZOS)
        return img

    bg_color = tuple(card_cfg["background_color"])
    return Image.new("RGBA", fallback_size, (*bg_color, 255))


def load_template(sport: str, name: str = "default") -> Optional[Image.Image]:
    """
    Load an optional overlay template from assets/<sport>/templates/<name>.png.

    Returns None if the file does not exist so callers can skip compositing.
    """
    tpl_path = ASSETS_DIR / sport / "templates" / f"{name}.png"
    if tpl_path.exists():
        return Image.open(tpl_path).convert("RGBA")
    return None


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Return an ImageFont of the requested *size*.

    Tries to load a system TrueType font; falls back to the Pillow default
    bitmap font if none is available.
    """
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue
    # Pillow built-in fallback (no size control)
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Text placement helpers
# ---------------------------------------------------------------------------

def draw_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    position: Tuple[int, int],
    font: ImageFont.FreeTypeFont,
    color: Tuple[int, int, int],
    anchor: str = "mm",
) -> None:
    """
    Draw *text* on *draw* at *position* with the given *font* and *color*.

    *anchor* follows Pillow's text anchor convention (default ``"mm"`` = centred).
    """
    draw.text(position, text, font=font, fill=(*color, 255), anchor=anchor)


def draw_divider(
    draw: ImageDraw.ImageDraw,
    y: int,
    x_start: int,
    x_end: int,
    color: Tuple[int, int, int],
    thickness: int = 2,
) -> None:
    """Draw a horizontal divider line."""
    for i in range(thickness):
        draw.line([(x_start, y + i), (x_end, y + i)], fill=(*color, 200))


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def save_image(img: Image.Image, filename: str) -> Path:
    """
    Save *img* as a PNG to the output/ directory.

    Creates the directory if it does not exist. Returns the full output path.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename
    img.convert("RGB").save(out_path, format="PNG")
    print(f"Saved: {out_path}")
    return out_path
