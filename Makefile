.PHONY: help install dev-install clean test lint format run list

help:
	@echo "Available commands:"
	@echo "  make install         - Install package"
	@echo "  make dev-install     - Install with dev dependencies"
	@echo "  make clean           - Remove generated files"
	@echo "  make test            - Run tests"
	@echo "  make lint            - Run linters"
	@echo "  make format          - Format code"
	@echo "  make list            - List all available SDKs and versions"
	@echo "  make run             - Generate docs for all SDKs (all versions)"
	@echo "  make run-js          - Generate docs for JavaScript (latest)"
	@echo "  make run-kotlin      - Generate docs for Kotlin (latest)"
	@echo "  make run-dart        - Generate docs for Dart (latest)"
	@echo "  make run-csharp      - Generate docs for C# (latest)"
	@echo "  make run-python      - Generate docs for Python (latest)"
	@echo "  make run-swift       - Generate docs for Swift (latest)"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

clean:
	rm -rf output/*/
	rm -rf src/*.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf build/
	rm -rf dist/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

test:
	pytest

lint:
	ruff check src/
	mypy src/ || true

format:
	black src/ tests/
	ruff check --fix src/ || true

list:
	supabase-llm-docs list-sdks

run:
	supabase-llm-docs generate --sdk all --version all

run-js:
	supabase-llm-docs generate --sdk javascript --version latest

run-kotlin:
	supabase-llm-docs generate --sdk kotlin --version latest

run-dart:
	supabase-llm-docs generate --sdk dart --version latest

run-csharp:
	supabase-llm-docs generate --sdk csharp --version latest

run-python:
	supabase-llm-docs generate --sdk python --version latest

run-swift:
	supabase-llm-docs generate --sdk swift --version latest
