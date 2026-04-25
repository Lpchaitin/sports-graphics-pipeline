#!/usr/bin/env python3
"""
Generate a sample MLB game graphic - Yankees @ Red Sox
"""

from src.card_generator import CardData, generate_card

# Create a hypothetical Yankees @ Red Sox game
card = CardData(
    away_team="NYY",           # Yankees (away)
    home_team="BOS",           # Red Sox (home)
    away_ml="+135",            # Yankees moneyline
    home_ml="-155",            # Red Sox moneyline (favorite)
    ou_line="9.5",             # Over/Under total
    ml_pick="home",            # Picking Red Sox to win
    ou_pick="OVER",            # Picking Over 9.5
    card_type="prediction",
    label="MLB 2026 | PREDICTIONS",
    branding="ORBANALYTICS.SUBSTACK.COM",
)

print("Generating Yankees @ Red Sox sample graphic...")
print("=" * 60)
print(f"Away: {card.away_team} ({card.away_ml})")
print(f"Home: {card.home_team} ({card.home_ml})")
print(f"O/U: {card.ou_line}")
print(f"Pick: {card.home_team} ML + OVER")
print("=" * 60)

img = generate_card(card)
output_path = "output/nyy_at_bos_sample.png"
img.save(output_path)

print(f"✓ Saved graphic to {output_path}")
print(f"  Dimensions: {img.width}×{img.height} (4:5 ratio for Instagram)")
