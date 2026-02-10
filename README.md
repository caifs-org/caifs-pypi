# caifs v0.1.0

Python wrapper for the [CAIFS](https://github.com/caifs-org/caifs) cross-platform installer framework.

## Install

```bash
uv tool install caifs
```

## Usage

```bash
caifs status          # Show available targets
caifs add <target>    # Install a target
caifs rm <target>     # Remove a target
```

## Development

```bash
uv sync                  # Install dependencies
just vendor              # Download caifs + caifs-common into _vendor/
uv run caifs --version   # Verify it works
just test                # Run tests
just pre-commit-run      # Lint and format
```
