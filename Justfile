# List available recipes
help:
    @just --list

# Download caifs + caifs-common into _vendor/
vendor *ARGS:
    ./scripts/vendor.sh {{ ARGS }}

# Build the Python package
build:
    uv build

# Publish the package to PyPI
publish:
    uv publish

# Run tests
test:
    uv run pytest

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Run pre-commit on all files
pre-commit-run:
    uv run pre-commit run --all-files

# Type check
type-check:
    uv run ty check .
