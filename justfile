# -*- mode: just -*-

# Test project
test:
    uv run pytest

# Check formatting with blue style
fmt:
    uv run pre-commit run --all

# Audit project dependencies
audit:
    uv tree
    uv pip compile pyproject.toml -o requirements.txt
    uvx pip-audit -r requirements.txt --fix

# Benchmark performance
# bench:
#     TODO
