# 🚀 Quick Start: Connect MLB-Model to Graphics Pipeline

## What You Need to Do Right Now

Follow these steps in order. Should take about 10 minutes.

---

## Step 1: Create GitHub Personal Access Token

1. **Go to:** https://github.com/settings/tokens
2. **Click:** "Generate new token (classic)"
3. **Fill in:**
   - Note: `MLB Model Graphics Access`
   - Expiration: `No expiration` (or set to 1 year)
   - **Check the `repo` box** (this gives full repository control)
4. **Click:** "Generate token" (bottom of page)
5. **COPY THE TOKEN** - it looks like `ghp_xxxxxxxxxxxxxxxxxxxx`
   - Save it temporarily - you won't see it again!

---

## Step 2: Add Token to Your MLB-Model Repo

1. **Go to:** https://github.com/Lpchaitin/MLB-Model/settings/secrets/actions
2. **Click:** "New repository secret"
3. **Enter:**
   - Name: `GRAPHICS_REPO_TOKEN`
   - Secret: [Paste the token you copied]
4. **Click:** "Add secret"

---

## Step 3: Copy Workflow File to MLB-Model Repo

In your MLB-Model repository, create this file:

**File:** `.github/workflows/send-picks-to-graphics.yml`

**Copy this content:**
```yaml
name: Send Picks to Graphics Pipeline

on:
  push:
    paths:
      - 'modeling/mlb_xgb_ml/predictions/**/*.csv'
  workflow_dispatch:
    inputs:
      picks_file:
        description: 'CSV file with picks to send'
        required: false
        default: 'modeling/mlb_xgb_ml/predictions/daily_picks.csv'

jobs:
  send-picks:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout MLB repo
        uses: actions/checkout@v4
      
      - name: Checkout graphics pipeline repo
        uses: actions/checkout@v4
        with:
          repository: Lpchaitin/sports-graphics-pipeline
          token: ${{ secrets.GRAPHICS_REPO_TOKEN }}
          path: graphics-pipeline
      
      - name: Copy picks to graphics repo
        run: |
          mkdir -p graphics-pipeline/incoming_picks
          
          PICKS_FILE="${{ github.event.inputs.picks_file || 'modeling/mlb_xgb_ml/predictions/daily_picks.csv' }}"
          
          if [ ! -f "$PICKS_FILE" ]; then
            echo "Error: Picks file not found: $PICKS_FILE"
            exit 1
          fi
          
          TIMESTAMP=$(date +%Y%m%d_%H%M%S)
          DEST_FILE="graphics-pipeline/incoming_picks/picks_${TIMESTAMP}.csv"
          
          cp "$PICKS_FILE" "$DEST_FILE"
          
          echo "✓ Copied $PICKS_FILE to $DEST_FILE"
      
      - name: Commit and push to graphics repo
        working-directory: graphics-pipeline
        run: |
          git config user.name "MLB Model Bot"
          git config user.email "mlb-model-bot@users.noreply.github.com"
          
          git add incoming_picks/*.csv
          
          if git diff --staged --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Add MLB picks for $(date +%Y-%m-%d)"
            git push
            echo "✓ Picks pushed to graphics pipeline repo"
          fi
      
      - name: Summary
        run: |
          echo "## Picks Sent Successfully! 📊" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "Your picks have been sent to the graphics pipeline repository." >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "View graphics: [Graphics Pipeline Actions](https://github.com/Lpchaitin/sports-graphics-pipeline/actions)" >> $GITHUB_STEP_SUMMARY
```

**Commands to create the file:**
```bash
cd /path/to/MLB-Model
mkdir -p .github/workflows
# Create the file above, then:
git add .github/workflows/send-picks-to-graphics.yml
git commit -m "Add workflow to send picks to graphics pipeline"
git push
```

---

## Step 4: Enable Permissions in Graphics Pipeline (This Repo)

1. **Go to:** https://github.com/Lpchaitin/sports-graphics-pipeline/settings/actions
2. **Scroll to:** "Workflow permissions"
3. **Select:** "Read and write permissions"
4. **Check:** "Allow GitHub Actions to create and approve pull requests"
5. **Click:** "Save"

---

## Step 5: Test It!

### Option A: Manual Test (Recommended First)

1. Go to: https://github.com/Lpchaitin/MLB-Model/actions
2. Click: "Send Picks to Graphics Pipeline" (left sidebar)
3. Click: "Run workflow" button (right side)
4. Click: Green "Run workflow" button
5. Wait ~30 seconds, then click on the workflow run to see progress
6. Check graphics pipeline: https://github.com/Lpchaitin/sports-graphics-pipeline/actions

### Option B: Automatic Test

1. In your MLB-Model repo, add or modify a CSV in `modeling/mlb_xgb_ml/predictions/`
2. Commit and push
3. Watch it automatically trigger!

---

## ✅ How to Know It's Working

**In MLB-Model repo:**
- Actions tab shows "Send Picks to Graphics Pipeline" run
- Green checkmark = success
- Click on the run to see logs

**In Graphics Pipeline repo:**
- Actions tab shows "Generate MLB Graphics" run  
- Green checkmark = graphics generated
- Check `output/mlb/` folder for PNG files
- Download graphics from "Artifacts" section

---

## 🎯 CSV Format Your Model Should Output

Save your picks as CSV with these columns:

```csv
date,away_team,home_team,away_ml,home_ml,ou_line,ml_pick,ou_pick
2026-04-20,NYY,BOS,+135,-155,9.5,home,OVER
2026-04-20,LAD,SF,+120,-140,8.5,away,UNDER
```

**Required:** away_team, home_team, away_ml, home_ml, ou_line
**Optional:** date, ml_pick (away/home), ou_pick (OVER/UNDER)

---

## 🔧 Troubleshooting

**"GRAPHICS_REPO_TOKEN not found"**
→ Go back to Step 2, make sure secret name is exactly `GRAPHICS_REPO_TOKEN`

**"Permission denied"**
→ Check token has `repo` scope and hasn't expired

**"File not found"**
→ Verify CSV path is `modeling/mlb_xgb_ml/predictions/daily_picks.csv` or update workflow

**Workflow doesn't trigger**
→ Check that workflow file is in `.github/workflows/` and pushed to main branch

---

## 📞 Questions?

Check the full guides:
- [WORKFLOW_SETUP.md](WORKFLOW_SETUP.md) - Detailed setup instructions
- [INTEGRATION.md](INTEGRATION.md) - Other integration methods

Or check workflow logs in the Actions tab of each repo.

---

**That's it! Once set up, every time you commit picks to your MLB repo, graphics will automatically generate.**
