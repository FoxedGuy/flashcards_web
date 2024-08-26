#!/usr/bin/env bash
TYPE=$1
PORT=$2
echo "Starting $TYPE on port $PORT"
sleep 1
python setup.py

if [ "$TYPE" = "dev" ]; then
    echo "Running in development mode"
    uvicorn src.start:app --reload --host 0.0.0.0 --port "$PORT"
fi

