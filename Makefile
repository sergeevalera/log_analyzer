check-poetry:
	@if ! command -v poetry &> /dev/null; then \
        echo "Poetry not installed. Install poetry 1.5.1 before continuing."; \
        exit 1; \
    fi

install: check-poetry
	@echo "Installing dependencies..."
	poetry install

install-test:
	@echo "Installing test dependencies..."
	poetry install --no-root --only test

lint:
	@echo "Running linters..."
	poetry run black --check .
	poetry run isort --check-only --diff .
	poetry run flake8 .
	poetry run mypy .

# Запуск тестов
test: install-test
	@echo "Running tests..."
	pytest

run: install
	@echo "Running application..."
	poetry run analyzer

clean:
	@echo "Cleaning..."
	rm -rf .venv
	rm -rf build/*
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -f .coverage

reinstall: clean install

.PHONY: install install-test lint test run clean reinstall
