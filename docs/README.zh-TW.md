# nhm-django-infra

[簡體中文](docs/README.zh.md)\|[英語](docs/README.en.md)\|[日本人](docs/README.ja.md)\|[繁體中文](docs/README.zh-TW.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

一個用於後端服務的輕量級 Django 5 + Django REST framework 腳手架，包含以下特性：

-   健康檢查接口：GET /api/health/
-   統一的 API 響應結構（code/data/message）與全局異常處理
-   默認使用 SQLite；可選 PostgreSQL 配置（預留 psycopg 連接池示例）和 Redis 示例
-   基於 Dynaconf 的環境變量配置（支持 .env）
-   提供 Gunicorn 配置與 Docker 示例
-   推薦使用 uv 進行依賴管理

## 項目結構（簡要）

-   部署/
    -   Dockerfile（基於 python:3.13-slim，內置 uv + gunicorn）
    -   docker-compose.yaml（PostgreSQL 服務）
    -   Gunicorn.py（wsgi_app=porsche.wsgi:application）
    -   postgres/（初始化腳本與 postgres.conf）
-   原始碼/
    -   manage.py
    -   保時捷/
        -   settings.py（已啟用 Dynaconf：APP 名稱 "porsche"）
        -   urls.py（API 路徑前綴 /api/）
        -   api/endpoints/（健康檢查示例）
        -   core/restframework（DRF 包裝：Request/Response、異常、mixins 等）

## 環境要求

-   Python 3.13+
-   SQLite（默認；開箱即用）
-   可選：PostgreSQL 17+、Redis、Docker 與 Docker Compose
-   uv 或 pip

## 配置（Dynaconf）

-   環境變量前綴：PORSCHE\_
-   支持在項目根目錄放置 .env 文件

示例 .env：

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

說明：

-   默認：DEBUG=false，ALLOWED_HOSTS=["*"]，示例 SECRET_KEY —— 生產環境務必覆蓋。
-   Dynaconf 的嵌套鍵使用雙下劃線 "**"，例如 PORSCHE_DATABASES**postgres\_\_HOST。
-   REST_FRAMEWORK 使用 QueryParameterVersioning（默認版本=1）；默認 URL 前綴不包含版本。

## 本地快速開始

使用 uv（推薦）：

1) 安裝 uv（<https://docs.astral.sh/uv/）>2) 在項目根目錄執行：

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) 數據庫：

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) 遷移並啟動：

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

使用 pip：

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`後安裝依賴（更推薦使用 uv）
3) 遷移和啟動同上

可選：創建超級用戶

    uv run python src/manage.py createsuperuser

## Docker（本地 Postgres）

倉庫提供了一個最小化的 docker-compose.yaml（僅包含 Postgres）：

1) 在項目根目錄準備 .env（至少包含）：

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) 啟動：

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres 映射到宿主機 5432 端口；數據/配置掛載在 deployment/postgres 下。

注意：該 compose 不會啟動 Django 應用；可在本地用 uv/pip 啟動，或自行擴展 compose 增加應用服務。

## 構建應用鏡像（可選）

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

說明：

-   構建時依賴來自 uv.lock 與 pyproject.toml。
-   入口為 gunicorn。
-   Dockerfile 的 HEALTHCHECK 指向 http&#x3A;//localhost:8000/api/v1/health。若你的應用使用 /api/health，請更新路徑或
    在 porsche/urls.py 中添加帶版本的前綴。
-   若要連接 compose 中的 Postgres，請確保網絡可達並正確設置 PORSCHE_DATABASES\_\_... 環境變量。

## API 示例

健康檢查：

-   路徑：`GET /api/health/`
-   響應（統一結構）：

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

-   捲曲：

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

在 src/porsche/api/endpoints/ 下添加更多接口，並在 src/porsche/urls.py 中進行聚合。

## 日誌與異常

-   日誌：輸出到 stdout（console handler），詳見 settings.LOGGING
-   異常：由 porsche.core.restframework.views.exception_handler 統一處理並返回結構化響應（code/data/message）

## 測試與覆蓋率

基礎測試位於 src/porsche/tests/。使用 Django 自帶測試運行器（無需 pytest）。

-   前置：安裝依賴並激活虛擬環境（推薦 uv）
    -   `uv sync && source .venv/bin/activate`
    -   如測試需要 DB，確保 Postgres 可用，或按下文通過 compose 啟動

-   運行全部測試：
    -   `uv run python src/manage.py test porsche`
    -   或`python src/manage.py test porsche`

-   運行指定包/模塊/用例：
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   覆蓋率：
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`（輸出到 htmlcov/）

## 常見問題（FAQ）

1) 數據庫連接問題？

-   確認 Postgres 正在運行，且憑據匹配（compose 使用 .env）
-   檢查 PORSCHE_DATABASES**postgres**主機/端口/用戶/密碼
-   在容器環境中運行時，確保網絡連通

2) SECRET_KEY 與 DEBUG？

-   生產環境請設置強隨機的 PORSCHE_SECRET_KEY，並設置 PORSCHE_DEBUG=false

3) 語言/時區？

-   默認：LANGUAGE_CODE=en-us，TIME_ZONE=UTC；可通過 Dynaconf 覆蓋（如 PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE）

## 許可證

MIT License — 見[執照](../LICENSE)

## 參考

-   姜戈：<https://docs.djangoproject.com/>
-   Django REST 框架：<https://www.django-rest-framework.org/>
-   動態會議：<https://www.dynaconf.com/>
-   心理諮詢：<https://www.psycopg.org/>
-   紫外線：<https://docs.astral.sh/uv/>

## 待辦
