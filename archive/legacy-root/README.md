# Legacy Root Directory Archive

This directory contains the original files from the repository root that have been reorganized into proper directories.

## What Happened

On 2026-04-20, the repository was reorganized to improve structure and maintainability:

- **Scripts** moved to `scripts/` directory
- **Documentation** moved to `docs/` directory  
- **Examples** moved to `examples/` directory

Old files were preserved here for reference and easy rollback if needed.

## Archived Files

### Python Scripts (now in scripts/)
- `convert_predictions.py`
- `process_picks.py`
- `generate_card.py`
- `generate_sample.py`
- `download_mlb_logos.py`

### Shell Scripts (now in scripts/)
- `cleanup.sh`

### Documentation (now in docs/)
- `QUICKSTART.md`
- `USAGE.md`
- `INTEGRATION.md`
- `WORKFLOW_SETUP.md`
- `EMAIL_SETUP.md`
- `ORGANIZATION.md`

### Examples (now in examples/)
- `example_picks.csv`

## How to Restore (if needed)

If you need to restore the old structure:

```bash
# Copy scripts back to root
cp archive/legacy-root/*.py .
cp archive/legacy-root/cleanup.sh .

# Copy docs back to root
cp archive/legacy-root/*.md .

# Copy example back to root
cp archive/legacy-root/example_picks.csv .

# Revert workflow changes
git checkout HEAD~1 -- .github/workflows/generate-graphics.yml

# Remove new directories if desired
rm -rf scripts/ docs/ examples/
```

## Git History

All files were moved using `git mv` to preserve their complete commit history. You can view the history of any file with:

```bash
git log --follow archive/legacy-root/FILENAME
```

## Safe to Delete?

These files are **safe to delete** after confirming the reorganization works correctly. The complete history is preserved in git, so you can always retrieve them with:

```bash
git checkout <commit-hash> -- path/to/file
```
