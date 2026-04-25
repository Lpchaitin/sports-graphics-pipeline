# 📊 How to Generate Graphics from Your MLB Predictions

## Quick Usage

Once your GitHub Actions workflow is set up, graphics will generate automatically. But if you want to test locally:

### 1. Convert Your Predictions File

```bash
python scripts/convert_predictions.py modeling/mlb_xgb_ml/predictions/predictions_2026-04-19.csv
```

This will:
- ✅ Only include games where `pick_made? = 1`
- ✅ Convert odds to proper format (+138, -140)
- ✅ Set `ml_pick` based on your `pick_home?` column
- ✅ Leave `ou_pick` blank (since you're not making O/U predictions yet)
- ✅ Skip games where you don't have confidence in the pick

### 2. Generate Graphics

```bash
python scripts/process_picks.py converted_predictions_2026-04-19.csv \
    --output-dir output/mlb \
    --label "MLB 2026 | TODAY'S PICKS"
```

### 3. View Graphics

Check `output/mlb/` for PNG files like:
- `20260419_kc_at_nyy.png`
- `20260419_tb_at_pit.png`
- etc.

## What the Graphics Show

✅ **Moneyline Pick**: Highlighted in **green**
✅ **O/U Line**: Displayed in **gray** (not highlighted)
✅ **Team Colors**: Each team's primary color as background
✅ **White-Outlined Logos**: Clear, professional look

## Automated Workflow

When set up with GitHub Actions:

1. Your model saves predictions to `modeling/mlb_xgb_ml/predictions/`
2. You commit and push to GitHub
3. Workflow automatically:
   - Copies predictions to graphics-pipeline repo
   - Converts format
   - Generates graphics (only for games with picks)
   - Saves to `output/mlb/`

## Your Predictions File Format

Your CSV has these columns (we use these):
- `date` → game date
- `home team`, `away team` → team abbreviations
- `home odds`, `away odds` → moneyline odds
- `pick_made?` → **1 = generate graphic, 0 = skip**
- `pick_home?` → **1 = pick home team, 0 = pick away team**
- `over close` → O/U line (shown but not highlighted)

Columns we don't use (but you can keep):
- `xgb_home_prob`, `xgb_away_prob`
- `pick_fav?`, `fav at home?`
- `pick_correct?`
- `over close odds`, `under close odds`

## When You Start Making O/U Predictions

Add a column to your predictions file:
- `ou_pick?` → 1 for OVER, -1 for UNDER, 0 for no pick

Then update `scripts/convert_predictions.py` to map that column to `ou_pick`.

## Troubleshooting

**No graphics generated?**
- Check that some games have `pick_made? = 1`
- Verify team abbreviations match (NYY, BOS, etc.)

**Wrong team highlighted?**
- Check `pick_home?` column is correct (1 = home, 0 = away)

**Odds look wrong?**
- Converter adds +/- signs automatically
- 140 becomes +140, -140 stays -140
