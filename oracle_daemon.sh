#!/bin/bash
# oracle_daemon.sh — Background daemon for Oracle SOV33 workspace
# Runs benchmarks, distillation, and training automatically
#
# Usage: bash oracle_daemon.sh start|stop|status

DAEMON_PIDFILE="/home/ubuntu/sov33_shared/daemon.pid"
DAEMON_LOG="/home/ubuntu/sov33_shared/daemon.log"
WORKSPACE="/home/ubuntu/sov33_shared"

start_daemon() {
    if [ -f "$DAEMON_PIDFILE" ] && kill -0 $(cat "$DAEMON_PIDFILE") 2>/dev/null; then
        echo "Daemon already running (PID $(cat $DAEMON_PIDFILE))"
        return 0
    fi

    echo "Starting SOV33 Oracle Daemon..."
    nohup bash -c '
        export $(cat /home/ubuntu/.env 2>/dev/null | xargs)
        cd /home/ubuntu/sov33_shared

        while true; do
            echo "$(date -u +%FT%TZ) daemon heartbeat" >> '"$DAEMON_LOG"'

            # 1. Check if Ollama is running
            if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
                echo "$(date -u +%FT%TZ) restarting ollama" >> '"$DAEMON_LOG"'
                ollama serve > /tmp/ollama.log 2>&1 &
                sleep 5
            fi

            # 2. Run API benchmarks if no recent results
            LATEST=$(ls -t benchmark-results/e2e_api_*.json 2>/dev/null | head -1)
            if [ -z "$LATEST" ] || [ $(find "$LATEST" -mmin +60 2>/dev/null | wc -l) -gt 0 ]; then
                echo "$(date -u +%FT%TZ) running api benchmark" >> '"$DAEMON_LOG"'
                python3 -u kaggle/sov33_e2e_orchestrator_v2.py --target api --provider groq --tasks 3 --workers 4 --out-prefix e2e_groq_auto 2>&1 | tail -5 >> '"$DAEMON_LOG"'
            fi

            # 3. Run distillation if training data is fresh
            if [ -f benchmark-results/training/self_train_data.jsonl ]; then
                echo "$(date -u +%FT%TZ) distillation data available" >> '"$DAEMON_LOG"'
            fi

            # 4. Sleep 5 minutes
            sleep 300
        done
    ' > /dev/null 2>&1 &
    echo $! > "$DAEMON_PIDFILE"
    echo "Daemon started (PID $(cat $DAEMON_PIDFILE))"
}

stop_daemon() {
    if [ -f "$DAEMON_PIDFILE" ]; then
        kill $(cat "$DAEMON_PIDFILE") 2>/dev/null
        rm -f "$DAEMON_PIDFILE"
        echo "Daemon stopped"
    else
        echo "No daemon running"
    fi
}

status_daemon() {
    if [ -f "$DAEMON_PIDFILE" ] && kill -0 $(cat "$DAEMON_PIDFILE") 2>/dev/null; then
        echo "Daemon running (PID $(cat $DAEMON_PIDFILE))"
        echo "Log tail:"
        tail -5 "$DAEMON_LOG" 2>/dev/null
    else
        echo "Daemon not running"
    fi
    echo ""
    echo "Workspace:"
    df -h "$WORKSPACE" 2>/dev/null | head -2
    echo ""
    echo "Ollama:"
    curl -s http://localhost:11434/api/tags 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d.get(\"models\",[]))} models')" 2>/dev/null || echo "not running"
}

case "${1:-status}" in
    start) start_daemon ;;
    stop) stop_daemon ;;
    status) status_daemon ;;
    *) echo "Usage: $0 {start|stop|status}" ;;
esac