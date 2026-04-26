#!/usr/bin/env python3
"""
Convert MLB model predictions to graphics pipeline format.

This script transforms the predictions CSV from the MLB-Model repo
into the format expected by the graphics pipeline.

Usage:
    python convert_predictions.py predictions_2026-04-19.csv
    python convert_predictions.py predictions_2026-04-19.csv --output converted_picks.csv
"""

import argparse
import csv
import sys
from pathlib import Path


def convert_odds(odds_str):
    """
    Convert odds from model format to display format.
    
    Input: "140" or "-140" (as string or number)
    Output: "+140" or "-140"
    """
    try:
        odds = float(odds_str)
        if odds > 0:
            return f"+{int(odds)}"
        else:
            return f"{int(odds)}"
    except (ValueError, TypeError):
        return odds_str


def convert_predictions(input_file, output_file=None):
    """
    Convert predictions CSV to graphics format.
    
    Input columns:
        date, home team, away team, home odds, away odds, fav at home?,
        xgb_home_prob, xgb_away_prob, pick?, pick_fav?, pick_home?,
        pick_made?, pick_correct?, over close, over close odds, under close odds
    
    Output columns:
        date, away_team, home_team, away_ml, home_ml, ou_line, ml_pick, ou_pick
    """
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Default output file
    if output_file is None:
        output_file = input_path.parent / f"converted_{input_path.name}"
    
    converted_games = []
    skipped_count = 0
    
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Only process games where pick_made? = 1
            pick_made = (row.get('pick_made?') or '0').strip()
            if pick_made != '1':
                skipped_count += 1
                continue
            
            # Determine ML pick (home or away)
            pick_home = (row.get('pick_home?') or '0').strip()
            ml_pick = 'home' if pick_home == '1' else 'away'
            
            # Determine ML result (if available)
            pick_correct = (row.get('pick_correct?') or '').strip()
            if pick_correct:
                try:
                    # Handle both '1'/'0' and '1.0'/'0.0' formats
                    if float(pick_correct) == 1.0:
                        ml_result = 'correct'
                    elif float(pick_correct) == 0.0:
                        ml_result = 'incorrect'
                    else:
                        ml_result = ''  # No result yet
                except (ValueError, TypeError):
                    ml_result = ''  # No result yet (prediction mode)
            else:
                ml_result = ''  # No result yet (prediction mode)
            
            # Convert odds (add +/- signs)
            home_ml = convert_odds(row['home odds'])
            away_ml = convert_odds(row['away odds'])
            
            # Get team abbreviations
            home_team = (row['home team'] or '').strip().upper()
            away_team = (row['away team'] or '').strip().upper()
            
            # Get O/U line
            ou_line = (row['over close'] or '').strip()
            
            # Format date (convert from M/D/YYYY to YYYY-MM-DD if needed)
            date_str = (row['date'] or '').strip()
            if '/' in date_str:
                # Convert 4/19/2026 to 2026-04-19
                parts = date_str.split('/')
                if len(parts) == 3:
                    month, day, year = parts
                    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Create converted row
            converted_game = {
                'date': date_str,
                'away_team': away_team,
                'home_team': home_team,
                'away_ml': away_ml,
                'home_ml': home_ml,
                'ou_line': ou_line,
                'ml_pick': ml_pick,
                'ou_pick': '',  # No O/U picks yet
                'ml_result': ml_result,
                'ou_result': '',  # No O/U results yet
            }
            
            converted_games.append(converted_game)
    
    # Write converted CSV
    if converted_games:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['date', 'away_team', 'home_team', 'away_ml', 
                         'home_ml', 'ou_line', 'ml_pick', 'ou_pick',
                         'ml_result', 'ou_result']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(converted_games)
        
        print(f"✓ Converted {len(converted_games)} game(s) to {output_file}")
        if skipped_count > 0:
            print(f"  Skipped {skipped_count} game(s) where pick_made? = 0")
        
        return str(output_file)
    else:
        print("No games found where pick_made? = 1")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Convert MLB model predictions to graphics pipeline format"
    )
    parser.add_argument(
        'input_file',
        help='Input predictions CSV file'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: converted_<input_file>)'
    )
    
    args = parser.parse_args()
    convert_predictions(args.input_file, args.output)


if __name__ == '__main__':
    main()
