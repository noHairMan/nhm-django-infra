# nhm-django-infra

一个基于 Django 5 与 Django REST framework 的后端基础设施模板，内置：

- 健康检查接口（/api/health）
- 统一响应包装（code/data/message）与异常处理（全局异常处理器）
- PostgreSQL 配置（含 psycopg 连接池参数位）、可选 Redis 缓存示例
- Dynaconf 环境变量管理（支持 .env、本地覆盖）
- gunicorn 运行配置与 Docker 部署示例
- 使用 uv 进行依赖管理，已配置国内镜像

适合快速搭建后端服务或作为项目脚手架。

## 目录结构

- deployment/
    - Dockerfile：后端镜像构建（基于 python:3.13-slim、内置 uv、gunicorn）
    - docker-compose.yaml：PostgreSQL 服务（桥接网络 nhm-django-infra-network）
    - gunicorn.py：gunicorn 配置（wsgi_app=porsche.wsgi:application 等）
    - postgres/docker-entrypoint-initdb.d/init-db.sh：初始化数据库脚本
    - postgres/postgres.conf：Postgres 配置（供容器挂载）
- src/
    - manage.py
    - porsche/
        - settings.py：Django 配置，Dynaconf 扩展启用（envvar_prefix=APP="porsche"，load_dotenv=True）
        - urls.py：API 路由聚合（前缀 /api/）
        - api/endpoints/
            - urls.py：注册 "health/" 路径
            - health.py：健康检查 API（返回 APP 与 VERSION）
        - core/restframework：对 DRF 的封装（Request/Response 包装、异常处理、mixins、generics、viewsets 等）

## 运行要求

- Python 3.13+
- PostgreSQL 17（或兼容版本）
- uv（推荐）或 pip
- 可选：Docker 与 Docker Compose（用于本地数据库或容器化部署）

## 环境变量与配置

本项目通过 Dynaconf 读取配置：

- APP 名称为 "porsche"，因此环境变量前缀为 PORSCHE_
- 支持 .env 文件（位于项目根目录），也可直接通过系统环境变量注入

常用配置项（示例 .env 片段）：

```
# 数据库（供 docker-compose 的 Postgres 使用）
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

# Django / Dynaconf（前缀 PORSCHE_）
# 注意：settings.py 默认 SECRET_KEY 为示例值，生产环境请务必覆盖！
PORSCHE_SECRET_KEY=your-secret-key
PORSCHE_DEBUG=true

# 数据库连接（PostgreSQL，已将 postgres 配置映射为 default）
# 你可以覆盖 postgres 或 default 命名空间中的键，以下二选一：
# 方式1：覆盖 postgres 命名空间（推荐）
PORSCHE_DATABASES__postgres__ENGINE=django.db.backends.postgresql
PORSCHE_DATABASES__postgres__NAME=porsche
PORSCHE_DATABASES__postgres__USER=postgres
PORSCHE_DATABASES__postgres__PASSWORD=postgres
PORSCHE_DATABASES__postgres__HOST=127.0.0.1
PORSCHE_DATABASES__postgres__PORT=5432
# 方式2：覆盖 default 命名空间（同样生效）
# PORSCHE_DATABASES__default__ENGINE=django.db.backends.postgresql
# PORSCHE_DATABASES__default__NAME=porsche
# PORSCHE_DATABASES__default__USER=postgres
# PORSCHE_DATABASES__default__PASSWORD=postgres
# PORSCHE_DATABASES__default__HOST=127.0.0.1
# PORSCHE_DATABASES__default__PORT=5432

# 连接池设置（可选，与 settings.py 中 OPTIONS.pool 对应）
# PORSCHE_DATABASES__postgres__OPTIONS__pool__min_size=4
# PORSCHE_DATABASES__postgres__OPTIONS__pool__max_size=20

# Redis（可选，用于 CACHES[redis] / CACHES[django_redis]）
# PORSCHE_REDIS_HOST=127.0.0.1
# PORSCHE_REDIS_PORT=6379
# PORSCHE_REDIS_USER=default
# PORSCHE_REDIS_PASSWORD=your-password
```

说明：

- settings.py 中默认 DEBUG=False、ALLOWED_HOSTS=["*"], SECRET_KEY 为示例值，强烈建议通过环境变量在生产环境覆盖。
- Dynaconf 的嵌套键使用双下划线 "__" 分隔，如：PORSCHE_DATABASES__postgres__HOST。
- REST_FRAMEWORK 使用 QueryParameterVersioning（默认 version=1），但当前 URL 前缀不包含版本号。

## 本地开发

方式 A：使用 uv（推荐）

1. 安装 uv（参考 https://docs.astral.sh/uv/）。
2. 在项目根目录执行：
    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或使用 `uv run` 执行命令）
3. 数据库：
    - 若已安装本地 Postgres，请创建数据库 porsche 并配置 .env；或
    - 使用下文 Docker 启动一个本地 Postgres。
4. 执行迁移并启动服务：
    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000` 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

方式 B：使用 pip

1. 建立虚拟环境并安装依赖：
    - `python -m venv .venv && source .venv/bin/activate`
    - `pip install -U pip && pip install -r <由 uv 导出的 requirements>（或改用 uv）`
2. 同上执行迁移与启动。

可选：创建超级用户（如后续扩展了认证模块）

```
uv run python src/manage.py createsuperuser
```

## 使用 Docker（本地 Postgres）

deployment 目录下提供了 docker-compose.yaml（仅包含 Postgres 服务），用于本地数据库：

1. 在项目根目录准备 .env（至少包含）：

```
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8
```

2. 启动：

```
docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build
```

3. 数据库映射到本机 5432 端口，数据与配置通过卷挂载到 deployment/postgres 目录。

注意：应用（Django）未在 compose 中启动。可本机通过 uv/pip 启动 Django，或扩展 compose 加入应用服务。

## 构建应用镜像与运行（可选）

deployment/Dockerfile 提供应用镜像构建示例：

```
# 在项目根目录执行（需要 Docker 24+）
docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

# 运行容器（示例）
docker run --rm -p 8000:8000 \
  --env-file .env \
  nhm-django-infra:latest
```

说明：

- 镜像在构建阶段通过 uv.lock 与 pyproject.toml 同步依赖。
- 容器入口为 gunicorn。
- Dockerfile 的 HEALTHCHECK 当前指向 http://localhost:8000/api/v1/health，如保持现有 URL 配置（/api/health），建议同步更新
  Dockerfile 的健康检查路径，或在 porsche/urls.py 中按需引入版本前缀。
- 若需要连接 compose 中的 Postgres，请保证容器网络可达并提供正确的 PORSCHE_DATABASES__... 环境变量。

## API 示例

- 健康检查：
    - 路径：`GET /api/health/`
    - 返回（统一响应包装）：
      ```json
      {
        "code": 0,
        "data": {"app": "porsche", "version": "1.0.0"},
        "message": "SUCCESS"
      }
      ```
    - 示例：
      ```bash
      curl -s http://127.0.0.1:8000/api/health/
      # 指定版本（QueryParameterVersioning）：
      curl -s "http://127.0.0.1:8000/api/health/?version=1"
      ```

后续可在 src/porsche/api/endpoints/ 下新增路由与视图，并在 src/porsche/urls.py 聚合。

## 日志与异常

- 日志：输出至标准输出（console handler），格式见 settings.LOGGING。
- 异常：统一使用 porsche.core.restframework.views.exception_handler 处理，返回统一响应结构（code/data/message）。

## 常见问题（FAQ）

1) 连接数据库失败？

- 确认 Postgres 已启动且账号密码正确（compose 版本使用项目根 .env）
- 检查 PORSCHE_DATABASES__postgres__HOST/PORT/USER/PASSWORD 是否设置
- 在容器中运行时，确保网络联通（同一 docker network 或正确的主机地址）

2) SECRET_KEY 与 DEBUG 如何设置？

- 生产环境务必设置强随机的 PORSCHE_SECRET_KEY，并将 PORSCHE_DEBUG 设为 false

3) 时区与语言设置？

- 默认 LANGUAGE_CODE=en-us，TIME_ZONE=UTC，可按需通过 Dynaconf 覆盖（如 PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE）

## 许可

当前仓库未声明许可证。如需开源发布，请补充 LICENSE 文件并在此处注明。

## 参考

- Django: https://docs.djangoproject.com/
- Django REST framework: https://www.django-rest-framework.org/
- Dynaconf: https://www.dynaconf.com/
- psycopg: https://www.psycopg.org/
- uv: https://docs.astral.sh/uv/
