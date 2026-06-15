#!/bin/bash
set -e

source .venv/bin/activate

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

PORT=${PORT:-8080}
HOST=${HOST:-0.0.0.0}

SESSION_NAME="ig-profile"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo ""
    echo "[*] Session '$SESSION_NAME' already exists. Killing..."
    tmux kill-session -t "$SESSION_NAME"
    echo "[+] Old session killed"
    echo ""
fi

echo ""
echo "[*] Starting Instagram Profile Card Service..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$PROXY_ENABLED" = "true" ] && [ -n "$PROXY_SERVER" ]; then
    echo "[*] Proxy: $PROXY_SERVER:$PROXY_PORT"
fi

tmux new-session -d -s "$SESSION_NAME" "uvicorn main:app --host $HOST --port $PORT --reload"

sleep 1

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "[+] Service running in tmux session '$SESSION_NAME'"
    echo ""
    echo "  Commands:"
    echo "    tmux attach -t $SESSION_NAME   - Attach to session"
    echo "    ./stop.sh                       - Stop service"
    echo ""
else
    echo "[!] Failed to start service"
    exit 1
fi