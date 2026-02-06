#!/usr/bin/env bash
set -e

echo "Starting FastAPI app..."
echo "PORT is: $PORT"

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
