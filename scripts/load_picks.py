"""
load_picks.py
-------------
Load and validate sports betting pick data from JSON or CSV files.

Usage (CLI):
    python scripts/load_picks.py --input data/example_picks.json
    python scripts/load_picks.py --input data/example_picks.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

# ---------------------------------------------------------------------------
# Required fields for a single pick entry
# ---------------------------------------------------------------------------

REQUIRED_PICK_FIELDS = {"away_team", "home_team", "pick", "odds", "edge", "confidence"}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_from_json(path: str | Path) -> dict[str, Any]:
    """
    Load pick data from a JSON file.

    Expected structure::

        {
            "sport": "mlb",
            "date": "YYYY-MM-DD",
            "picks": [
                {
                    "away_team": "...",
                    "home_team": "...",
                    "pick": "...",
                    "odds": "...",
                    "edge": 3.5,
                    "confidence": "A"
                },
                ...
            ]
        }

    Returns the parsed dict after basic validation.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    _validate_json_data(data)
    return data


def load_from_csv(path: str | Path) -> dict[str, Any]:
    """
    Load pick data from a CSV file and normalise it into the standard dict format.

    Expected columns: sport, date, away_team, home_team, pick, odds, edge, confidence

    All rows must share the same *sport* and *date* values; if they differ the
    first row's values are used and a warning is printed.

    Returns a dict that mirrors the JSON structure.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]

    required_cols = {"sport", "date", "away_team", "home_team", "pick", "odds", "edge", "confidence"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    if df["sport"].nunique() > 1 or df["date"].nunique() > 1:
        print(
            "Warning: CSV contains rows with different sport/date values. "
            "Using values from the first row."
        )

    sport = df["sport"].iloc[0].strip()
    date = df["date"].iloc[0].strip()

    picks = []
    for _, row in df.iterrows():
        picks.append(
            {
                "away_team": row["away_team"].strip(),
                "home_team": row["home_team"].strip(),
                "pick": row["pick"].strip(),
                "odds": row["odds"].strip(),
                "edge": float(row["edge"]),
                "confidence": row["confidence"].strip(),
            }
        )

    return {"sport": sport, "date": date, "picks": picks}


def load_picks(path: str | Path) -> dict[str, Any]:
    """
    Auto-detect format (JSON / CSV) from the file extension and load pick data.

    Returns a normalised dict with keys: sport, date, picks.
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        return load_from_json(path)
    elif suffix == ".csv":
        return load_from_csv(path)
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Use .json or .csv.")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _validate_json_data(data: dict[str, Any]) -> None:
    """Raise ValueError if the JSON data is missing required top-level keys."""
    for key in ("sport", "date", "picks"):
        if key not in data:
            raise ValueError(f"Input data is missing required key: '{key}'")

    if not isinstance(data["picks"], list) or len(data["picks"]) == 0:
        raise ValueError("'picks' must be a non-empty list.")

    for i, pick in enumerate(data["picks"]):
        missing = REQUIRED_PICK_FIELDS - set(pick.keys())
        if missing:
            raise ValueError(f"Pick #{i} is missing required fields: {missing}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Load and display pick data from a JSON or CSV file.")
    parser.add_argument("--input", required=True, help="Path to the input JSON or CSV file.")
    args = parser.parse_args()

    data = load_picks(args.input)
    print(f"Sport : {data['sport']}")
    print(f"Date  : {data['date']}")
    print(f"Picks : {len(data['picks'])}")
    for i, pick in enumerate(data["picks"], 1):
        print(
            f"  [{i}] {pick['away_team']} @ {pick['home_team']} — "
            f"{pick['pick']} ({pick['odds']}) | Edge: {pick['edge']} | Conf: {pick['confidence']}"
        )


if __name__ == "__main__":
    _cli()
