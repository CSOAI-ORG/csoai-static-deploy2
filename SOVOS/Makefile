# SOVOS Makefile
# One build. One test. One deploy.

.PHONY: help build test install clean lint deploy docker docker-push all

help:
	@echo "SOVOS — Governance OS for AI"
	@echo ""
	@echo "  make install      Install all SOVOS packages in editable mode"
	@echo "  make test         Run all tests (pytest)"
	@echo "  make lint         Run linters on all packages"
	@echo "  make build        Build all Docker images"
	@echo "  make deploy       Deploy the full stack (docker-compose)"
	@echo "  make clean        Remove build artifacts"
	@echo ""

install:
	pip install -e packages/sovos-core
	pip install -e packages/sovos-clans
	pip install -e packages/sovos-signal
	pip install -e packages/sovos-harness
	pip install -e packages/sovos-3kb
	pip install -e packages/sovos-c2pa
	pip install -e packages/sovos-error-mergekit
	pip install -e packages/sovos-mcp

test:
	PYTHONPATH=packages pytest packages/*/tests -v

lint:
	@for pkg in packages/*/; do \
		echo "Linting $$pkg"; \
		(cd $$pkg && python3 -m py_compile $$(find src -name "*.py" 2>/dev/null) || true); \
	done

build:
	docker compose build

deploy:
	docker compose up -d

docker:
	for pkg in packages/*/ mcp-servers/*/; do \
		if [ -f "$$pkg/Dockerfile" ]; then \
			echo "Building $$pkg"; \
			docker build -t "csoai/$$(basename $$pkg):latest" "$$pkg"; \
		fi \
	done

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true

all: install test