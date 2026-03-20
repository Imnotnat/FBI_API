# FBI API"

Python client for the [FBI Wanted Persons public API](https://api.fbi.gov/).

## Installation

```bash
pip install -e ".[dev]"   # editable install with dev dependencies
```

Or for use in another project:

```bash
pip install fbi-api
```

## Quick start

```python
from fbi_api import FBIClient

client = FBIClient()

# List the first page of wanted persons
results = client.search_wanted()
print(f"Total wanted: {results.total}")
for person in results.items:
    print(person.title, "-", person.url)

# Filter by subject and field office
results = client.search_wanted(subject="terrorism", field_office="miami", page=1, page_size=10)

# Retrieve a single person by UID
person = client.get_person("7db4d4428c2045b6b04bf3e6af2be1ea")
print(person.title)
print(person.caution)
```

## API reference

### `FBIClient(base_url, timeout, session)`

| Parameter  | Default                           | Description                          |
|------------|-----------------------------------|--------------------------------------|
| `base_url` | `https://api.fbi.gov/wanted/v1`   | Override the API base URL            |
| `timeout`  | `10`                              | HTTP request timeout in seconds      |
| `session`  | new `requests.Session`            | Reuse an existing session            |

#### `search_wanted(**kwargs) -> SearchResults`

| Parameter      | Type  | Description                                     |
|----------------|-------|-------------------------------------------------|
| `title`        | `str` | Filter by name / title                          |
| `field_office` | `str` | FBI field office slug (e.g. `"dallas"`)         |
| `subject`      | `str` | Subject category (e.g. `"terrorism"`)           |
| `status`       | `str` | Status code (e.g. `"na"` for active)            |
| `page`         | `int` | Page number, starting at 1 (default: `1`)       |
| `page_size`    | `int` | Results per page, max 50 (default: `20`)        |

#### `get_person(uid: str) -> WantedPerson`

Retrieve a single wanted person by their unique identifier.

### Models

#### `WantedPerson`

| Attribute       | Type            |
|-----------------|-----------------|
| `uid`           | `str`           |
| `title`         | `str`           |
| `description`   | `str \| None`   |
| `url`           | `str`           |
| `images`        | `list[str]`     |
| `subjects`      | `list[str]`     |
| `field_offices` | `list[str]`     |
| `reward_text`   | `str \| None`   |
| `details`       | `str \| None`   |
| `caution`       | `str \| None`   |
| `status`        | `str \| None`   |
| `nationality`   | `str \| None`   |
| `age_range`     | `str \| None`   |
| `hair`          | `str \| None`   |
| `eyes`          | `str \| None`   |
| `height_min`    | `int \| None`   |
| `height_max`    | `int \| None`   |
| `weight_min`    | `int \| None`   |
| `weight_max`    | `int \| None`   |

#### `SearchResults`

| Attribute | Type               |
|-----------|--------------------|
| `total`   | `int`              |
| `items`   | `list[WantedPerson]` |
| `page`    | `int`              |

### Exceptions

| Exception                 | Raised when                              |
|---------------------------|------------------------------------------|
| `FBIAPIError`             | Base class for all library errors        |
| `FBIAPIConnectionError`   | Network/timeout error                    |
| `FBIAPIResponseError`     | Non-2xx HTTP response (has `.status_code`) |

## Project structure

```
fbi_api/
├── __init__.py       # Public API surface
├── client.py         # FBIClient class
├── models.py         # WantedPerson, SearchResults dataclasses
└── exceptions.py     # Custom exceptions
tests/
├── test_client.py    # Client tests (mocked HTTP)
└── test_models.py    # Model unit tests
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
