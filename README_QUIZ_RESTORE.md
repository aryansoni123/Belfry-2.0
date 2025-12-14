# Restoring Quizzes - Quick Guide

If quizzes disappear from your database, use these scripts to restore them.

## Quick Restore (Recommended)

**Safe restore - doesn't drop existing data:**

```bash
python restore_quizzes_safe.py
```

This script:
- ✅ Creates database tables if they don't exist
- ✅ Creates users if they don't exist
- ✅ Adds missing quizzes (only if they don't already exist)
- ✅ Generates 500+ test cases for each quiz
- ✅ **NEVER drops existing data**

## Full Reset (Use with Caution)

**WARNING: This will delete ALL existing data!**

```bash
python seed_sample_data.py
```

This script:
- ⚠️ Drops all tables and recreates them
- ⚠️ Deletes all existing quizzes, submissions, and users
- ✅ Creates fresh database with sample data

## Why Quizzes Might Disappear

1. **Database file deleted** - The SQLite database file (`instance/belfry.db`) was deleted
2. **Database reset** - Someone ran `init_db.py` or `seed_sample_data.py` which drops tables
3. **Schema migration** - Database schema changed and tables were recreated

## Prevention

- **Always use `restore_quizzes_safe.py`** for restoring quizzes
- **Never run `init_db.py`** unless you want to start fresh
- **Backup your database** before major changes:
  ```bash
  copy instance\belfry.db instance\belfry.db.backup
  ```

## Quick Commands

```bash
# Restore quizzes safely (recommended)
python restore_quizzes_safe.py

# Check current quiz count
python -c "from app import app, db; from models import Quiz; app.app_context().push(); print(f'Quizzes: {len(Quiz.query.all())}')"

# Verify all quizzes are active
python -c "from app import app, db; from models import Quiz; app.app_context().push(); [print(f'{q.title}: Active={q.is_active}') for q in Quiz.query.all()]"
```

