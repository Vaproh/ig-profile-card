#!/bin/bash
set -e

source .venv/bin/activate

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

PORT=${PORT:-8080}
HOST=${HOST:-0.0.0.0}

if [ "$PROXY_ENABLED" = "true" ] && [ -n "$PROXY_SERVER" ]; then
    export PROXY_SERVER
    export PROXY_PORT
    export PROXY_USERNAME
    export PROXY_PASSWORD
    echo "Starting with proxy: $PROXY_SERVER"
fi

echo "Starting Instagram Profile Card Service on $HOST:$PORT..."
uvicorn main:app --host "$HOST" --port "$PORT" --reload