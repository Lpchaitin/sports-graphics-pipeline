"""
MLB matchup card generator.

Generates a 1080×1350 px PNG card (4:5 Instagram ratio) showing:
  - Top half: split logo panels (away | home) on team primary-color backgrounds
  - Bottom half: data table with TEAM / MONEY / O/U columns
  - Footer: label (e.g. "MLB 2026 | PREDICTIONS") and branding text

Usage::

    from src.card_generator import CardData, generate_card

    card = CardData(
        away_team="NYY",
        home_team="BOS",
        away_ml="+150",
        home_ml="-180",
        ou_line="8.5",
        ml_pick="away",       # "away", "home", or None
        ou_pick="OVER",       # "OVER", "UNDER", or None
        card_type="prediction",
        ml_result=None,       # "correct" / "incorrect" / None  (results cards only)
        ou_result=None,
        label="MLB 2026 | PREDICTIONS",
        branding="ORBANALYTICS.SUBSTACK.COM",
    )
    img = generate_card(card)
    img.save("output/nyy_vs_bos.png")
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import Literal

import requests
from PIL import Image, ImageDraw

from src.font_utils import get_font
from src.team_data import get_team

# ---------------------------------------------------------------------------
# Card dimensions (4:5 ratio for Instagram)
# ---------------------------------------------------------------------------
CARD_WIDTH = 1080
LOGO_HEIGHT = 720
DATA_HEIGHT = 630
CARD_HEIGHT = LOGO_HEIGHT + DATA_HEIGHT  # = 1350

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
BG_COLOR = (18, 18, 28)        # near-black navy
DIVIDER_COLOR = (35, 35, 50)   # subtle column separator
WHITE = (255, 255, 255)
GREEN = (57, 255, 20)          # neon green  #39FF14
RED = (255, 60, 60)            # bright red
GRAY = (130, 130, 140)         # inactive cells
DARK_GRAY = (55, 55, 65)       # inactive cell borders
TEAM_BOX_COLOR = (255, 255, 255)   # team name box border / text

BORDER_WIDTH = 3               # px — box stroke thickness
LOGO_PADDING = 60              # px — padding around logo inside its panel

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class CardData:
    """All inputs required to render one matchup card."""

    away_team: str        # e.g. "NYY"
    home_team: str        # e.g. "BOS"
    away_ml: str          # e.g. "+150"
    home_ml: str          # e.g. "-180"
    ou_line: str          # e.g. "8.5"
    ml_pick: Literal["away", "home"] | None = None
    ou_pick: Literal["OVER", "UNDER"] | None = None
    card_type: Literal["prediction", "results"] = "prediction"
    # For results cards — "correct" / "incorrect" / None
    ml_result: str | None = None
    ou_result: str | None = None
    label: str = "MLB | PREDICTIONS"
    branding: str = "ORBANALYTICS.SUBSTACK.COM"


# ---------------------------------------------------------------------------
# Logo fetching
# ---------------------------------------------------------------------------
_LOGO_CACHE: dict[str, Image.Image | None] = {}


def _fetch_logo(abbr: str) -> Image.Image | None:
    """Load team logo PNG from local assets; returns RGBA Image or None."""
    if abbr in _LOGO_CACHE:
        return _LOGO_CACHE[abbr]

    team = get_team(abbr)
    if team is None:
        _LOGO_CACHE[abbr] = None
        return None

    # Use local logo with white outline
    import os
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets", "mlb", f"{team['espn_abbr']}.png"
    )
    
    try:
        if os.path.exists(logo_path):
            img = Image.open(logo_path).convert("RGBA")
            _LOGO_CACHE[abbr] = img
            return img
        else:
            # Fallback to ESPN if local doesn't exist
            url = f"https://a.espncdn.com/i/teamlogos/mlb/500/{team['espn_abbr']}.png"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            _LOGO_CACHE[abbr] = img
            return img
    except Exception:
        _LOGO_CACHE[abbr] = None
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _darken(rgb: tuple[int, int, int], factor: float = 0.75) -> tuple[int, int, int]:
    """Return a darkened version of *rgb* for the panel background."""
    return tuple(int(c * factor) for c in rgb)  # type: ignore[return-value]


def _draw_rect_border(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    color: tuple[int, int, int],
    width: int = BORDER_WIDTH,
) -> None:
    """Draw a hollow rectangle border."""
    x0, y0, x1, y1 = xy
    for i in range(width):
        draw.rectangle([x0 + i, y0 + i, x1 - i, y1 - i], outline=color)


def _centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: int,
    cy: int,
    font,
    color: tuple[int, int, int],
) -> None:
    """Draw *text* centered on (*cx*, *cy*)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=color)


# ---------------------------------------------------------------------------
# Logo panel
# ---------------------------------------------------------------------------

def _draw_logo_panel(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    x_offset: int,
    panel_width: int,
    height: int,
    abbr: str,
) -> None:
    """Fill one half of the top section with team color and centred logo."""
    team = get_team(abbr)
    primary_rgb = _hex_to_rgb(team["primary_color"]) if team else (30, 30, 45)
    bg_rgb = _darken(primary_rgb, factor=0.6)

    # Background
    draw.rectangle([x_offset, 0, x_offset + panel_width, height], fill=bg_rgb)

    # Team logo
    logo = _fetch_logo(abbr)
    if logo:
        # Scale logo to fit with padding
        max_size = height - 2 * LOGO_PADDING
        logo_copy = logo.copy()
        logo_copy.thumbnail((max_size, max_size), Image.LANCZOS)
        lw, lh = logo_copy.size
        px = x_offset + (panel_width - lw) // 2
        py = (height - lh) // 2
        if logo_copy.mode == "RGBA":
            img.paste(logo_copy, (px, py), logo_copy)
        else:
            img.paste(logo_copy, (px, py))
    else:
        # Fallback: large abbr text
        font = get_font(80)
        _centered_text(
            draw, abbr.upper(), x_offset + panel_width // 2, height // 2, font, WHITE
        )

    # Subtle color strip at top of panel matching the full primary color
    strip_h = 8
    draw.rectangle(
        [x_offset, 0, x_offset + panel_width, strip_h], fill=primary_rgb
    )


# ---------------------------------------------------------------------------
# Data table
# ---------------------------------------------------------------------------

def _pick_colors(
    is_pick: bool,
    result: str | None,
    card_type: str,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """
    Return (border_color, text_color) for a data cell.

    - Non-pick cells: gray border, gray text.
    - Prediction cards: pick cells get green (indicating the prediction).
    - Results cards: pick correct → green, pick incorrect → red.
    """
    if not is_pick:
        return DARK_GRAY, GRAY

    if card_type == "prediction":
        return GREEN, GREEN

    # Results card
    if result == "correct":
        return GREEN, GREEN
    if result == "incorrect":
        return RED, RED
    # Pick was made but result unknown
    return GREEN, GREEN


def _draw_data_cell(
    draw: ImageDraw.ImageDraw,
    text: str,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    border_color: tuple[int, int, int],
    text_color: tuple[int, int, int],
    font,
    fill: tuple[int, int, int] = BG_COLOR,
) -> None:
    """Draw a bordered rectangle with centred text."""
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    _draw_rect_border(draw, (x0, y0, x1, y1), border_color)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    _centered_text(draw, text, cx, cy, font, text_color)


def _draw_data_section(
    draw: ImageDraw.ImageDraw,
    card: CardData,
    data_top: int,
) -> None:
    """Render the TEAM / MONEY / O/U table below the logo panels."""

    # ---- column geometry -----------------------------------------------
    margin = 22
    gutter = 12
    usable = CARD_WIDTH - 2 * margin
    col_w = (usable - 2 * gutter) // 3

    col1_x0 = margin
    col1_x1 = col1_x0 + col_w
    col2_x0 = col1_x1 + gutter
    col2_x1 = col2_x0 + col_w
    col3_x0 = col2_x1 + gutter
    col3_x1 = CARD_WIDTH - margin          # let last column absorb rounding

    # ---- vertical geometry ---------------------------------------------
    header_top = data_top + 60
    header_h = 60
    row_h = 145
    row_gap = 35
    row1_top = header_top + header_h + 35
    row2_top = row1_top + row_h + row_gap
    footer_y = row2_top + row_h + 60

    # ---- fonts ---------------------------------------------------------
    header_font = get_font(36)
    cell_font = get_font(42)
    footer_font = get_font(24)

    # ---- column headers ------------------------------------------------
    headers = ["TEAM", "MONEY", "O/U"]
    col_centers = [
        (col1_x0 + col1_x1) // 2,
        (col2_x0 + col2_x1) // 2,
        (col3_x0 + col3_x1) // 2,
    ]
    header_cy = header_top + header_h // 2
    for text, cx in zip(headers, col_centers):
        _centered_text(draw, text, cx, header_cy, header_font, WHITE)

    # Thin separator line under headers
    sep_y = header_top + header_h + 4
    draw.line(
        [(margin, sep_y), (CARD_WIDTH - margin, sep_y)],
        fill=DIVIDER_COLOR,
        width=1,
    )

    # ---- helper to get away/home display values -------------------------
    away_team_data = get_team(card.away_team)
    home_team_data = get_team(card.home_team)
    away_label = away_team_data["short"] if away_team_data else card.away_team
    home_label = home_team_data["short"] if home_team_data else card.home_team

    # O/U cell labels
    away_ou_text = f"O {card.ou_line}"
    home_ou_text = f"U {card.ou_line}"

    # ---- row 1 (away team) ---------------------------------------------
    r1_y0 = row1_top
    r1_y1 = row1_top + row_h

    # Team name (always white)
    _draw_data_cell(
        draw, away_label,
        col1_x0, r1_y0, col1_x1, r1_y1,
        TEAM_BOX_COLOR, WHITE, cell_font,
    )

    # Moneyline away
    ml_away_pick = card.ml_pick == "away"
    ml_bc, ml_tc = _pick_colors(ml_away_pick, card.ml_result, card.card_type)
    _draw_data_cell(
        draw, card.away_ml,
        col2_x0, r1_y0, col2_x1, r1_y1,
        ml_bc, ml_tc, cell_font,
    )

    # O/U away row (OVER side)
    ou_away_pick = card.ou_pick == "OVER"
    ou_away_bc, ou_away_tc = _pick_colors(ou_away_pick, card.ou_result, card.card_type)
    _draw_data_cell(
        draw, away_ou_text,
        col3_x0, r1_y0, col3_x1, r1_y1,
        ou_away_bc, ou_away_tc, cell_font,
    )

    # ---- row 2 (home team) ---------------------------------------------
    r2_y0 = row2_top
    r2_y1 = row2_top + row_h

    # Team name (always white)
    _draw_data_cell(
        draw, home_label,
        col1_x0, r2_y0, col1_x1, r2_y1,
        TEAM_BOX_COLOR, WHITE, cell_font,
    )

    # Moneyline home
    ml_home_pick = card.ml_pick == "home"
    ml_hbc, ml_htc = _pick_colors(ml_home_pick, card.ml_result, card.card_type)
    _draw_data_cell(
        draw, card.home_ml,
        col2_x0, r2_y0, col2_x1, r2_y1,
        ml_hbc, ml_htc, cell_font,
    )

    # O/U home row (UNDER side)
    ou_home_pick = card.ou_pick == "UNDER"
    ou_home_bc, ou_home_tc = _pick_colors(ou_home_pick, card.ou_result, card.card_type)
    _draw_data_cell(
        draw, home_ou_text,
        col3_x0, r2_y0, col3_x1, r2_y1,
        ou_home_bc, ou_home_tc, cell_font,
    )

    # ---- footer --------------------------------------------------------
    footer_cy = footer_y + footer_font.size // 2
    _centered_text(
        draw,
        card.label,
        CARD_WIDTH // 4,
        footer_cy,
        footer_font,
        GRAY,
    )
    _centered_text(
        draw,
        card.branding,
        3 * CARD_WIDTH // 4,
        footer_cy,
        footer_font,
        GRAY,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_card(card: CardData) -> Image.Image:
    """
    Render an MLB matchup card and return it as a PIL Image (RGB, 1080×1350).
    
    Instagram-compatible 4:5 aspect ratio.

    Parameters
    ----------
    card : CardData
        All the information needed to render the graphic.

    Returns
    -------
    PIL.Image.Image
        The finished card ready to be saved or displayed.
    """
    img = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    panel_w = CARD_WIDTH // 2

    # Top logo panels
    _draw_logo_panel(img, draw, 0, panel_w, LOGO_HEIGHT, card.away_team)
    _draw_logo_panel(img, draw, panel_w, panel_w, LOGO_HEIGHT, card.home_team)

    # Centre divider line between panels
    draw.line(
        [(CARD_WIDTH // 2, 0), (CARD_WIDTH // 2, LOGO_HEIGHT)],
        fill=BG_COLOR,
        width=4,
    )

    # Horizontal rule between top and data sections
    draw.rectangle(
        [0, LOGO_HEIGHT, CARD_WIDTH, LOGO_HEIGHT + 4], fill=DIVIDER_COLOR
    )

    # Data table
    _draw_data_section(draw, card, LOGO_HEIGHT + 4)

    return img
