#!/usr/bin/env bash
echo "Starting FastAPI app..."
echo "PORT is: ${PORT}"

exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
