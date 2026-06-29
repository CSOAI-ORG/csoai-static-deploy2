# =====================================================================
# MEOK Backend — SOV3 Sovereign Composite
# Multi-stage Docker build for the sovereign-mcp-server (FastAPI + uvicorn)
# Port: 3101
# Image base: python:3.11-slim (PEP 668 compliant, installs in venv)
# =====================================================================

# ---------- Stage 1: build dependencies in an isolated venv ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build tools for any wheels that need compiling
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create venv, install deps into it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn==21.2.0

# ---------- Stage 2: minimal runtime ----------
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="meok-sov3-backend" \
      org.opencontainers.image.description="MEOK SOV3 Sovereign Composite — MCP server on :3101" \
      org.opencontainers.image.source="https://github.com/CSOAI-ORG/clawd-workspace" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    MEOK_PORT=3101 \
    MEOK_WORKERS=2

WORKDIR /app

# Copy venv and app from builder
COPY --from=builder /opt/venv /opt/venv
COPY . /app

# Non-root user for runtime safety
RUN useradd --create-home --shell /bin/bash meok \
    && chown -R meok:meok /app
USER meok

EXPOSE 3101

# Healthcheck pings /mcp (POST — see AGENTS.md §3: NEVER GET /health)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request, sys; \
req = urllib.request.Request('http://127.0.0.1:3101/mcp', method='POST', \
data=b'{\"jsonrpc\":\"2.0\",\"method\":\"tools/list\",\"id\":1}', \
headers={'Content-Type':'application/json'}); \
sys.exit(0 if urllib.request.urlopen(req, timeout=3).status == 200 else 1)"

# Boot via gunicorn (matches launchd-managed prod: 2 uvicorn workers)
CMD ["gunicorn", "sovereign_mcp_server:app", \
     "--bind", "0.0.0.0:3101", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
