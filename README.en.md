# Nazidjnjfra

[Simplified Chinese]\|[English](docs/README.en.md)\|[Japanese](docs/README.ja.md)\|[French](docs/README.fr.md)\|[Español](docs/README.es.md)\|[Deutsch](docs/README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

A lightweight Django 5 + Django REST framework scaffolding for backend services, including the following features:

-   Health check interface: GET /api/health/
-   Unified API response structure (code/data/message) and global exception handling
-   SQLite is used by default; optional PostgreSQL configuration (reserve psycopg connection pool example) and Redis example
-   Dynaconf-based environment variable configuration (supports .env)
-   Provide Gunicorn configuration and Docker examples
-   It is recommended to use uv for dependency management

## Project Structure (Brief)

-   deployment/
    -   Dockerfile (based on python:3.13-slim, built-in uv + gunicorn)
    -   docker-compose.yaml (PostgreSQL service)
    -   gunicorn.py（wsgi_app=porsche.wsgi:application）
    -   postgres/ (initialize script with postgres.conf)
-   src/
    -   manage.py
    -   porsche/
        -   settings.py (Dynaconf: APP name "porsche" enabled)
        -   urls.py (API path prefix /api/)
        -   api/endpoints/ (Health Check Example)
        -   core/restframework (DRF packaging: Request/Response, exception, mixins, etc.)

## Environmental Requirements

-   Python 3.13+
-   SQLite (default; out of the box)
-   Optional: PostgreSQL 17+, Redis, Docker and Docker Compose
-   uv or pip

## Configuration (Dynaconf)

-   Environment variable prefix: PORSCHE\_
-   Supports placement of .env files in the project root directory

Example .env:

    # docker-compose 的 Postgres 示例
    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

    # Django / Dynaconf（PORSCHE_*）
    # 重要：生产环境请覆盖 SECRET_KEY
    PORSCHE_SECRET_KEY=your-secret-key
    PORSCHE_DEBUG=true

    # PostgreSQL 连接（若不设置则回退到 SQLite）
    PORSCHE_DATABASES__postgres__ENGINE=django.db.backends.postgresql
    PORSCHE_DATABASES__postgres__NAME=porsche
    PORSCHE_DATABASES__postgres__USER=postgres
    PORSCHE_DATABASES__postgres__PASSWORD=postgres
    PORSCHE_DATABASES__postgres__HOST=127.0.0.1
    PORSCHE_DATABASES__postgres__PORT=5432

    # 可选的连接池占位示例
    # PORSCHE_DATABASES__postgres__OPTIONS__pool__min_size=4
    # PORSCHE_DATABASES__postgres__OPTIONS__pool__max_size=20

    # 可选 Redis
    # PORSCHE_REDIS_HOST=127.0.0.1
    # PORSCHE_REDIS_PORT=6379
    # PORSCHE_REDIS_USER=default
    # PORSCHE_REDIS_PASSWORD=your-password

illustrate:

-   Default: DEBUG=false, ALLOWED_HOSTS=["*"], example SECRET_KEY — The production environment must be covered.
-   Dynaconf's nested keys use double underscores "**", e.g. PORSCHE_DATABASES**postgres\_\_HOST。
-   REST_FRAMEWORK Use QueryParameterVersioning (default version=1); the default URL prefix does not contain the version.

## Quick start local

Use uv (recommended):

1) Install uv(<https://docs.astral.sh/uv/）>2) Execute in the project root directory:

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) Database:

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) Migrate and start:

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

Using pip:

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`Post-install dependencies (UV is more recommended)
3) Migration and startup are the same as above

Optional: Create a super user

    uv run python src/manage.py createsuperuser

## Docker (local Postgres)

The repository provides a minimized docker-compose.yaml (including Postgres only):

1) Prepare .env in the project root directory (at least):

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) Start:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres is mapped to host port 5432; data/configuration is mounted under deployment/postgres.

Note: This compose will not start the Django application; you can start it locally with uv/pip, or expand the compose to increase the application service by yourself.

## Build an application image (optional)

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

illustrate:

-   Build-time dependencies come from uv.lock with pyproject.toml.
-   The entrance is gunicorn.
-   The HEALTHCHECK of the Dockerfile points to http&#x3A;//localhost:8000/api/v1/health. If your application uses /api/health, please update the path or
    Add a versioned prefix in pornche/urls.py.
-   To connect to Postgres in compose, make sure the network is accessible and the PORSCHE_DATABASES\_\_... environment variable is set correctly.

## API Example

Health Check:

-   path:`GET /api/health/`
-   Response (Unified Structure):

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

-   Curl：

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

Add more interfaces under src/porsche/api/endpoints/ and aggregate in src/porsche/urls.py.

## Logs and exceptions

-   Log: Output to stdout (console handler), see settings.LOGGING for details
-   Exception: uniformly handled by pornsche.core.restframework.views.exception_handler and returns a structured response (code/data/message)

## Testing and coverage

The basic test is located in src/porsche/tests/. Use Django's own test runner (no pytest required).

-   Prerequisite: Install dependencies and activate the virtual environment (recommended uv)
    -   `uv sync && source .venv/bin/activate`
    -   If the test requires DB, make sure Postgres is available, or start with compose as follows

-   Run all tests:
    -   `uv run python src/manage.py test porsche`
    -   or`python src/manage.py test porsche`

-   Run the specified package/module/use case:
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   Coverage:
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`(Output to htmlcov/)

## FAQ

1) Database connection problem?

-   Confirm that Postgres is running and the credentials match (compose uses .env)
-   Check PORSCHE_DATABASES**postgres**HOST/PORT/USER/PASSWORD
-   Ensure network connectivity while running in container environment

2) SECRET_KEY and DEBUG?

-   Please set strong random PORSCHE_SECRET_KEY in the production environment and set PORSCHE_DEBUG=false

3) Language/time zone?

-   Default: LANGUAGE_CODE=en-us, TIME_ZONE=UTC; can be overwritten by Dynaconf (such as PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE)

## license

MIT License — See[LICENSE](../LICENSE)

## reference

-   Django:<https://docs.djangoproject.com/>
-   Django REST framework:<https://www.django-rest-framework.org/>
-   Dynaconf:<https://www.dynaconf.com/>
-   psycopg:<https://www.psycopg.org/>
-   uv:<https://docs.astral.sh/uv/>

## To be done
