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

### Attempt 1: Fix path and command structure (Current)
**Change:** Update Playwright config to use absolute paths and better error handling
**Reason:** The relative path `../snake-game-be` may not work correctly in CI
**Result:** ⏳ Testing...

