# Incoming Picks Directory

This directory receives CSV files from your MLB model repository via GitHub Actions workflow.

## How It Works

1. Your MLB model repo generates picks as a CSV file
2. A GitHub Actions workflow in your MLB repo pushes the CSV here
3. This triggers the graphics generation workflow in this repo
4. After processing, CSVs are moved to `processed/` subdirectory

## Directory Structure

```
incoming_picks/
├── picks_YYYYMMDD_HHMMSS.csv    # Incoming picks (auto-processed)
└── processed/                    # Archived picks after graphics generated
    └── YYYYMMDD_HHMMSS_picks_*.csv
```

## CSV Format

See `example_picks.csv` in the root directory for the expected format.

Required columns:
- `away_team`, `home_team`, `away_ml`, `home_ml`, `ou_line`

Optional columns:
- `date`, `ml_pick`, `ou_pick`, `ml_result`, `ou_result`

## Workflow

This directory is monitored by `.github/workflows/generate-graphics.yml`:
- When a CSV appears here, graphics are automatically generated
- Generated graphics are saved to `output/mlb/`
- Processed CSVs are archived to `processed/` subdirectory

## Manual Testing

To test the workflow manually:

```bash
cp example_picks.csv incoming_picks/test.csv
git add incoming_picks/test.csv
git commit -m "Test picks"
git push
```

Check the Actions tab to see the workflow run.
