# pyserp-api

[![Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fgithub.com%2Fwhode%2Fpyserp-api%2Fraw%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=project.version&label=version)](https://github.com/whode/pyserp-api/blob/main/pyproject.toml)
[![Workflow Status](https://img.shields.io/github/actions/workflow/status/whode/pyserp-api/ci.yml?branch=main)](https://github.com/whode/pyserp-api/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/whode/pyserp-api)](LICENSE)

Async REST API wrapper around the `pyserp` library.

## Features

- Async FastAPI service with typed request/response models.
- Provider-specific endpoints for Google and Bing.
- Docker-ready (Gunicorn + Uvicorn workers).
- Environment-based configuration.

## Design / Decisions

- Async + FastAPI: the workload is I/O-bound (network calls), so async improves throughput.
- Managers are built via a factory to centralize config (proxies, SSL, limits) and keep a single change point.
- Concurrency is capped via `PYSERP_SEMAPHORE_LIMIT` to reduce rate-limit/ban risks.
- Default headers/cookies/proxies live in env for consistent behavior across requests.

## Requirements

- Python 3.10+

## Quick start

### Local

1) Create and activate a virtual environment:

```bash
# Windows (PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -e .
```

3) Create a local env file:

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

4) Run the service:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

Before the first run, create `.env` from `.env.example`:

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

```bash
docker compose up --build
```

## Configuration

All configuration is via environment variables. See `.env.example` for the full list.

Common settings:

- `PYSERP_ENV`: environment name (e.g. `development`, `production`).
- `PYSERP_LOG_LEVEL`: log level (`INFO`, `DEBUG`).
- `PYSERP_SEMAPHORE_LIMIT`: max concurrent requests.
- `PYSERP_PROXIES`: JSON array of proxies (e.g. `["http://user:pass@host:port"]`).
- `PYSERP_GOOGLE_HEADERS`, `PYSERP_GOOGLE_COOKIES`: JSON objects for defaults.

## API

Interactive docs:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

Health:
- `GET /health`
- `GET /version`

Search endpoints:
- `POST /google/search-one`
- `POST /google/search-many`
- `POST /google/search-top`
- `POST /bing/search-one`
- `POST /bing/search-many`
- `POST /bing/search-top`

### Request shapes

`search-one`:

```json
{
  "query": "how to learn python",
  "start": 0,
  "params": {"num": 10},
  "headers": {"User-Agent": "..."},
  "cookies": {"NID": "..."},
  "proxy": "http://user:pass@host:port",
  "tries": 3
}
```

`search-many`:

```json
{
  "query": "how to learn python",
  "starts": [0, 10, 20],
  "in_order": true
}
```

`search-top`:

```json
{
  "query": "how to learn python",
  "limit": 20,
  "in_order": true,
  "pages_per_time_default": 2,
  "ignore_page_errors": false,
  "include_page_errors": true
}
```

### Example

```bash
curl -X POST "http://localhost:8000/google/search-one" \
  -H "Content-Type: application/json" \
  -d '{"query": "how to learn python"}'
```

Example response (Google):

```json
{
  "results": {
    "organic": [
      {
        "url": "https://example.com",
        "title": "Example",
        "site_name": "Example Site",
        "snippet": "Stubbed result"
      }
    ]
  },
  "has_more": false
}
```

`search-many` and `search-top` return a list wrapper:

```json
{
  "pages": [
    {
      "results": {"organic": []},
      "has_more": false
    }
  ]
}
```

Notes:
- Errors from the underlying library are returned as `ErrorModel` objects.
- The API passes through `pyserp` models without reshaping.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

Licensed under the MIT License. See `LICENSE` for details.
