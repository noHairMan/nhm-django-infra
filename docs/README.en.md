# nhm-django-infra

[English] | [简体中文](README.zh.md) | [日本語](README.ja.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)
![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

A lightweight Django 5 + Django REST framework boilerplate for backend services. It includes:

- Health check endpoint: GET /api/health/
- Unified API response (code/data/message) and global exception handler
- SQLite by default; optional PostgreSQL config (psycopg pool placeholders) and Redis example
- Dynaconf-based settings via environment variables (.env supported)
- Gunicorn config and Docker examples
- Dependency management with uv (recommended)

## Project Layout (brief)

- deployment/
    - Dockerfile (python:3.13-slim with uv + gunicorn)
    - docker-compose.yaml (PostgreSQL service)
    - gunicorn.py (wsgi_app=porsche.wsgi:application)
    - postgres/ (init scripts and postgres.conf)
- src/
    - manage.py
    - porsche/
        - settings.py (Dynaconf enabled: APP name "porsche")
        - urls.py (API under /api/)
        - api/endpoints/ (health endpoint)
        - core/restframework (DRF wrappers: Request/Response, exceptions, mixins, etc.)

## Requirements

- Python 3.13+
- SQLite (default, no setup)
- Optional: PostgreSQL 17+, Redis, Docker & Docker Compose
- uv or pip

## Configuration (Dynaconf)

- Environment variable prefix: PORSCHE_
- .env at project root is supported

Example .env:

```
# For docker-compose Postgres
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

# Django / Dynaconf (PORSCHE_*)
# IMPORTANT: override SECRET_KEY in production
PORSCHE_SECRET_KEY=your-secret-key
PORSCHE_DEBUG=true

# PostgreSQL connection (defaults to SQLite if not set)
PORSCHE_DATABASES__postgres__ENGINE=django.db.backends.postgresql
PORSCHE_DATABASES__postgres__NAME=porsche
PORSCHE_DATABASES__postgres__USER=postgres
PORSCHE_DATABASES__postgres__PASSWORD=postgres
PORSCHE_DATABASES__postgres__HOST=127.0.0.1
PORSCHE_DATABASES__postgres__PORT=5432

# Optional connection pool placeholders
# PORSCHE_DATABASES__postgres__OPTIONS__pool__min_size=4
# PORSCHE_DATABASES__postgres__OPTIONS__pool__max_size=20

# Optional Redis
# PORSCHE_REDIS_HOST=127.0.0.1
# PORSCHE_REDIS_PORT=6379
# PORSCHE_REDIS_USER=default
# PORSCHE_REDIS_PASSWORD=your-password
```

Notes:

- Defaults: DEBUG=false, ALLOWED_HOSTS=["*"], sample SECRET_KEY — override in production.
- Dynaconf nested keys use "__" (double underscores), e.g. PORSCHE_DATABASES__postgres__HOST.
- REST_FRAMEWORK uses QueryParameterVersioning (default version=1); URL prefix does not include version by default.

## Quick Start (local)

Using uv (recommended):

1) Install uv (https://docs.astral.sh/uv/)
2) In project root:
    - Sync deps: `uv sync`
    - Activate venv: `source .venv/bin/activate` (or use `uv run`)
3) Database:
    - Use local Postgres (create DB porsche and set .env), or
    - Start Postgres via Docker Compose (see below)
4) Migrate & run:
    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - or `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

Using pip:

1) `python -m venv .venv && source .venv/bin/activate`
2) `pip install -U pip` and install dependencies (or prefer uv)
3) Run migrations and server as above

Optional: create superuser

```
uv run python src/manage.py createsuperuser
```

## Docker (local Postgres)

A minimal docker-compose.yaml is provided for Postgres only:

1) Prepare .env in project root (at least):

```
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8
```

2) Start:

```
docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build
```

3) Postgres is mapped to host port 5432; data/config mounted under deployment/postgres.

Note: The Django app is not started by compose; run it locally with uv/pip, or extend the compose to add the app
service.

## Build App Image (optional)

```
# From project root (Docker 24+)
docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

# Run example
docker run --rm -p 8000:8000 \
  --env-file .env \
  nhm-django-infra:latest
```

Notes:

- Dependencies are synced from uv.lock + pyproject.toml during build.
- Entry point is gunicorn.
- Dockerfile HEALTHCHECK points to http://localhost:8000/api/v1/health. If your app uses /api/health, update the path or
  add a versioned prefix in porsche/urls.py.
- To connect to compose Postgres, ensure network reachability and proper PORSCHE_DATABASES__... envs.

## API Example

Health check:

- Path: `GET /api/health/`
- Response (unified wrapper):

```json
{
  "code": 0,
  "data": {
    "app": "porsche",
    "version": "1.0.0"
  },
  "message": "SUCCESS"
}
```

- Curl:

```bash
curl -s http://127.0.0.1:8000/api/health/
# With QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

Add more endpoints under src/porsche/api/endpoints/ and aggregate in src/porsche/urls.py.

## Logging & Exceptions

- Logs: stdout (console handler), see settings.LOGGING
- Exceptions: handled by porsche.core.restframework.views.exception_handler returning unified structure (
  code/data/message)

## Tests & Coverage

Basic tests live in src/porsche/tests/. Use Django's test runner (pytest not required).

- Prereq: install deps and activate venv (uv recommended)
    - `uv sync && source .venv/bin/activate`
    - Ensure Postgres is available if tests need DB, or start it via compose below

- Run all tests:
    - `uv run python src/manage.py test porsche`
    - or `python src/manage.py test porsche`

- Run specific package/module/test:
    - `uv run python src/manage.py test porsche.tests.core`
    - `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    - `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

- Coverage:
    - `uv run coverage run src/manage.py test porsche`
    - `uv run coverage report`
    - `uv run coverage html` (outputs to htmlcov/)

## FAQ

1) Database connection issues?

- Ensure Postgres is running, and credentials match (.env for compose)
- Check PORSCHE_DATABASES__postgres__HOST/PORT/USER/PASSWORD
- When running in containers, ensure network connectivity

2) SECRET_KEY and DEBUG?

- In production set a strong PORSCHE_SECRET_KEY and set PORSCHE_DEBUG=false

3) Locale/Timezone?

- Defaults: LANGUAGE_CODE=en-us, TIME_ZONE=UTC; override via Dynaconf (e.g., PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE)

## License

MIT License — see [LICENSE](../LICENSE)

## References

- Django: https://docs.djangoproject.com/
- Django REST framework: https://www.django-rest-framework.org/
- Dynaconf: https://www.dynaconf.com/
- psycopg: https://www.psycopg.org/
- uv: https://docs.astral.sh/uv/

## Todo
