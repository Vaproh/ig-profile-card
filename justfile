set dotenv-load := true

default: help

@help:
    @just --list

# Install dependencies with uv
install:
    uv sync

# Sync dependencies (install + update lock file)
sync:
    uv sync

# Update dependencies
update:
    uv update

# Run the service
run:
    uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Start in tmux session
start:
    ./start.sh

# Stop the service
stop:
    ./stop.sh

# Clean cache and build artifacts
clean:
    rm -rf __pycache__/ */__pycache__/ */*/__pycache__/
    rm -rf .pytest_cache/ .coverage htmlcov/
    rm -rf dist/ build/ *.egg-info/ .eggs/
    rm -rf .venv/
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*~$" -delete
    echo "Cleaned cache and build artifacts"

# Format code with ruff
fmt:
    uv run ruff format .

# Format code with ruff (check only)
fmt-check:
    uv run ruff format --check .

# Lint with ruff
lint:
    uv run ruff check .

# Lint and format with ruff
check: fmt-check lint
    echo "All checks passed"

# Run tests
test:
    uv run pytest

# Shell into uv environment
shell:
    uv run python
