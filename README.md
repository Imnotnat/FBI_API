# FBI API

Python client for the [FBI Wanted Persons public API](https://api.fbi.gov/).

## Installation

```bash
pip install -e ".[dev]"   # editable install with dev dependencies
```

## Project structure

```
fbi_api/
├── __init__.py       # Public API surface
├── client.py         # FBIClient class  ← à compléter
├── models.py         # WantedPerson, SearchResults  ← à compléter
└── exceptions.py     # Custom exceptions  ← à compléter
tests/
├── test_client.py    # Client tests  ← à compléter
└── test_models.py    # Model unit tests  ← à compléter
pyproject.toml        # Project metadata & dependencies
```

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

