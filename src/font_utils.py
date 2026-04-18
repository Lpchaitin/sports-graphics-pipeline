"""
Font loading utilities.

Priority order:
1. Oswald-Bold downloaded to assets/fonts/
2. DejaVu Sans Condensed Bold (system)
3. Liberation Sans Bold (system)
4. DejaVu Sans Bold (system)
5. PIL default (bitmap, last resort)
"""

import os
from pathlib import Path

from PIL import ImageFont

# Where we cache the downloaded font
_ASSETS_DIR = Path(__file__).parent.parent / "assets" / "fonts"
_OSWALD_PATH = _ASSETS_DIR / "Oswald-Bold.ttf"

# Public GitHub raw URL for Oswald Bold (Google Fonts mirror)
_OSWALD_URL = (
    "https://github.com/googlefonts/OswaldFont/raw/main/fonts/ttf/Oswald-Bold.ttf"
)

_SYSTEM_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
]


def _download_oswald() -> bool:
    """Attempt to download Oswald-Bold.ttf. Returns True on success."""
    try:
        import requests

        _ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        resp = requests.get(_OSWALD_URL, timeout=15)
        resp.raise_for_status()
        _OSWALD_PATH.write_bytes(resp.content)
        return True
    except Exception:
        return False


def _best_font_path() -> str | None:
    """Return the path to the best available font file, or None."""
    if _OSWALD_PATH.exists():
        return str(_OSWALD_PATH)
    if _download_oswald():
        return str(_OSWALD_PATH)
    for path in _SYSTEM_FONTS:
        if os.path.exists(path):
            return path
    return None


_FONT_PATH: str | None = _best_font_path()


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Return a PIL font at *size* points, using the best available typeface."""
    if _FONT_PATH:
        return ImageFont.truetype(_FONT_PATH, size)
    return ImageFont.load_default()
