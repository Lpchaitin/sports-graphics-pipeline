"""
generate_daily_card.py
----------------------
Render a full-slate daily card that displays all picks for a given date.

Usage (CLI):
    python scripts/generate_daily_card.py --input data/example_picks.json
    python scripts/generate_daily_card.py --input data/example_picks.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from load_picks import load_picks
from utils import (
    draw_divider,
    draw_text,
    get_font,
    load_background,
    load_settings,
    load_team_logo,
    paste_image,
    save_image,
)


# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

# Height reserved for the header section (sport label + date)
HEADER_HEIGHT = 160
# Height allocated per pick row
ROW_HEIGHT = 200
# Extra bottom padding
FOOTER_PAD = 60


# ---------------------------------------------------------------------------
# Core rendering functions
# ---------------------------------------------------------------------------

def _render_header(draw: ImageDraw.ImageDraw, sport: str, date: str, width: int, settings: dict) -> None:
    """Draw the sport label and date in the header area."""
    font_cfg = settings["font"]
    cx = width // 2

    font_title = get_font(font_cfg["size_title"], bold=True)
    font_small = get_font(font_cfg["size_small"])

    c_accent = tuple(font_cfg["color_accent"])
    c_secondary = tuple(font_cfg["color_secondary"])

    draw_text(draw, sport.upper(), (cx, 55), font_title, c_accent)
    draw_text(draw, f"Daily Picks  ·  {date}", (cx, 110), font_small, c_secondary)


def _render_pick_row(
    card: Image.Image,
    draw: ImageDraw.ImageDraw,
    pick: dict[str, Any],
    sport: str,
    row_top: int,
    width: int,
    settings: dict,
) -> None:
    """Render one pick row onto *card* starting at *row_top* (y-coordinate)."""
    font_cfg = settings["font"]
    logo_cfg = settings["logo"]
    layout_cfg = settings["layout"]
    pad = layout_cfg["padding"]

    logo_size = (80, 80)  # Smaller logos for the daily card
    cx = width // 2
    logo_y = row_top + ROW_HEIGHT // 2 - 10

    c_primary = tuple(font_cfg["color_primary"])
    c_secondary = tuple(font_cfg["color_secondary"])
    c_accent = tuple(font_cfg["color_accent"])
    c_divider = tuple(layout_cfg["divider_color"])

    font_body = get_font(font_cfg["size_body"], bold=True)
    font_small = get_font(font_cfg["size_small"])

    # Logos
    away_logo = load_team_logo(sport, pick["away_team"], logo_size)
    home_logo = load_team_logo(sport, pick["home_team"], logo_size)
    paste_image(card, away_logo, (pad + 50, logo_y))
    paste_image(card, home_logo, (width - pad - 50, logo_y))

    # Matchup label
    matchup = f"{pick['away_team']}  @  {pick['home_team']}"
    draw_text(draw, matchup, (cx, row_top + 55), font_body, c_primary)

    # Pick + odds
    pick_str = f"{pick['pick']}   {pick['odds']}"
    draw_text(draw, pick_str, (cx, row_top + 105), font_small, c_accent)

    # Edge + confidence (right-aligned block)
    stats_str = f"Edge: {pick['edge']}%   Grade: {pick['confidence']}"
    draw_text(draw, stats_str, (cx, row_top + 150), font_small, c_secondary)

    # Row divider
    draw_divider(
        draw,
        row_top + ROW_HEIGHT - 10,
        pad,
        width - pad,
        c_divider,
        layout_cfg["divider_thickness"],
    )


def render_daily_card(data: dict[str, Any]) -> Image.Image:
    """
    Compose a full-slate daily card from *data* and return the image.

    The card height is computed dynamically based on the number of picks.
    """
    settings = load_settings()
    card_cfg = settings["card"]
    layout_cfg = settings["layout"]

    sport = data["sport"]
    date = data["date"]
    picks = data["picks"]

    width = card_cfg["width"]
    height = HEADER_HEIGHT + (len(picks) * ROW_HEIGHT) + FOOTER_PAD

    # ── Background ──────────────────────────────────────────────────────────
    card = load_background(sport, size=(width, height))
    draw = ImageDraw.Draw(card)

    # ── Header ───────────────────────────────────────────────────────────────
    _render_header(draw, sport, date, width, settings)

    # Divider below header
    draw_divider(
        draw,
        HEADER_HEIGHT - 10,
        layout_cfg["padding"],
        width - layout_cfg["padding"],
        tuple(layout_cfg["divider_color"]),
        layout_cfg["divider_thickness"] + 1,
    )

    # ── Pick rows ────────────────────────────────────────────────────────────
    for i, pick in enumerate(picks):
        row_top = HEADER_HEIGHT + i * ROW_HEIGHT
        _render_pick_row(card, draw, pick, sport, row_top, width, settings)

    return card


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Generate a daily picks slate graphic.")
    parser.add_argument("--input", required=True, help="Path to JSON or CSV picks file.")
    args = parser.parse_args()

    data = load_picks(args.input)
    card = render_daily_card(data)

    filename = f"{data['date']}_{data['sport']}_daily_card.png"
    save_image(card, filename)


if __name__ == "__main__":
    _cli()
