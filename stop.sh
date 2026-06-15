#!/bin/bash
set -e

SESSION_NAME="ig-profile"

echo ""
echo "[*] Stopping Instagram Profile Card Service..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    tmux kill-session -t "$SESSION_NAME"
    echo "[+] Session '$SESSION_NAME' stopped"
else
    echo "[*] No active session found"
fi

echo ""
echo "[+] All services stopped"
echo ""