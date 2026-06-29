#!/usr/bin/env bash
# shellcheck disable=SC2068
# (chmod +x handled at install time by `chmod +x start.sh healthcheck.sh`)
# =====================================================================
# MEOK SOV3 Backend — start.sh
# Boots the sovereign-mcp-server (FastAPI + uvicorn) under gunicorn
# on the canonical port 3101. Mirrors the launchd-managed prod config
# described in ~/clawd/AGENTS.md §1.
# =====================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${MEOK_PORT:-3101}"
WORKERS="${MEOK_WORKERS:-2}"
HOST="${MEOK_HOST:-0.0.0.0}"
APP_MODULE="${MEOK_APP:-sovereign_mcp_server:app}"

# ---- Pretty banner --------------------------------------------------------
cat <<'BANNER'
╔══════════════════════════════════════════════════════════════════╗
║   🜏  MEOK SOV3 SOVEREIGN COMPOSITE                              ║
║   Booting sovereign-mcp-server on :3101                         ║
╚══════════════════════════════════════════════════════════════════╝
BANNER

# ---- Sanity checks --------------------------------------------------------
command -v python3 >/dev/null      || { echo "❌ python3 missing"; exit 1; }
command -v gunicorn >/dev/null      || {
    echo "⚙️  gunicorn not installed; installing..."
    python3 -m pip install --user --quiet gunicorn==21.2.0 uvicorn==0.29.0
}

# Make sure the server module is importable
python3 -c "import ${APP_MODULE%%:*}" 2>/dev/null || {
    echo "⚠️  Could not import ${APP_MODULE}. Falling back to discovery..."
    if [ -f "sovereign_mcp_server.py" ]; then
        APP_MODULE="sovereign_mcp_server:app"
    elif [ -f "server.py" ]; then
        APP_MODULE="server:app"
    else
        echo "❌ No entry-point module found (need sovereign_mcp_server.py or server.py)"
        exit 1
    fi
}

# ---- Pre-flight: ensure no stale process is bound ----------------------
if lsof -ti tcp:"$PORT" >/dev/null 2>&1; then
    echo "⚠️  Port $PORT already in use:"
    lsof -i tcp:"$PORT" || true
    if [ "${MEOK_FORCE_RESTART:-0}" = "1" ]; then
        echo "🔪 MEOK_FORCE_RESTART=1 — killing stale process"
        lsof -ti tcp:"$PORT" | xargs -r kill -9 || true
        sleep 1
    else
        echo "❌ Refusing to start. Set MEOK_FORCE_RESTART=1 to override."
        exit 2
    fi
fi

# ---- Launch under gunicorn (2 uvicorn workers) -------------------------
echo "🚀  gunicorn ${APP_MODULE} --bind ${HOST}:${PORT} --workers ${WORKERS}"
echo "🔍  Logs: stdout (use '| tee sov3.log' to persist)"
echo "❤️   Healthcheck: POST http://127.0.0.1:${PORT}/mcp"
echo

exec gunicorn "$APP_MODULE" \
    --bind "${HOST}:${PORT}" \
    --workers "${WORKERS}" \
    --worker-class "uvicorn.workers.UvicornWorker" \
    --timeout 120 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    "$@"
