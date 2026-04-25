#!/usr/bin/env python3
"""
CLI entry point for the MLB matchup card generator.

Examples
--------
# Prediction card (Yankees vs Red Sox, pick NYY ML + OVER)
python generate_card.py --away NYY --home BOS --away-ml +150 --home-ml -180 \
    --ou-line 8.5 --ml-pick away --ou-pick OVER \
    --label "MLB 2026 | PREDICTIONS" --output output/nyy_vs_bos_pred.png

# Results card (pick was correct on ML, incorrect on O/U)
python generate_card.py --away NYY --home BOS --away-ml +150 --home-ml -180 \
    --ou-line 8.5 --ml-pick away --ou-pick OVER \
    --card-type results --ml-result correct --ou-result incorrect \
    --label "MLB 2026 | RESULTS" --output output/nyy_vs_bos_results.png
"""

import argparse
import sys
from pathlib import Path

from src.card_generator import CardData, generate_card


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate an MLB matchup prediction/results card."
    )
    p.add_argument("--away", required=True, metavar="ABBR", help="Away team abbreviation (e.g. NYY)")
    p.add_argument("--home", required=True, metavar="ABBR", help="Home team abbreviation (e.g. BOS)")
    p.add_argument("--away-ml", required=True, metavar="ODDS", help="Away team moneyline (e.g. +150)")
    p.add_argument("--home-ml", required=True, metavar="ODDS", help="Home team moneyline (e.g. -180)")
    p.add_argument("--ou-line", required=True, metavar="LINE", help="Over/Under total (e.g. 8.5)")
    p.add_argument("--ml-pick", choices=["away", "home"], default=None, help="Moneyline pick side")
    p.add_argument("--ou-pick", choices=["OVER", "UNDER"], default=None, help="Over/Under pick")
    p.add_argument(
        "--card-type", choices=["prediction", "results"], default="prediction",
        help="Card type (default: prediction)"
    )
    p.add_argument(
        "--ml-result", choices=["correct", "incorrect"], default=None,
        help="Moneyline result (results cards only)"
    )
    p.add_argument(
        "--ou-result", choices=["correct", "incorrect"], default=None,
        help="Over/Under result (results cards only)"
    )
    p.add_argument("--label", default="MLB | PREDICTIONS", help="Bottom-left label text")
    p.add_argument("--branding", default="ORBANALYTICS.SUBSTACK.COM", help="Bottom-right branding text")
    p.add_argument("--output", default="output/card.png", help="Output PNG path")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    card = CardData(
        away_team=args.away,
        home_team=args.home,
        away_ml=args.away_ml,
        home_ml=args.home_ml,
        ou_line=args.ou_line,
        ml_pick=args.ml_pick,
        ou_pick=args.ou_pick,
        card_type=args.card_type,
        ml_result=args.ml_result,
        ou_result=args.ou_result,
        label=args.label,
        branding=args.branding,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    img = generate_card(card)
    img.save(out_path)
    print(f"Card saved → {out_path}")


if __name__ == "__main__":
    main()
