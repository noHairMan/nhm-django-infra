# We thank you for your help

[Simplified Chinese](/docs/README.zh.md)\|[English](/docs/README.en.md)\|[Japanese](/docs/README.ja.md)\|[Traditional Chinese](/docs/README.zh-TW.md)

![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FnoHairMan%2Fnhm-django-infra%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.requires-python&label=python)[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

A lightweight Django 5 + Django REST framework scaffolding for backend services, including the following features:

-   Health check interface: GET /api/health/
-   Unified API response structure (code/data/message) and global exception handling
-   SQLite is used by default; optional PostgreSQL configuration (reserved for psycopg connection pool example) and Redis example
-   Dynaconf-based environment variable configuration (supports .env)
-   Provide Gunicorn configuration and Docker examples
-   It is recommended to use uv for dependency management
-   Support OpenAPI 3 (customized AutoSchema, integrated PyYAML) to facilitate the generation and release of interface specifications
-   Provides permission examples and built-in FilterBackend (search/ordering) to support filtering and sorting
-   Provide a simple request/test tool (request_client) to facilitate joint debugging and automation

## Project structure (brief)

-   deployment/
    -   Dockerfile (based on python:3.13-slim, built-in uv + gunicorn)
    -   docker-compose.yaml (PostgreSQL service)
    -   gunicorn.py（wsgi_app=porsche.wsgi:application）
    -   postgres/ (initialization script and postgres.conf)
-   src/
    -   manage.py
    -   porsche/
        -   settings.py (Dynaconf enabled: APP name "porsche")
        -   urls.py (API path prefix /api/)
        -   api/endpoints/ (health check example)
        -   core/restframework (DRF packaging: Request/Response, exceptions, mixins, etc.)

## Environmental requirements

-   Python 3.13+
-   SQLite (default; works out of the box)
-   Optional: PostgreSQL 17+, Redis, Docker and Docker Compose
-   uv or pip

## Configuration (Dynaconf)

-   Environment variable prefix: PORSCHE\_
-   Support placing .env files in the project root directory

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

-   Default: DEBUG=false, ALLOWED_HOSTS=["*"], example SECRET_KEY - the production environment must be covered.
-   Dynaconf's nested keys use double underscores "**", for example PORSCHE_DATABASES**postgres\_\_HOST。
-   REST_FRAMEWORK uses QueryParameterVersioning (default version=1); the default URL prefix does not include version; the API version number can be obtained dynamically from settings.

## local quick start

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

Use pip:

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`Install dependencies later (it is more recommended to use uv)
3) Migration and startup are the same as above

Optional: Create a superuser

    uv run python src/manage.py createsuperuser

## Docker (native Postgres)

The repository provides a minimal docker-compose.yaml (containing only Postgres):

1) Prepare .env in the project root directory (containing at least):

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) Start:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres is mapped to port 5432 of the host; data/configuration is mounted under deployment/postgres.

Note: This compose will not start the Django application; you can start it locally with uv/pip, or extend compose by yourself to add application services.

-   Health check: The image health check path has been pointed to`/api/health/`, which can be used for liveness/readiness of container orchestration.

## Build application image (optional)

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

illustrate:

-   Build-time dependencies come from uv.lock and pyproject.toml.
-   The entrance is gunicorn.
-   To connect to Postgres in compose, make sure the network is reachable and the PORSCHE_DATABASES\_\_... environment variable is set correctly.

## API example

Health check:

-   path:`GET /api/health/`
-   Response (unified structure):

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

Add more interfaces under src/porsche/api/endpoints/ and aggregate them in src/porsche/urls.py.

### Filtering, sorting and permissions

-   Filter/Search: Supported`?search=关键字`
-   Sort: Support`?ordering=字段`or`?ordering=-created_at`
-   Permissions: DRF permission classes and custom permissions can be configured as needed, examples are at`porsche/core/restframework`

### OpenAPI 3 与 Schema

-   OpenAPI 3 has been adopted, AutoSchema has been customized and PyYAML has been integrated to facilitate exporting and publishing API specifications.
-   If you need to generate or expose interface specifications, you can extend the corresponding routes/commands in the project, refer to`porsche/core/restframework`

## Logs and exceptions

-   Log: Output to stdout (console handler), see settings.LOGGING for details
-   Exceptions: handled uniformly by porsche.core.restframework.views.exception_handler and return structured response (code/data/message)

## Testing and Coverage

Basic tests are located in src/porsche/tests/. Use Django's built-in test runner (no pytest required).

-   Pre-requisite: Install dependencies and activate virtual environment (uv recommended)
    -   `uv sync && source .venv/bin/activate`
    -   If the test requires DB, make sure Postgres is available, or start it through compose as follows

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

-   CI and coverage merging: Multi-Python version testing has been done in CI and coverage data has been merged. Badges and links at the top of the page point to the merged report for unified viewing.

Example: can be used in testing`PorscheAPITestCase`of`request_client`provided`RequestsClient`Perform external request simulation:

```python
from porsche.core.restframework.test import PorscheAPITestCase


class TestSomething(PorscheAPITestCase):
    def test_request(self):
        resp = self.request_client.get("http://localhost:8000/api/health/")
        self.assertEqual(resp.status_code, 200)
```

## Frequently Asked Questions (FAQ)

1) Database connection problem?

-   Confirm that Postgres is running and the credentials match (compose uses .env)
-   Check PORSCHE_DATABASES**postgres**HOST/PORT/USER/PASSWORD
-   Ensure network connectivity when running in a container environment

2) SECRET_KEY and DEBUG?

-   In the production environment, please set strong random PORSCHE_SECRET_KEY and set PORSCHE_DEBUG=false

3) Language/time zone?

-   Default: LANGUAGE_CODE=en-us, TIME_ZONE=UTC; can be overridden through Dynaconf (such as PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE)

## license

MIT License — see[LICENSE](../LICENSE)

## reference

-   Django:<https://docs.djangoproject.com/>
-   Django REST framework:<https://www.django-rest-framework.org/>
-   Dynaconf:<https://www.dynaconf.com/>
-   psycopg:<https://www.psycopg.org/>
-   uv:<https://docs.astral.sh/uv/>

## To-do
