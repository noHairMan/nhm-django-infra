# nhm-django-infra

一个基于 Django 5 与 Django REST framework 的后端基础设施模板，内置：

- 健康检查接口（/api/v1/health）
- PostgreSQL（使用 psycopg 连接池）
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
        - urls.py：API 路由聚合（前缀 /api/v1/）
        - api/endpoints/
            - urls.py：注册 "health/" 路径
            - health.py：健康检查 API（返回 {"status": "ok"}）
        - core/restframework：对 DRF 的基本封装（mixins、generics、viewsets 等）

## 运行要求

- Python 3.13+
- PostgreSQL 17（或兼容版本）
- uv（推荐）或 pip
- 可选：Docker 与 Docker Compose（仅用于本地数据库或容器化部署）

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
# 数据库连接（psycopg，PostgreSQL）
PORSCHE_DATABASES__default__ENGINE=django.db.backends.postgresql
PORSCHE_DATABASES__default__NAME=porsche
PORSCHE_DATABASES__default__USER=postgres
PORSCHE_DATABASES__default__PASSWORD=postgres
PORSCHE_DATABASES__default__HOST=127.0.0.1
PORSCHE_DATABASES__default__PORT=5432
# 连接池设置（可选，与 settings.py 中 OPTIONS.pool 对应）
# PORSCHE_DATABASES__default__OPTIONS__pool__min_size=4
# PORSCHE_DATABASES__default__OPTIONS__pool__max_size=20
```

说明：

- settings.py 中默认 DEBUG=False、ALLOWED_HOSTS=["*"], SECRET_KEY 为示例值，强烈建议通过环境变量在生产环境覆盖。
- Dynaconf 的嵌套键使用双下划线 "__" 分隔：PORSCHE_DATABASES__default__HOST。

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
    - `uv run python src/manage.py runserver 0.0.0.0:8000`

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

在 deployment 目录下提供了 docker-compose.yaml，仅包含 Postgres 服务，用于本地数据库：

操作步骤：

1. 准备 .env（位于项目根目录），至少包含：

```
POSTGRES_DB=porsche
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8
```

2. 切换到 deployment 目录并启动：

```
cd deployment
docker compose up -d
```

3. 数据库将映射到本机 5432 端口，数据与配置通过卷挂载到当前 deployment/postgres 目录。

注意：应用（Django）并未在 compose 中启动。你可以在本机通过 uv/pip 启动 Django，或自行扩展 compose 加入应用服务。

## 构建应用镜像与运行（可选）

deployment/Dockerfile 提供了应用镜像构建示例：

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
- 容器入口为 gunicorn，健康检查路径为 http://localhost:8000/api/v1/health（见 Dockerfile HEALTHCHECK）。
- 若需要连接 compose 中的 Postgres，请保证容器网络可达并提供正确的 PORSCHE_DATABASES__... 环境变量。

## API 示例

- 健康检查：
    - 路径：`GET /api/v1/health/`
    - 返回：`{"status": "ok"}`
    - 示例：
      ```bash
      curl -s http://127.0.0.1:8000/api/v1/health/
      ```

后续可在 src/porsche/api/endpoints/ 下新增路由与视图，并在 src/porsche/urls.py 进行聚合。

## 日志

- 统一使用标准输出（console handler），格式见 settings.LOGGING。
- 通过环境变量可调整 LOG_LEVEL（若在 Dynaconf 中暴露）。

## 常见问题（FAQ）

1) 连接数据库失败？

- 确认 Postgres 已启动且账号密码正确（compose 版本在 deployment/.env 或项目根 .env）
- 检查 PORSCHE_DATABASES__default__HOST/PORT/USER/PASSWORD 是否设置
- 在容器中运行时，需要确保网络联通（同一 docker network 或正确的主机地址）

2) SECRET_KEY 与 DEBUG 如何设置？

- 生产环境务必设置强随机的 PORSCHE_SECRET_KEY，并将 PORSCHE_DEBUG 设为 false

3) 时区与语言设置？

- 默认 LANGUAGE_CODE=en-us，TIME_ZONE=UTC，可按需通过 Dynaconf 覆盖（如 PORSCHE_LANGUAGE_CODE/PORSCHE_TIME_ZONE）

## 许可

当前仓库未声明许可证。如需开源发布，请补充 LICENSE 文件并在此处注明。

## 参考

- Django: https://docs.djangoproject.com/
- Django REST framework: https://www.django-rest-framework.org/
- Dynaconf: https://www.dynaconf.com/
- psycopg: https://www.psycopg.org/
- uv: https://docs.astral.sh/uv/
