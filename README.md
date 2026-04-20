# 🎨 Sports Graphics Pipeline

Automated pipeline for generating professional sports prediction graphics from model predictions. Creates Instagram-ready graphics with team colors, logos, and betting picks.

![MLB Graphics Example](output/mlb/20260419_kc_at_nyy.png)

## 📊 Features

✅ **Automatic Graphics Generation** - GitHub Actions workflow generates graphics when predictions are committed  
✅ **Email Notifications** - Automatically emails graphics when generated (Gmail integration)  
✅ **Team Colors & Logos** - 30 MLB team logos with white outlines, primary color backgrounds  
✅ **Instagram-Optimized** - 1080×1350 (4:5 ratio) perfect for social media  
✅ **Smart Pick Highlighting** - Green borders on your picks, gray on non-picks  
✅ **Supports Multiple Sports** - Currently MLB, expandable to NBA/NFL  
✅ **Clean & Organized** - Automatic archiving and cleanup

## 🚀 Quick Start

1. **Setup GitHub Actions**: Follow [QUICKSTART.md](QUICKSTART.md)
2. **Understand the Organization**: Read [ORGANIZATION.md](ORGANIZATION.md)
3. **Learn to Use**: Check [USAGE.md](USAGE.md)

## 📁 Repository Organization

See **[ORGANIZATION.md](ORGANIZATION.md)** for complete details on:
- What gets committed vs ignored
- Directory structure and file lifecycle
- Keeping the repo clean and organized
- Storage strategy

## 🔗 Integration with MLB-Model

Your MLB model repo sends predictions here automatically:

```
MLB-Model/predictions_2026-04-19.csv 
    ↓ (GitHub Actions)
graphics-pipeline/incoming_picks/
    ↓ (Auto-converts & generates)
graphics-pipeline/output/mlb/*.png
    ↓ (Email workflow)
📧 Graphics emailed to you!
```

See **[INTEGRATION.md](INTEGRATION.md)** for all integration methods.

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Set up GitHub Actions in 10 minutes
- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Configure Gmail email notifications 📧
- **[ORGANIZATION.md](ORGANIZATION.md)** - Keep the repo clean and organized ⭐
- **[USAGE.md](USAGE.md)** - How to use with your predictions format
- **[INTEGRATION.md](INTEGRATION.md)** - Multiple integration methods
- **[WORKFLOW_SETUP.md](WORKFLOW_SETUP.md)** - Detailed workflow configuration

## 🛠️ Key Files

- `convert_predictions.py` - Converts your predictions format to graphics format
- `process_picks.py` - Batch processes CSV files into graphics
- `generate_card.py` - Single game graphic generator (CLI)
- `cleanup.sh` - Periodic cleanup script

## 📏 Current Status

- **Repo size**: ~4 MB (lean and clean!)
- **MLB logos**: 30 teams ✅
- **Graphics format**: 1080×1350 PNG
- **Auto-cleanup**: 30-day archive retention

## 🧹 Maintenance

Run periodic cleanup:
```bash
./cleanup.sh
```

This removes:
- Processed predictions older than 30 days
- Temporary conversion files
- Python cache files

## 💡 Tips

- Graphics available as **GitHub Actions Artifacts** (30-day retention)
- Only games with `pick_made? = 1` generate graphics
- Moneyline picks highlighted in green
- O/U lines shown in gray (when not making O/U picks)

---

**Repository maintained for clean, automated graphics generation from sports betting model predictions.**
