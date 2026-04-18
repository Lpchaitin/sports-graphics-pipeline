"""
generate_single_pick.py
-----------------------
Render a single matchup graphic for one pick entry.

Usage (CLI):
    python scripts/generate_single_pick.py --input data/example_picks.json --index 0
    python scripts/generate_single_pick.py --input data/example_picks.csv  --index 1
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from PIL import ImageDraw

from load_picks import load_picks
from utils import (
    create_blank_card,
    draw_divider,
    draw_text,
    get_font,
    load_background,
    load_settings,
    load_team_logo,
    load_template,
    paste_image,
    save_image,
)


# ---------------------------------------------------------------------------
# Core rendering function
# ---------------------------------------------------------------------------

def render_single_pick(pick: dict[str, Any], sport: str, date: str) -> Any:  # PIL.Image
    """
    Compose a matchup graphic for a single *pick* dict and return the image.

    Layout (top → bottom):
      - Sport label + date
      - Team logos (away | VS | home)
      - Team names
      - Divider
      - Pick text (pick, odds)
      - Edge + confidence badge
    """
    settings = load_settings()
    card_cfg = settings["card"]
    font_cfg = settings["font"]
    logo_cfg = settings["logo"]
    layout_cfg = settings["layout"]

    width = card_cfg["width"]
    height = card_cfg["height"]
    pad = layout_cfg["padding"]
    cx = width // 2  # horizontal centre

    # ── Background ──────────────────────────────────────────────────────────
    card = load_background(sport, size=(width, height))
    template = load_template(sport)
    if template is not None:
        paste_image(card, template, (0, 0), center=False)

    draw = ImageDraw.Draw(card)

    # ── Fonts ────────────────────────────────────────────────────────────────
    font_title = get_font(font_cfg["size_title"], bold=True)
    font_body = get_font(font_cfg["size_body"])
    font_small = get_font(font_cfg["size_small"])

    c_primary = tuple(font_cfg["color_primary"])
    c_secondary = tuple(font_cfg["color_secondary"])
    c_accent = tuple(font_cfg["color_accent"])
    c_divider = tuple(layout_cfg["divider_color"])

    # ── Sport / Date header ──────────────────────────────────────────────────
    draw_text(draw, sport.upper(), (cx, 60), font_small, c_accent)
    draw_text(draw, date, (cx, 100), font_small, c_secondary)

    # ── Team logos ───────────────────────────────────────────────────────────
    logo_size = tuple(logo_cfg["size"])
    away_logo_pos = tuple(logo_cfg["away_position"])
    home_logo_pos = tuple(logo_cfg["home_position"])

    away_logo = load_team_logo(sport, pick["away_team"], logo_size)
    home_logo = load_team_logo(sport, pick["home_team"], logo_size)

    paste_image(card, away_logo, away_logo_pos)
    paste_image(card, home_logo, home_logo_pos)

    # ── VS label ─────────────────────────────────────────────────────────────
    draw_text(draw, "VS", (cx, away_logo_pos[1]), font_title, c_secondary)

    # ── Team names ───────────────────────────────────────────────────────────
    names_y = away_logo_pos[1] + logo_size[1] // 2 + 40
    draw_text(draw, pick["away_team"], (away_logo_pos[0], names_y), font_body, c_primary)
    draw_text(draw, pick["home_team"], (home_logo_pos[0], names_y), font_body, c_primary)

    # ── Divider ───────────────────────────────────────────────────────────────
    div_y = names_y + 60
    draw_divider(draw, div_y, pad, width - pad, c_divider, layout_cfg["divider_thickness"])

    # ── Pick info ─────────────────────────────────────────────────────────────
    pick_y = div_y + 60
    draw_text(draw, "PICK", (cx, pick_y), font_small, c_accent)
    draw_text(draw, pick["pick"], (cx, pick_y + 50), font_title, c_primary)
    draw_text(draw, f"Odds: {pick['odds']}", (cx, pick_y + 110), font_body, c_secondary)

    # ── Edge + Confidence ─────────────────────────────────────────────────────
    stats_y = pick_y + 180
    draw_divider(draw, stats_y - 20, pad, width - pad, c_divider, layout_cfg["divider_thickness"])
    draw_text(draw, f"Edge: {pick['edge']}%", (cx - 150, stats_y + 20), font_body, c_accent)
    draw_text(draw, f"Grade: {pick['confidence']}", (cx + 150, stats_y + 20), font_body, c_accent)

    return card


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Generate a single matchup pick graphic.")
    parser.add_argument("--input", required=True, help="Path to JSON or CSV picks file.")
    parser.add_argument(
        "--index", type=int, default=0,
        help="Zero-based index of the pick to render (default: 0)."
    )
    args = parser.parse_args()

    data = load_picks(args.input)
    picks = data["picks"]

    if args.index < 0 or args.index >= len(picks):
        raise IndexError(
            f"Index {args.index} is out of range. File contains {len(picks)} pick(s) (0–{len(picks)-1})."
        )

    pick = picks[args.index]
    card = render_single_pick(pick, data["sport"], data["date"])

    away = pick["away_team"].replace(" ", "_")
    home = pick["home_team"].replace(" ", "_")
    filename = f"{data['date']}_{data['sport']}_{away}_vs_{home}.png"
    save_image(card, filename)


if __name__ == "__main__":
    _cli()
