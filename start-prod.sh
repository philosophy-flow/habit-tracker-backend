#!/bin/bash
set -e

pip install -r requirements.txt
echo "Starting uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000