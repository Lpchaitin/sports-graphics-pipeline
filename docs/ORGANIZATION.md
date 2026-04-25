# 📁 Repository Organization

## Directory Structure

```
sports-graphics-pipeline/
│
├── .github/
│   └── workflows/
│       ├── generate-graphics.yml                    # Active: Generates graphics when CSV arrives
│       └── TEMPLATE_send_picks_from_mlb_repo.yml   # Template: Copy to MLB-Model repo
│
├── assets/                                          # COMMITTED: Team logos and fonts
│   ├── mlb/                                        # MLB team logos (with white outlines)
│   │   ├── nyy.png, bos.png, etc.                 # 30 team logos
│   ├── nba/                                        # (Future: NBA logos)
│   └── nfl/                                        # (Future: NFL logos)
│
├── incoming_picks/                                  # TEMPORARY: Received predictions
│   ├── .gitkeep                                    # Git placeholder (committed)
│   ├── processed/                                  # Archived CSVs after processing
│   │   └── .gitkeep                               # Git placeholder (committed)
│   └── *.csv                                       # IGNORED: Incoming prediction files
│
├── output/                                          # IGNORED: Generated graphics
│   ├── mlb/                                        # MLB graphics (PNGs)
│   ├── nba/                                        # (Future: NBA graphics)
│   └── nfl/                                        # (Future: NFL graphics)
│
├── src/                                             # COMMITTED: Core graphics code
│   ├── __init__.py
│   ├── card_generator.py                           # Main graphics generation logic
│   ├── font_utils.py                               # Font handling
│   └── team_data.py                                # Team colors and data
│
├── scripts/                                         # COMMITTED: Executable scripts
│   ├── convert_predictions.py                      # Converts your format → graphics format
│   ├── process_picks.py                            # Batch process CSV → graphics
│   ├── generate_card.py                            # Single game CLI generator
│   ├── generate_sample.py                          # Sample generation script
│   ├── download_mlb_logos.py                       # One-time logo downloader
│   └── cleanup.sh                                  # Periodic cleanup script
│
├── docs/                                            # COMMITTED: Documentation
│   ├── QUICKSTART.md                               # Setup guide
│   ├── USAGE.md                                    # How to use guide
│   ├── INTEGRATION.md                              # Integration methods
│   ├── WORKFLOW_SETUP.md                           # Detailed workflow setup
│   ├── EMAIL_SETUP.md                              # Email configuration
│   └── ORGANIZATION.md                             # This file
│
├── examples/                                        # COMMITTED: Example files
│   └── example_picks.csv                           # Example file for reference
│
├── requirements.txt                                 # COMMITTED: Python dependencies
├── README.md                                        # COMMITTED: Main documentation
│
└── .gitignore                                       # COMMITTED: What NOT to commit
```

## What Gets Committed vs Ignored

### ✅ COMMITTED (in git)
- All source code (`src/`, `scripts/*.py`)
- Team logos (`assets/mlb/*.png`)
- Documentation (`docs/*.md`, `README.md`)
- Workflow files (`.github/workflows/`)
- Example files (`examples/example_picks.csv`)
- Dependencies (`requirements.txt`)
- Directory placeholders (`.gitkeep`)

### ❌ IGNORED (not in git)
- Generated graphics (`output/**/*.png`)
- Incoming prediction CSVs (`incoming_picks/*.csv`)
- Processed/archived CSVs (`incoming_picks/processed/*.csv`)
- Temporary conversion files (`*_converted.csv`, `converted_*.csv`)
- Python cache (`__pycache__/`, `*.pyc`)
- Test files (`predictions_*.csv`, `test_picks.csv`)

## Workflow Data Flow

```
MLB-Model Repo                          Graphics Pipeline Repo
──────────────                          ──────────────────────

predictions_2026-04-19.csv              
         │                              
         │ (GitHub Actions copies)      
         ↓                              
                                 ───→   incoming_picks/picks_TIMESTAMP.csv
                                              │
                                              │ (scripts/convert_predictions.py)
                                              ↓
                                        incoming_picks/picks_TIMESTAMP_converted.csv
                                              │
                                              │ (scripts/process_picks.py)
                                              ↓
                                        output/mlb/20260419_team_at_team.png
                                              │
                                              │ (archive original)
                                              ↓
                                        incoming_picks/processed/TIMESTAMP_picks_TIMESTAMP.csv
                                              │
                                              │ (cleanup converted)
                                              ↓
                                        [converted file deleted]
```

## File Lifecycle

1. **Prediction CSV arrives** → `incoming_picks/picks_TIMESTAMP.csv`
2. **Converted** → `incoming_picks/picks_TIMESTAMP_converted.csv` (temporary)
3. **Graphics generated** → `output/mlb/*.png`
4. **Original archived** → `incoming_picks/processed/TIMESTAMP_picks_TIMESTAMP.csv`
5. **Converted deleted** → Cleanup (not needed after graphics created)

## Keeping the Repo Clean

### Automatic Cleanup (by workflow)
- ✅ Converts predictions → generates graphics → deletes converted files
- ✅ Archives original predictions to `processed/` folder
- ✅ Only keeps necessary files in main directories

### Manual Cleanup (periodic)
```bash
# Clean old processed CSVs (older than 30 days)
find incoming_picks/processed -name "*.csv" -mtime +30 -delete

# Clean old graphics (older than 90 days)
find output/mlb -name "*.png" -mtime +90 -delete
```

### Download Graphics via GitHub Actions
- Graphics are available as **Artifacts** in each workflow run
- Download from Actions tab → no need to commit to repo
- Artifacts retained for 30 days automatically

## Storage Strategy

### What stays in repo long-term:
- **Source code** (small, essential)
- **Team logos** (30 MLB logos ≈ 5MB total)
- **Documentation** (text files, minimal size)

### What gets downloaded/deleted:
- **Graphics** (download from Actions artifacts)
- **Old predictions** (archive, then delete after 30 days)
- **Temporary files** (auto-deleted by workflow)

## Repository Size Management

Current estimated sizes:
- Source code: < 1 MB
- MLB logos: ≈ 4-5 MB
- Per day graphics (6 games): ≈ 1 MB
- Documentation: < 1 MB

**Total committed:** ~7 MB (very small!)
**Graphics (in artifacts only):** ~1 MB/day × 30 days = ~30 MB (auto-cleaned)

## Best Practices

1. **Don't commit**:
   - Generated graphics (use artifacts)
   - Prediction CSVs (temporary processing only)
   - Test files

2. **Do commit**:
   - Code changes
   - New team logos
   - Documentation updates

3. **Download graphics from**:
   - GitHub Actions artifacts
   - Or pull from `output/mlb/` after workflow runs (if you enable committing)

4. **Archive strategy**:
   - Keep processed predictions for 30 days (for debugging)
   - Auto-delete after that
   - Graphics available in artifacts for 30 days

## Optional: Committing Graphics

If you want graphics in the repo (not recommended for long-term):

**Enable in workflow** (`.github/workflows/generate-graphics.yml`):
```yaml
- name: Commit generated graphics
  run: |
    git add output/mlb/
    git commit -m "Graphics for $(date +%Y-%m-%d)" || true
    git push
```

**Pros:**
- Graphics always in repo
- Easy to browse history

**Cons:**
- Repo size grows ~1MB per day
- 365 days = ~365 MB

**Recommendation:** Use artifacts for downloads, keep repo lean.
