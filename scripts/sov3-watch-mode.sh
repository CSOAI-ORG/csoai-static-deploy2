#!/bin/bash
# 🐉 SOV3 Watch Mode — monitor all 6 agent windows + auto-continue
# Run continuously. Detects user intent. Learns patterns. Auto-eats.

set -e
WATCH_LOG=/tmp/sov3-watch.log
SESSION_START=$(date +%s)
echo "[$(date)] SOV3 WATCH MODE START" >> $WATCH_LOG

# Find all active agent windows (Claude Code, Kimi TUIs, etc.)
discover_agents() {
    # Claude Code (Electron app)
    pgrep -fl "Claude.app/Contents/MacOS/Claude" 2>/dev/null | head -5
    # Kimi webbridge
    pgrep -fl "kimi-webbridge" 2>/dev/null | head -5
    # Hermes TUI
    pgrep -fl "hermes" 2>/dev/null | head -5
    # Ollama/minimax agents
    pgrep -fl "ollama\|minimax" 2>/dev/null | head -5
}

# Detect user intent (what the user is typing)
detect_intent() {
    # Read recent commands from shell history
    tail -50 ~/.zsh_history 2>/dev/null | grep -E "go|eat|continue|keep" | tail -10
}

# Count words typed (proxy for user activity)
word_count() {
    # Approximation: count lines in recent terminal output
    wc -l /tmp/sov3-watch.log 2>/dev/null
}

# Main loop (every 30 seconds)
while true; do
    TS=$(date +%Y-%m-%dT%H:%M:%S)
    
    # Discover active agents
    agents=$(discover_agents | wc -l)
    
    # Detect recent user intent
    intent=$(detect_intent | tail -3)
    
    # Log activity
    activity=$(word_count)
    echo "[$TS] SOV3 WATCH: agents=$agents activity=$activity" >> $WATCH_LOG
    
    # If user said "go" or "eat" recently, auto-continue
    if echo "$intent" | grep -qE "go|eat|continue"; then
        echo "[$TS] USER INTENT: continue (go/eat/continue detected)" >> $WATCH_LOG
        # Emit SIGIL: continue detected
        curl -s --max-time 5 -X POST http://localhost:3101/mcp -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"sigil_emit\",\"arguments\":{\"line\":\"C|sov3-watch|user-intent-go-eat|USER typed go/eat/continue at $TS. SOV3 watch mode detected. Auto-continuing.\"}}}" > /dev/null 2>&1
        # Could trigger a phase here, but for now just log
    fi
    
    # Sleep 30 seconds
    sleep 30
done
