.PHONY: help init install setup-db clean test lint format run-cli intake discover expose prioritize remove deindex monitor report archive

# Default target
help:
	@echo "Footprint Ops - Digital Privacy Remediation Toolkit"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install         - Install Python dependencies"
	@echo "  make setup-db        - Initialize database (migrations)"
	@echo "  make init            - Complete setup (install + db)"
	@echo ""
	@echo "Operational Workflows:"
	@echo "  make intake          - Run identity intake questionnaire (Phase 1)"
	@echo "  make discover        - Run full discovery sweep (Phase 2)"
	@echo "  make expose          - Generate exposure analysis (Phase 3)"
	@echo "  make prioritize      - Risk-rank exposures"
	@echo "  make remove          - Execute removal operations (Phase 4)"
	@echo "  make deindex         - Run search engine suppression (Phase 5)"
	@echo "  make monitor         - Start continuous monitoring (Phase 7)"
	@echo ""
	@echo "Reporting & Analysis:"
	@echo "  make report          - Generate full operational report"
	@echo "  make dashboard       - Start web dashboard"
	@echo "  make archive         - Create operational snapshot"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           - Remove generated files & logs"
	@echo "  make lint            - Run code linters"
	@echo "  make format          - Auto-format code"
	@echo "  make test            - Run test suite"
	@echo ""

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

setup-db:
	@echo "Initializing database..."
	python -m footprint_ops.db init
	@echo "Database initialized."

init: install setup-db
	@echo "✓ Footprint Ops fully initialized"
	@echo "Next: run 'make intake' to begin identity ingestion"

# Development
clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -f .coverage .pytest_cache
	@echo "✓ Cleaned"

lint:
	ruff check footprint_ops/
	mypy footprint_ops/ --ignore-missing-imports

format:
	black footprint_ops/ --line-length=100
	ruff check --fix footprint_ops/

test:
	pytest tests/ -v --cov=footprint_ops/

# Operational Workflows

intake:
	@echo "Starting identity intake (Phase 1)..."
	python footprint_ops/cli.py intake --interactive --mode full

discover:
	@echo "Starting discovery sweep (Phase 2)..."
	python footprint_ops/cli.py discover \
		--scope full \
		--engines google,bing,duckduckgo,archive \
		--targets osint,people-search,data-brokers,social \
		--parallel 4 \
		--progress

expose:
	@echo "Analyzing exposures (Phase 3)..."
	python footprint_ops/cli.py analyze exposures \
		--score-risk \
		--correlation \
		--timeline

prioritize:
	@echo "Prioritizing exposures by risk..."
	python footprint_ops/cli.py prioritize \
		--include-severity \
		--include-correlation-risk \
		--group-by category

remove:
	@echo "Removal operations (Phase 4)..."
	@echo "Running in DRY-RUN mode first for review..."
	python footprint_ops/cli.py removal \
		--dry-run \
		--review \
		--estimate-impact
	@echo ""
	@echo "To execute: python footprint_ops/cli.py removal --execute --confirm"

deindex:
	@echo "Search engine de-indexing (Phase 5)..."
	python footprint_ops/cli.py deindex \
		--targets google,bing,duckduckgo \
		--cache-removal \
		--snippet-suppression \
		--batch-size 10

monitor:
	@echo "Starting continuous monitoring (Phase 7)..."
	python footprint_ops/cli.py monitor \
		--frequency daily \
		--alerts \
		--diff-reports

# Reporting & Analysis
report:
	@echo "Generating full operational report..."
	python footprint_ops/cli.py report \
		--include identity-graph \
		--include exposure-summary \
		--include removal-status \
		--include search-visibility \
		--format html \
		--output reports/

dashboard:
	@echo "Starting web dashboard on http://localhost:8000"
	python footprint_ops/dashboard.py

archive:
	@echo "Creating operational snapshot..."
	python footprint_ops/cli.py archive \
		--include-data \
		--include-logs \
		--compress \
		--encrypt

# Quick starts
.PHONY: quickstart full-scan minimal-scan

quickstart:
	@echo "Quick start: identity intake + limited discovery"
	make intake
	@echo "Next: run 'make discover' for full discovery"

full-scan:
	@echo "Full operational scan..."
	make intake
	make discover
	make expose
	make report

minimal-scan:
	@echo "Minimal scan (name + email only)..."
	python footprint_ops/cli.py intake --mode minimal
	python footprint_ops/cli.py discover --targets search-engines --scope limited
