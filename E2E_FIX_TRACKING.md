# E2E Tests Fix Tracking

## Problem
E2E tests are failing in GitHub Actions CI with error: "Error: Process from config.webServer was not able to start. Exit code: 1"

## Root Cause Analysis
The Playwright config tries to start the backend server with:
```
cd ../snake-game-be && venv/bin/python bootstrap_db.py && venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Issues identified:
1. The path `../snake-game-be` may not be correct from the working directory in CI
2. The command uses `&&` which means if bootstrap_db.py fails, uvicorn won't start
3. The working directory in CI is `snake-game-fe` when Playwright runs
4. Need to check if `/health` endpoint exists

## Attempts and Changes

### Attempt 1: Fix command structure (Commit 877e12d)
**Change:** Changed `&&` to `;` in webServer command to allow uvicorn to start even if bootstrap fails
**Reason:** Thought bootstrap might be failing and preventing uvicorn from starting
**Result:** ❌ Failed - Still getting "Process from config.webServer was not able to start. Exit code: 1"

### Attempt 2: Fix DATABASE_URL format (Commit 7891fd9)
**Change:** Changed DATABASE_URL from `sqlite+aiosqlite:///./test_snake_game.db` to `sqlite:///./test_snake_game.db`
**Reason:** The error shows SQLAlchemy is failing to parse the database URL. The `session.py` file converts `sqlite://` to `sqlite+aiosqlite://` automatically, so we should pass the base format.
**Result:** ✅ **SUCCESS** - All E2E tests now pass! The entire CI/CD pipeline is working.

## Summary
The root cause was that the Playwright config was passing `sqlite+aiosqlite://` as the DATABASE_URL, but the `app/db/session.py` file expects `sqlite://` and automatically converts it to `sqlite+aiosqlite://`. Passing the already-converted format caused SQLAlchemy to fail parsing the URL with `ValueError: too many values to unpack (expected 2)`.

**Final Status:** ✅ All tests passing (backend, frontend unit, and E2E tests)

