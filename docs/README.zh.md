# nhm-django-infra

[简体中文](docs/README.zh.md) | [English](docs/README.en.md) | [日本語](docs/README.ja.md) | [繁体中文](docs/README.zh-TW.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)
![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

一个用于后端服务的轻量级 Django 5 + Django REST framework 脚手架，包含以下特性：

- 健康检查接口：GET /api/health/
- 统一的 API 响应结构（code/data/message）与全局异常处理
- 默认使用 SQLite；可选 PostgreSQL 配置（预留 psycopg 连接池示例）和 Redis 示例
- 基于 Dynaconf 的环境变量配置（支持 .env）
- 提供 Gunicorn 配置与 Docker 示例
- 推荐使用 uv 进行依赖管理

## 项目结构（简要）

- deployment/
    - Dockerfile（基于 python:3.13-slim，内置 uv + gunicorn）
    - docker-compose.yaml（PostgreSQL 服务）
    - gunicorn.py（wsgi_app=porsche.wsgi:application）
    - postgres/（初始化脚本与 postgres.conf）
- src/
    - manage.py
    - porsche/
        - settings.py（已启用 Dynaconf：APP 名称 "porsche"）
        - urls.py（API 路径前缀 /api/）
        - api/endpoints/（健康检查示例）
        - core/restframework（DRF 包装：Request/Response、异常、mixins 等）

## 环境要求

- Python 3.13+
- SQLite（默认；开箱即用）
- 可选：PostgreSQL 17+、Redis、Docker 与 Docker Compose
- uv 或 pip

## 配置（Dynaconf）

- 环境变量前缀：PORSCHE_
- 支持在项目根目录放置 .env 文件

示例 .env：

```
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
```

说明：

- 默认：DEBUG=false，ALLOWED_HOSTS=["*" ]，示例 SECRET_KEY —— 生产环境务必覆盖。
- Dynaconf 的嵌套键使用双下划线 "__"，例如 PORSCHE_DATABASES__postgres__HOST。
- REST_FRAMEWORK 使用 QueryParameterVersioning（默认版本=1）；默认 URL 前缀不包含版本。

## 本地快速开始

使用 uv（推荐）：

1) 安装 uv（https://docs.astral.sh/uv/）
2) 在项目根目录执行：
    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）
3) 数据库：
    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）
4) 迁移并启动：
    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

使用 pip：

1) `python -m venv .venv && source .venv/bin/activate`
2) `pip install -U pip` 后安装依赖（更推荐使用 uv）
3) 迁移和启动同上

可选：创建超级用户

```
uv run python src/manage.py createsuperuser
```

## Docker（本地 Postgres）

仓库提供了一个最小化的 docker-compose.yaml（仅包含 Postgres）：

1) 在项目根目录准备 .env（至少包含）：

```
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8
```

2) 启动：

```
docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build
```

3) Postgres 映射到宿主机 5432 端口；数据/配置挂载在 deployment/postgres 下。

注意：该 compose 不会启动 Django 应用；可在本地用 uv/pip 启动，或自行扩展 compose 增加应用服务。

## 构建应用镜像（可选）

```
# 在项目根目录（Docker 24+）执行
docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

# 运行示例
docker run --rm -p 8000:8000 \
  --env-file .env \
  nhm-django-infra:latest
```

说明：

- 构建时依赖来自 uv.lock 与 pyproject.toml。
- 入口为 gunicorn。
- Dockerfile 的 HEALTHCHECK 指向 http://localhost:8000/api/v1/health。若你的应用使用 /api/health，请更新路径或
  在 porsche/urls.py 中添加带版本的前缀。
- 若要连接 compose 中的 Postgres，请确保网络可达并正确设置 PORSCHE_DATABASES__... 环境变量。

## API 示例

健康检查：

- 路径：`GET /api/health/`
- 响应（统一结构）：

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

- Curl：

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

在 src/porsche/api/endpoints/ 下添加更多接口，并在 src/porsche/urls.py 中进行聚合。

## 日志与异常

- 日志：输出到 stdout（console handler），详见 settings.LOGGING
- 异常：由 porsche.core.restframework.views.exception_handler 统一处理并返回结构化响应（code/data/message）

## 测试与覆盖率

基础测试位于 src/porsche/tests/。使用 Django 自带测试运行器（无需 pytest）。

- 前置：安装依赖并激活虚拟环境（推荐 uv）
    - `uv sync && source .venv/bin/activate`
    - 如测试需要 DB，确保 Postgres 可用，或按下文通过 compose 启动

- 运行全部测试：
    - `uv run python src/manage.py test porsche`
    - 或 `python src/manage.py test porsche`

- 运行指定包/模块/用例：
    - `uv run python src/manage.py test porsche.tests.core`
    - `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    - `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

- 覆盖率：
    - `uv run coverage run src/manage.py test porsche`
    - `uv run coverage report`
    - `uv run coverage html`（输出到 htmlcov/）

## 常见问题（FAQ）

1) 数据库连接问题？

- 确认 Postgres 正在运行，且凭据匹配（compose 使用 .env）
- 检查 PORSCHE_DATABASES__postgres__HOST/PORT/USER/PASSWORD
- 在容器环境中运行时，确保网络连通

2) SECRET_KEY 与 DEBUG？

- 生产环境请设置强随机的 PORSCHE_SECRET_KEY，并设置 PORSCHE_DEBUG=false

3) 语言/时区？

- 默认：LANGUAGE_CODE=en-us，TIME_ZONE=UTC；可通过 Dynaconf 覆盖（如 PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE）

## 许可证

MIT License — 见 [LICENSE](../LICENSE)

## 参考

- Django: https://docs.djangoproject.com/
- Django REST framework: https://www.django-rest-framework.org/
- Dynaconf: https://www.dynaconf.com/
- psycopg: https://www.psycopg.org/
- uv: https://docs.astral.sh/uv/

## 待办
