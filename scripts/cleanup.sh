#!/bin/bash
# Cleanup script for sports-graphics-pipeline repo
# Run this periodically to keep the repo clean

set -e

echo "🧹 Cleaning up sports-graphics-pipeline repository..."
echo ""

# Clean old processed predictions (older than 30 days)
if [ -d "incoming_picks/processed" ]; then
    DELETED_CSVS=$(find incoming_picks/processed -name "*.csv" -mtime +30 -type f -delete -print | wc -l)
    if [ "$DELETED_CSVS" -gt 0 ]; then
        echo "✓ Deleted $DELETED_CSVS old prediction file(s) from incoming_picks/processed/"
    else
        echo "  No old predictions to delete (< 30 days)"
    fi
fi

# Clean any stray converted files in root
if ls converted_*.csv *_converted.csv 2>/dev/null >/dev/null; then
    rm -f converted_*.csv *_converted.csv
    echo "✓ Removed temporary converted CSV files"
fi

# Clean any test prediction files in root
if ls predictions_*.csv test_picks.csv 2>/dev/null >/dev/null; then
    rm -f predictions_*.csv test_picks.csv
    echo "✓ Removed test prediction files"
fi

# Optional: Clean old graphics (uncomment if needed)
# if [ -d "output/mlb" ]; then
#     DELETED_GRAPHICS=$(find output/mlb -name "*.png" -mtime +90 -type f -delete -print | wc -l)
#     if [ "$DELETED_GRAPHICS" -gt 0 ]; then
#         echo "✓ Deleted $DELETED_GRAPHICS old graphic(s) from output/mlb/"
#     fi
# fi

# Clean Python cache
if [ -d "__pycache__" ] || [ -d "src/__pycache__" ]; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo "✓ Removed Python cache files"
fi

echo ""
echo "✨ Cleanup complete! Repository is tidy."
echo ""

# Show current disk usage
echo "📊 Current directory sizes:"
du -sh assets/ src/ output/ incoming_picks/ 2>/dev/null || true
echo ""
echo "Total repo size:"
du -sh . 2>/dev/null || true
