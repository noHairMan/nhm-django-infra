# 我們感謝您的幫助

[簡體中文](/docs/README.zh.md)\|[英語](/docs/README.en.md)\|[日本人](/docs/README.ja.md)\|[繁體中文](/docs/README.zh-TW.md)

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/downloads/)![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noHairMan/nhm-django-infra/build.yml)[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

一個用於後端服務的輕量級 Django 5 + Django REST framework 腳手架，包含以下特性：

-   健康檢查介面：GET /api/health/
-   統一的 API 回應結構（code/data/message）與全域例外處理
-   預設使用 SQLite；可選 PostgreSQL 配置（預留 psycopg 連接池範例）和 Redis 範例
-   基於 Dynaconf 的環境變數配置（支援 .env）
-   提供 Gunicorn 配置與 Docker 範例
-   建議使用 uv 進行依賴管理
-   支援 OpenAPI 3（自訂 AutoSchema，整合 PyYAML），方便產生與發布介面規範
-   提供權限範例與內建 FilterBackend（search / ordering）以支援篩選與排序
-   提供簡潔的請求/測試工具（request_client），方便聯調與自動化

## 項目架構（簡要）

-   部署/
    -   Dockerfile（基於 python:3.13-slim，內建 uv + gunicorn）
    -   docker-compose.yaml（PostgreSQL 服務）
    -   Gunicorn.py（wsgi_app=porsche.wsgi:application）
    -   postgres/（初始化腳本與 postgres.conf）
-   原始碼/
    -   manage.py
    -   保時捷/
        -   settings.py（已啟用 Dynaconf：APP 名稱 "porsche"）
        -   urls.py（API 路徑前綴 /api/）
        -   api/endpoints/（健康檢查範例）
        -   core/restframework（DRF 包裝：Request/Response、異常、mixins 等）

## 環境要求

-   Python 3.12+
-   SQLite（預設；開箱即用）
-   選用：PostgreSQL 17+、Redis、Docker 與 Docker Compose
-   uv 或 pip

## 配置（Dynaconf）

-   環境變數前綴：PORSCHE\_
-   支援在專案根目錄放置 .env 文件

範例 .env：

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

-   預設：DEBUG=false，ALLOWED_HOSTS=["*"]，範例 SECRET_KEY —— 生產環境務必覆蓋。
-   Dynaconf 的嵌套鍵使用雙下劃線 "**"，例如 PORSCHE_DATABASES**postgres\_\_HOST。
-   REST_FRAMEWORK 使用 QueryParameterVersioning（預設版本=1）；預設 URL 前綴不包含版本；API 版本號可從 settings 動態取得。

## 本地快速開始

使用 uv（建議）：

1) 安裝 uv（<https://docs.astral.sh/uv/）>2) 在專案根目錄執行：

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) 資料庫：

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) 遷移並啟動：

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

使用 pip：

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`後安裝依賴（更建議使用 uv）
3) 遷移和啟動同上

可選：建立超級用戶

    uv run python src/manage.py createsuperuser

## Docker（本地 Postgres）

倉庫提供了一個最小化的 docker-compose.yaml（僅包含 Postgres）：

1) 在專案根目錄準備 .env（至少包含）：

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) 啟動：

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres 對應到宿主機 5432 連接埠；資料/配置掛載在 deployment/postgres 下。

注意：此 compose 不會啟動 Django 應用；可在本地用 uv/pip 啟動，或自行擴充 compose 增加應用程式服務。

-   健康檢查：鏡像健康檢查路徑已指向`/api/health/`，可用於容器編排的 liveness/readiness。

## 建構應用鏡像（可選）

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

說明：

-   建置時依賴來自 uv.lock 與 pyproject.toml。
-   入口為 gunicorn。
-   若要連接 compose 中的 Postgres，請確保網路可達並正確設定 PORSCHE_DATABASES\_\_... 環境變數。

## API 範例

健康檢查：

-   路徑：`GET /api/health/`
-   回應（統一結構）：

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

在 src/porsche/api/endpoints/ 下新增更多接口，並在 src/porsche/urls.py 中進行聚合。

### 過濾、排序與權限

-   過濾/搜尋：支持`?search=关键字`
-   排序：支持`?ordering=字段`或`?ordering=-created_at`
-   權限：可按需配置 DRF 權限類別與自訂權限，範例位於`porsche/core/restframework`

### OpenAPI 3 與架構

-   已採用 OpenAPI 3，自訂 AutoSchema 並整合 PyYAML，方便匯出與發布 API 規範
-   如需產生或暴露介面規範，可在專案中擴展對應路由/指令，參考`porsche/core/restframework`

## 日誌與異常

-   日誌：輸出到 stdout（console handler），詳見 settings.LOGGING
-   例外：由 porsche.core.restframework.views.exception_handler 統一處理並傳回結構化回應（code/data/message）

## 測試與覆蓋率

基礎測試位於 src/porsche/tests/。使用 Django 自帶測試運行器（無需 pytest）。

-   前置：安裝依賴並啟動虛擬環境（建議 uv）
    -   `uv sync && source .venv/bin/activate`
    -   如測試需要 DB，確保 Postgres 可用，或按文透過 compose 啟動

-   運行全部測試：
    -   `uv run python src/manage.py test porsche`
    -   或`python src/manage.py test porsche`

-   使用 tox 進行多版本本地測試：
    -   前置：`pip install tox`(配置已集成`tox-uv`)
    -   運行所有支援的版本 (py312, py313, py314)：`tox`
    -   運行指定版本：`tox -e py313`

-   運行指定包/模組/用例：
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   覆蓋率：
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`（輸出到 htmlcov/）

-   CI 與覆蓋率合併：已在 CI 中進行多 Python 版本測試並合併覆蓋率資料。頁面頂部徽章與連結指向合併後的報告，以便於統一查看。

範例：在測試中可使用`PorscheAPITestCase`的`request_client`提供的`RequestsClient`進行外部請求模擬：

```python
from porsche.core.restframework.test import PorscheAPITestCase


class TestSomething(PorscheAPITestCase):
    def test_request(self):
        resp = self.request_client.get("http://localhost:8000/api/health/")
        self.assertEqual(resp.status_code, 200)
```

## 常見問題（FAQ）

1) 資料庫連線問題？

-   確認 Postgres 正在運行，且憑證匹配（compose 使用 .env）
-   檢查 PORSCHE_DATABASES**postgres**主機/連接埠/使用者/密碼
-   在容器環境中運作時，確保網路連通

2) SECRET_KEY 與 DEBUG？

-   生產環境請設定強隨機的 PORSCHE_SECRET_KEY，並設定 PORSCHE_DEBUG=false

3) 語言/時區？

-   預設：LANGUAGE_CODE=en-us，TIME_ZONE=UTC；可透過 Dynaconf 覆寫（如 PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE）

## 許可證

MIT License — 見[執照](../LICENSE)

## 參考

-   姜戈：<https://docs.djangoproject.com/>
-   Django REST 框架：<https://www.django-rest-framework.org/>
-   動態會議：<https://www.dynaconf.com/>
-   心理諮商：<https://www.psycopg.org/>
-   紫外線：<https://docs.astral.sh/uv/>

## 待辦
