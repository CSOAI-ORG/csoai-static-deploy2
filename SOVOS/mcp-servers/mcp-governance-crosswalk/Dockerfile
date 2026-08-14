FROM python:3.11-slim

WORKDIR /app

# Install the PyPI package (canonical source, not vendored)
RUN pip install --no-cache-dir csoai-governance-crosswalk-mcp

# Expose MCP server port
EXPOSE 3001

# Environment
ENV FRAMEWORKS=EU_AI_ACT,NIST_RMF,ISO_42001,DORA,GDPR,NIS2
ENV PORT=3001

CMD ["python3", "-m", "governance_crosswalk_mcp", "--port", "3001"]