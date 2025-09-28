# nazidjnjfra

[単純化された中国人]\|[英語](docs/README.en.md)\|[日本語](docs/README.ja.md)\|[フランス語](docs/README.fr.md)\|[スペイン語](docs/README.es.md)\|[ドイツ語](docs/README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

次の機能を含む、バックエンドサービスのための軽量のDjango 5 + Django RESTフレームワーク足場：

-   ヘルスチェックインターフェイス：get/api/health/
-   統合されたAPI応答構造（コード/データ/メッセージ）およびグローバル例外処理
-   sqliteはデフォルトで使用されます。オプションのpostgreSQL構成（PSYCOPG接続プールの例を予約）およびRedisの例
-   dynaconfベースの環境変数構成（サポート.env）
-   Gunicornの構成とDockerの例を提供します
-   依存関係管理にUVを使用することをお勧めします

## プロジェクト構造（概要）

-   展開/
    -   Dockerfile（Pythonに基づく：3.13スリム、ビルトインUV + Gunicorn）
    -   docker-compose.yaml（postgresqlサービス）
    -   gunicorn.py
    -   postgres/（postgres.confを使用してスクリプトを初期化）
-   SRC/
    -   manage.py
    -   ポルシェ/
        -   settings.py（dynaconf：アプリ名「ポルシェ」が有効）
        -   urls.py（APIパスプレフィックス /API /）
        -   API/エンドポイント/（ヘルスチェックの例）
        -   Core/RestFramework（DRFパッケージ：リクエスト/応答、例外、ミキシンなど）

## 環境要件

-   Python 3.13+
-   sqlite（デフォルト;箱から出して）
-   オプション：PostgreSQL 17+、Redis、Docker、Docker Compose
-   UVまたはPIP

## 配置（Dynaconf）

-   環境変数プレフィックス：Porsche\_
-   プロジェクトルートディレクトリに.ENVファイルの配置をサポートしています

例.ENV：

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

説明：

-   デフォルト：debug = false、aotad_hosts =["*"]、例Secret_key  - 生産環境をカバーする必要があります。
-   Dynaconfのネストされたキーは二重のアンダースコアを使用します」**「、例えばポルシェ\_DATABASES**postgres\_\_host。
-   REST_FRAMEWORK 使用 QueryParameterVersioning（默认版本=1）；默认 URL 前缀不包含版本。

## クイックスタートローカル

UV（推奨）を使用してください：

1）UVをインストールする（<https://docs.astral.sh/uv/）>2）プロジェクトルートディレクトリで実行する：

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3）データベース：

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4）移行と開始：

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

PIPの使用：

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`インストール後の依存関係（UVをもっとお勧めします）
3）移行と起動は上記と同じです

オプション：スーパーユーザーを作成します

    uv run python src/manage.py createsuperuser

## Docker（ローカルポストグレス）

仓库提供了一个最小化的 docker-compose.yaml（仅包含 Postgres）：

1）Project Root Directoryで.ENVを準備します（少なくとも）：

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2）開始：

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3）Postgresは、ポート5432をホストするためにマッピングされます。データ/構成は、アンダーデプロイメント/ポストグラスにマウントされます。

注：この構成は、Djangoアプリケーションを開始しません。 UV/PIPでローカルに起動するか、自分でアプリケーションサービスを増やすためにコンポーシングを展開できます。

## アプリケーション画像を作成する（オプション）

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

説明：

-   ビルドタイムの​​依存関係は、pyproject.tomlを使用したUV.Lockからのものです。
-   入り口はガニコーンです。
-   DockerfileのHealthCheckは、http：// localhost：8000/api/v1/healthを指します。アプリケーションが /API /ヘルスを使用している場合は、パスを更新するか、
    Pornche/urls.pyにバージョンされたプレフィックスを追加します。
-   ComposeのPostgresに接続するには、ネットワークにアクセスできることを確認し、Porsche_Database \_\_...環境変数が正しく設定されていることを確認してください。

## APIの例

健康チェック：

-   パス：`GET /api/health/`
-   応答（統一された構造）：

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

-   カール：

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

SRC/Porsche/API/Endpoints/およびSrc/Porsche/urls.pyの集合体の下にさらにインターフェイスを追加します。

## ログと例外

-   ログ：stdout（コンソールハンドラー）への出力、詳細についてはsettings.loggingを参照してください
-   例外：pornsche.core.restframework.views.exception_handlerによって均一に処理され、構造化された応答（コード/データ/メッセージ）を返します

## テストとカバレッジ

基本テストは、SRC/Porsche/Tests/にあります。 Django独自のテストランナーを使用します（pytestは必要ありません）。

-   前提条件：依存関係をインストールし、仮想環境（推奨UV）をアクティブにします
    -   `uv sync && source .venv/bin/activate`
    -   テストがDBを必要とする場合は、Postgresが利用可能であることを確認するか、次のようにComposeから始めてください

-   すべてのテストを実行します：
    -   `uv run python src/manage.py test porsche`
    -   または`python src/manage.py test porsche`

-   指定されたパッケージ/モジュール/ユースケースを実行します。
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   カバレッジ：
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`（htmlcovへの出力/）

## よくある質問

1）データベース接続の問題？

-   Postgresが実行されており、資格情報が一致していることを確認します（ComposeS .ENV）
-   Porsche_Databaseを確認してください**ポストグレス**ホスト/ポート/ユーザー/パスワード
-   コンテナ環境での実行中にネットワーク接続を確保します

2）Secret_Keyとデバッグ？

-   生産環境で強力なランダムポルシェ\_secret_keyを設定し、porsche_debug = falseを設定してください

3）言語/タイムゾーン？

-   デフォルト：Language_code = en-us、time_zone = utc; dynaconf（porsche_language_code / porsche_time_zoneなど）によって上書きすることができます

## ライセンス

MITライセンス - 参照[ライセンス](../LICENSE)

## 参考

-   Django：<https://docs.djangoproject.com/>
-   Django RESTフレームワーク：<https://www.django-rest-framework.org/>
-   dynaconf：<https://www.dynaconf.com/>
-   psycopg：<https://www.psycopg.org/>
-   UV：<https://docs.astral.sh/uv/>

## やられます
