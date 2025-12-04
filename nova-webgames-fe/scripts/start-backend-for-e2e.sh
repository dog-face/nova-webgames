#!/bin/bash
set -e

echo "=========================================="
echo "E2E Backend Startup Script"
echo "=========================================="
echo "Current directory: $(pwd)"
echo "Timestamp: $(date)"

# Navigate to backend directory
cd ../nova-webgames-be
echo "Changed to backend directory: $(pwd)"

# Activate venv if it exists, otherwise use system Python
if [ -f "venv/bin/activate" ]; then
    echo "✓ Found venv, activating..."
    source venv/bin/activate
    UVICORN=venv/bin/uvicorn
    echo "✓ Using venv uvicorn: $UVICORN"
else
    echo "⚠ No venv found, using system uvicorn"
    UVICORN=uvicorn
fi

# Check if uvicorn exists
if ! command -v $UVICORN &> /dev/null; then
    echo "✗ ERROR: uvicorn not found at $UVICORN"
    echo "Available Python: $(which python3)"
    echo "Python version: $(python3 --version)"
    exit 1
fi

# Check environment variables
echo "Environment variables:"
echo "  DATABASE_URL: ${DATABASE_URL:-not set}"
echo "  SECRET_KEY: ${SECRET_KEY:-not set}"

# Check if database file exists (for SQLite)
if [[ "${DATABASE_URL}" == sqlite* ]]; then
    DB_FILE=$(echo "$DATABASE_URL" | sed 's|sqlite:///\./||')
    if [ -f "$DB_FILE" ]; then
        echo "✓ Database file exists: $DB_FILE"
    else
        echo "⚠ Database file does not exist yet: $DB_FILE"
    fi
fi

# Start uvicorn server (bootstrap should already be done in CI)
# Suppress access logs to reduce noise in E2E test output
echo "=========================================="
echo "Starting uvicorn server..."
echo "Command: $UVICORN app.main:app --host 0.0.0.0 --port 8000 --no-access-log"
echo "=========================================="
exec $UVICORN app.main:app --host 0.0.0.0 --port 8000 --no-access-log

