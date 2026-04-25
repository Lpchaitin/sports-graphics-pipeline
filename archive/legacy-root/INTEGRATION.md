# Integration Guide: MLB Model → Graphics Pipeline

This guide explains how to connect your MLB model repository to this graphics pipeline to automatically generate game graphics from your model's picks.

## 📋 CSV Format

Your model should output picks in CSV format with these columns:

### Required Columns:
- `away_team` - Away team abbreviation (e.g., NYY, BOS, LAD)
- `home_team` - Home team abbreviation
- `away_ml` - Away moneyline (e.g., +135, -110)
- `home_ml` - Home moneyline (e.g., -155, +100)
- `ou_line` - Over/Under line (e.g., 9.5, 8.0)

### Optional Columns:
- `date` - Game date in YYYY-MM-DD format (defaults to today)
- `ml_pick` - Your moneyline pick: `away` or `home` (leave blank for no pick)
- `ou_pick` - Your O/U pick: `OVER` or `UNDER` (leave blank for no pick)
- `ml_result` - ML result: `correct` or `incorrect` (for results cards)
- `ou_result` - O/U result: `correct` or `incorrect` (for results cards)

### Example CSV:
```csv
date,away_team,home_team,away_ml,home_ml,ou_line,ml_pick,ou_pick
2026-04-20,NYY,BOS,+135,-155,9.5,home,OVER
2026-04-20,LAD,SF,+120,-140,8.5,away,UNDER
2026-04-20,CHC,STL,-110,+100,8.0,away,
2026-04-20,HOU,SEA,-180,+155,7.5,,OVER
```

## 🔄 Integration Methods

### Method 1: Direct Script Call (Simplest)

After your model generates picks, call the batch processor:

```bash
# In your model repo
python /path/to/sports-graphics-pipeline/process_picks.py \
    model_output/daily_picks.csv \
    --output-dir graphics/mlb \
    --label "MLB 2026 | PREDICTIONS"
```

**In Python:**
```python
import subprocess
import os

# After your model generates picks.csv
subprocess.run([
    'python',
    '/path/to/sports-graphics-pipeline/process_picks.py',
    'picks.csv',
    '--output-dir', 'output/mlb',
    '--label', 'MLB 2026 | PREDICTIONS'
], check=True)
```

### Method 2: Python Import (Most Flexible)

Import the graphics pipeline as a module:

```python
import sys
sys.path.insert(0, '/path/to/sports-graphics-pipeline')

from src.card_generator import CardData, generate_card
import pandas as pd

# Read your model's picks
picks_df = pd.read_csv('model_output/daily_picks.csv')

for _, row in picks_df.iterrows():
    card = CardData(
        away_team=row['away_team'],
        home_team=row['home_team'],
        away_ml=row['away_ml'],
        home_ml=row['home_ml'],
        ou_line=str(row['ou_line']),
        ml_pick=row.get('ml_pick') if pd.notna(row.get('ml_pick')) else None,
        ou_pick=row.get('ou_pick') if pd.notna(row.get('ou_pick')) else None,
        label="MLB 2026 | PREDICTIONS",
        branding="ORBANALYTICS.SUBSTACK.COM"
    )
    
    img = generate_card(card)
    filename = f"output/mlb/{row['away_team'].lower()}_at_{row['home_team'].lower()}.png"
    img.save(filename)
    print(f"Generated: {filename}")
```

### Method 3: GitHub Actions Workflow

Set up automatic graphic generation when your model pushes picks to GitHub:

**In your model repo** (`.github/workflows/generate-graphics.yml`):
```yaml
name: Generate Graphics

on:
  push:
    paths:
      - 'output/picks.csv'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Clone graphics pipeline
        run: |
          git clone https://github.com/Lpchaitin/sports-graphics-pipeline.git
          cd sports-graphics-pipeline
          pip install -r requirements.txt
      
      - name: Generate graphics
        run: |
          python sports-graphics-pipeline/process_picks.py \
            output/picks.csv \
            --output-dir graphics/mlb
      
      - name: Commit graphics
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add graphics/
          git commit -m "Generated graphics for $(date +%Y-%m-%d)" || true
          git push
```

### Method 4: Shared Filesystem / Dropbox

If both repos are on the same machine or share a filesystem:

**In your model repo:**
```python
# Save picks to shared location
picks_df.to_csv('/shared/picks/daily_picks.csv', index=False)
```

**Run a cron job or scheduled task:**
```bash
# Run every day at 9 AM
0 9 * * * python /path/to/sports-graphics-pipeline/process_picks.py \
    /shared/picks/daily_picks.csv \
    --output-dir /shared/graphics/mlb
```

### Method 5: API Service (Advanced)

Turn the graphics pipeline into a web service:

**Create `api_server.py`:**
```python
from flask import Flask, request, send_file
from io import BytesIO
from src.card_generator import CardData, generate_card

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_graphic():
    data = request.json
    
    card = CardData(
        away_team=data['away_team'],
        home_team=data['home_team'],
        away_ml=data['away_ml'],
        home_ml=data['home_ml'],
        ou_line=data['ou_line'],
        ml_pick=data.get('ml_pick'),
        ou_pick=data.get('ou_pick'),
        label=data.get('label', 'MLB 2026 | PREDICTIONS'),
        branding=data.get('branding', 'ORBANALYTICS.SUBSTACK.COM')
    )
    
    img = generate_card(card)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**From your model repo:**
```python
import requests

response = requests.post('http://localhost:5000/generate', json={
    'away_team': 'NYY',
    'home_team': 'BOS',
    'away_ml': '+135',
    'home_ml': '-155',
    'ou_line': '9.5',
    'ml_pick': 'home',
    'ou_pick': 'OVER'
})

with open('graphic.png', 'wb') as f:
    f.write(response.content)
```

## 🎯 Recommended Workflow

**For development/testing:**
- Use **Method 1** (Direct Script Call) - Simple and straightforward

**For production:**
- Use **Method 2** (Python Import) if both repos are tightly coupled
- Use **Method 3** (GitHub Actions) for cloud automation
- Use **Method 5** (API Service) if you need to scale or separate services

## 📁 Example End-to-End Workflow

**1. Your model repo generates picks:**
```python
# In your MLB model repo
import pandas as pd

# Your model outputs predictions
picks = model.generate_daily_picks()

# Format as DataFrame
picks_df = pd.DataFrame({
    'date': picks['game_date'],
    'away_team': picks['away_abbr'],
    'home_team': picks['home_abbr'],
    'away_ml': picks['away_moneyline'],
    'home_ml': picks['home_moneyline'],
    'ou_line': picks['total'],
    'ml_pick': picks['ml_prediction'],  # 'away' or 'home'
    'ou_pick': picks['ou_prediction'],  # 'OVER' or 'UNDER'
})

# Save to CSV
picks_df.to_csv('output/daily_picks.csv', index=False)
print("✓ Picks saved to output/daily_picks.csv")
```

**2. Call graphics pipeline:**
```python
# Automatically generate graphics
import subprocess

result = subprocess.run([
    'python',
    '../sports-graphics-pipeline/process_picks.py',
    'output/daily_picks.csv',
    '--output-dir', 'output/graphics/mlb',
    '--label', f'MLB {datetime.now().year} | PREDICTIONS',
    '--branding', 'ORBANALYTICS.SUBSTACK.COM'
], capture_output=True, text=True)

print(result.stdout)
print("✓ Graphics generated!")
```

**3. Use the graphics:**
- Post to social media
- Embed in your Substack
- Send via email newsletter
- Upload to website

## 🧪 Testing the Integration

Use the provided example file:

```bash
# Test with example picks
python process_picks.py example_picks.csv --output-dir output/mlb/test

# Verify graphics were generated
ls -lh output/mlb/test/
```

## ⚙️ Team Abbreviations

Make sure your model uses the correct team abbreviations:

| Team | Abbreviation |
|------|--------------|
| Arizona Diamondbacks | ARI |
| Atlanta Braves | ATL |
| Baltimore Orioles | BAL |
| Boston Red Sox | BOS |
| Chicago Cubs | CHC |
| Chicago White Sox | CWS |
| Cincinnati Reds | CIN |
| Cleveland Guardians | CLE |
| Colorado Rockies | COL |
| Detroit Tigers | DET |
| Houston Astros | HOU |
| Kansas City Royals | KC |
| Los Angeles Angels | LAA |
| Los Angeles Dodgers | LAD |
| Miami Marlins | MIA |
| Milwaukee Brewers | MIL |
| Minnesota Twins | MIN |
| New York Mets | NYM |
| New York Yankees | NYY |
| Oakland Athletics | OAK |
| Philadelphia Phillies | PHI |
| Pittsburgh Pirates | PIT |
| San Diego Padres | SD |
| San Francisco Giants | SF |
| Seattle Mariners | SEA |
| St. Louis Cardinals | STL |
| Tampa Bay Rays | TB |
| Texas Rangers | TEX |
| Toronto Blue Jays | TOR |
| Washington Nationals | WSH |

See `src/team_data.py` for the complete reference.

## 🚨 Troubleshooting

**Graphics not generating?**
- Check CSV column names match exactly
- Verify team abbreviations are correct (case-insensitive)
- Ensure moneylines include + or - sign
- Check file paths are absolute or relative to working directory

**Missing logos?**
- Run `python download_mlb_logos.py` to download all logos with white outlines

**Wrong dimensions?**
- Graphics are 1080×1350 (4:5 Instagram ratio) by default
- Modify `CARD_WIDTH` and `CARD_HEIGHT` in `src/card_generator.py` if needed

## 📞 Need Help?

Check the example files:
- `example_picks.csv` - Sample CSV format
- `generate_sample.py` - Single game example
- `process_picks.py` - Batch processing script
