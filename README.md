# Sports Graphics Pipeline

A Python-based graphics rendering pipeline that transforms structured sports betting prediction data into clean, shareable visual outputs (matchup cards, daily pick slates, etc.).

> **Important:** This repository is **only** responsible for rendering graphics. It does **not** generate predictions or contain any machine learning logic.

---

## Purpose

Given structured pick data (JSON or CSV), this pipeline:

1. Loads the prediction data
2. Fetches team logos and background templates from `assets/`
3. Composites the graphic using Pillow (PIL)
4. Exports final images to `output/`

The pipeline is designed to be modular and easily extendable to support multiple sports (MLB, NBA, NFL, etc.).

---

## Project Structure

```
sports-graphics-pipeline/
├── assets/
│   ├── mlb/
│   │   ├── logos/          # Team logo PNGs
│   │   ├── templates/      # Card template images
│   │   └── backgrounds/    # Background images
│   ├── nba/
│   │   ├── logos/
│   │   ├── templates/
│   │   └── backgrounds/
│   └── nfl/
│       ├── logos/
│       ├── templates/
│       └── backgrounds/
├── config/
│   └── settings.json       # Global settings (fonts, colors, sizes)
├── data/
│   └── example_picks.json  # Example input data
├── examples/
│   └── example_daily_card.png  # Sample rendered output
├── output/                 # Generated graphics (git-ignored)
├── scripts/
│   ├── utils.py            # Helper functions (image loading, text placement)
│   ├── load_picks.py       # Load picks from JSON or CSV
│   ├── generate_single_pick.py   # Render a single matchup card
│   └── generate_daily_card.py    # Render a full-slate daily card
├── .github/
│   └── workflows/
│       └── generate_graphics.yml  # CI workflow
├── requirements.txt
└── README.md
```

---

## Input Data Format

Pick data should be structured as follows (JSON):

```json
{
  "sport": "mlb",
  "date": "2024-07-15",
  "picks": [
    {
      "away_team": "Yankees",
      "home_team": "Red Sox",
      "pick": "Yankees +1.5",
      "odds": "-110",
      "edge": 3.5,
      "confidence": "A"
    }
  ]
}
```

CSV format is also supported (see `data/example_picks.csv`).

---

## Scripts

| Script | Description |
|---|---|
| `scripts/load_picks.py` | Loads and validates pick data from JSON or CSV |
| `scripts/generate_single_pick.py` | Renders a single matchup graphic |
| `scripts/generate_daily_card.py` | Renders a full-slate daily card with all picks |
| `scripts/utils.py` | Shared helper functions (image I/O, text overlay, resizing) |

---

## Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Generate a daily card

```bash
python scripts/generate_daily_card.py --input data/example_picks.json
```

### Generate a single pick graphic

```bash
python scripts/generate_single_pick.py --input data/example_picks.json --index 0
```

---

## Configuration

Edit `config/settings.json` to customize:

- Card dimensions
- Font family and sizes
- Text colors
- Logo/text placement coordinates

---

## Adding Assets

- Place team logo PNGs in `assets/<sport>/logos/<TeamName>.png`
- Place background images in `assets/<sport>/backgrounds/`
- Place card template images in `assets/<sport>/templates/`

File names should match team names used in the pick data (e.g., `Yankees.png`).

---

## Output

Generated images are saved to the `output/` directory (excluded from version control).  
Example outputs are committed to `examples/` for reference.

---

## GitHub Actions

The workflow at `.github/workflows/generate_graphics.yml` can be triggered manually or on push to run the daily card generation script automatically.

---

## Dependencies

- [Pillow](https://python-pillow.org/) — image compositing
- [pandas](https://pandas.pydata.org/) — CSV data handling
