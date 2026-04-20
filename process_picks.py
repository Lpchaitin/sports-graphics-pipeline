#!/usr/bin/env python3
"""
Batch process MLB picks from CSV and generate graphics.

This script reads a CSV file with daily MLB picks and generates a graphic for each game.

CSV Format:
-----------
date,away_team,home_team,away_ml,home_ml,ou_line,ml_pick,ou_pick
2026-04-20,NYY,BOS,+135,-155,9.5,home,OVER
2026-04-20,LAD,SF,+120,-140,8.5,away,UNDER

Usage:
------
# Process today's picks
python process_picks.py picks.csv

# Process with custom output directory
python process_picks.py picks.csv --output-dir output/mlb

# Custom label and branding
python process_picks.py picks.csv --label "MLB 2026 | TODAY'S PICKS" --branding "YOUR_BRAND.COM"
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

from src.card_generator import CardData, generate_card


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate MLB graphics from CSV picks file"
    )
    parser.add_argument(
        "csv_file",
        help="Path to CSV file with picks (e.g., picks.csv)"
    )
    parser.add_argument(
        "--output-dir",
        default="output/mlb",
        help="Directory to save generated graphics (default: output/mlb)"
    )
    parser.add_argument(
        "--label",
        default="MLB 2026 | PREDICTIONS",
        help="Label text for graphics (default: MLB 2026 | PREDICTIONS)"
    )
    parser.add_argument(
        "--branding",
        default="ORBANALYTICS.SUBSTACK.COM",
        help="Branding text for graphics"
    )
    parser.add_argument(
        "--card-type",
        choices=["prediction", "results"],
        default="prediction",
        help="Type of card to generate (default: prediction)"
    )
    return parser.parse_args()


def read_picks_csv(csv_path: Path):
    """
    Read picks from CSV file.
    
    Expected columns:
    - date (YYYY-MM-DD)
    - away_team (e.g., NYY)
    - home_team (e.g., BOS)
    - away_ml (e.g., +135)
    - home_ml (e.g., -155)
    - ou_line (e.g., 9.5)
    - ml_pick (away/home or blank)
    - ou_pick (OVER/UNDER or blank)
    
    Optional columns (for results cards):
    - ml_result (correct/incorrect)
    - ou_result (correct/incorrect)
    """
    picks = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Validate required columns
        required_cols = ['away_team', 'home_team', 'away_ml', 'home_ml', 'ou_line']
        missing = [col for col in required_cols if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        
        for row in reader:
            # Clean up the data
            pick = {
                'date': row.get('date', ''),
                'away_team': row['away_team'].strip().upper(),
                'home_team': row['home_team'].strip().upper(),
                'away_ml': row['away_ml'].strip(),
                'home_ml': row['home_ml'].strip(),
                'ou_line': row['ou_line'].strip(),
                'ml_pick': row.get('ml_pick', '').strip().lower() or None,
                'ou_pick': row.get('ou_pick', '').strip().upper() or None,
                'ml_result': row.get('ml_result', '').strip().lower() or None,
                'ou_result': row.get('ou_result', '').strip().lower() or None,
            }
            
            # Validate ml_pick
            if pick['ml_pick'] and pick['ml_pick'] not in ['away', 'home']:
                print(f"Warning: Invalid ml_pick '{pick['ml_pick']}' for "
                      f"{pick['away_team']}@{pick['home_team']}, skipping pick")
                pick['ml_pick'] = None
            
            # Validate ou_pick
            if pick['ou_pick'] and pick['ou_pick'] not in ['OVER', 'UNDER']:
                print(f"Warning: Invalid ou_pick '{pick['ou_pick']}' for "
                      f"{pick['away_team']}@{pick['home_team']}, skipping pick")
                pick['ou_pick'] = None
            
            picks.append(pick)
    
    return picks


def generate_filename(pick: dict, output_dir: Path) -> Path:
    """Generate a filename for the graphic."""
    away = pick['away_team'].lower()
    home = pick['home_team'].lower()
    date_str = pick.get('date', datetime.now().strftime('%Y%m%d'))
    
    # Clean date string (remove hyphens)
    date_str = date_str.replace('-', '')
    
    filename = f"{date_str}_{away}_at_{home}.png"
    return output_dir / filename


def process_picks(csv_path: Path, output_dir: Path, label: str, branding: str, card_type: str):
    """Process all picks from CSV and generate graphics."""
    
    print(f"Reading picks from {csv_path}...")
    picks = read_picks_csv(csv_path)
    
    if not picks:
        print("No picks found in CSV file.")
        return
    
    print(f"Found {len(picks)} game(s) to process")
    print("=" * 60)
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    for i, pick in enumerate(picks, 1):
        try:
            print(f"\n[{i}/{len(picks)}] Generating: "
                  f"{pick['away_team']} @ {pick['home_team']}")
            
            # Create CardData object
            card = CardData(
                away_team=pick['away_team'],
                home_team=pick['home_team'],
                away_ml=pick['away_ml'],
                home_ml=pick['home_ml'],
                ou_line=pick['ou_line'],
                ml_pick=pick['ml_pick'],
                ou_pick=pick['ou_pick'],
                card_type=card_type,
                ml_result=pick['ml_result'],
                ou_result=pick['ou_result'],
                label=label,
                branding=branding,
            )
            
            # Generate graphic
            img = generate_card(card)
            
            # Save to file
            output_path = generate_filename(pick, output_dir)
            img.save(output_path)
            
            print(f"  ✓ Saved → {output_path}")
            if pick['ml_pick']:
                print(f"    ML Pick: {pick['ml_pick'].upper()}")
            if pick['ou_pick']:
                print(f"    O/U Pick: {pick['ou_pick']}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print(f"Complete! Successfully generated {success_count}/{len(picks)} graphics")
    if error_count > 0:
        print(f"Errors: {error_count}")
    print(f"Graphics saved to: {output_dir}")


def main():
    args = parse_args()
    
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)
    
    output_dir = Path(args.output_dir)
    
    process_picks(csv_path, output_dir, args.label, args.branding, args.card_type)


if __name__ == '__main__':
    main()
