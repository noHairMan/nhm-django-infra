# ご協力に感謝いたします

[簡体字中国語](/docs/README.zh.md)\|[英語](/docs/README.en.md)\|[日本語](/docs/README.ja.md)\|[繁体中文](/docs/README.zh-TW.md)

![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FnoHairMan%2Fnhm-django-infra%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.requires-python&label=python)![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noHairMan/nhm-django-infra/build.yml)[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

バックエンド サービス用の軽量の Django 5 + Django REST フレームワーク スキャフォールディングには、次の機能が含まれます。

-   ヘルスチェックインターフェイス: GET /api/health/
-   統合された API 応答構造 (コード/データ/メッセージ) とグローバル例外処理
-   SQLite がデフォルトで使用されます。オプションの PostgreSQL 構成 (psycopg 接続プールの例用に予約) と Redis の例
-   Dynaconf ベースの環境変数設定 (.env をサポート)
-   Gunicorn 構成と Docker サンプルを提供する
-   依存関係の管理には uv を使用することをお勧めします
-   OpenAPI 3 (カスタマイズされた AutoSchema、統合された PyYAML) をサポートし、インターフェイス仕様の生成とリリースを容易にします。
-   フィルタリングと並べ替えをサポートするための権限の例と組み込みの FilterBackend (検索/順序付け) を提供します
-   共同デバッグと自動化を容易にするためのシンプルなリクエスト/テスト ツール (request_client) を提供します。

## プロジェクトの構造（概要）

-   導入/
    -   Dockerfile (Python:3.13-slim ベース、組み込み uv + gunicorn)
    -   docker-compose.yaml (PostgreSQL サービス)
    -   gunicorn.py（wsgi_app=porsche.wsgi:application）
    -   postgres/ (初期化スクリプトとpostgres.conf)
-   ソース/
    -   manage.py
    -   ポルシェ/
        -   settings.py (Dynaconf 有効: APP 名「porsche」)
        -   urls.py (API パス接頭辞 /api/)
        -   api/endpoints/ (ヘルスチェックの例)
        -   コア/レストフレームワーク (DRF パッケージ化: リクエスト/レスポンス、例外、ミックスインなど)

## 環境要件

-   Python 3.13+
-   SQLite (デフォルト、すぐに使用可能)
-   オプション: PostgreSQL 17 以降、Redis、Docker、Docker Compose
-   uvまたはpip

## 配置（Dynaconf）

-   環境変数プレフィックス: PORSCHE\_
-   プロジェクトのルート ディレクトリへの .env ファイルの配置をサポート

.env の例:

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

例証します:

-   デフォルト: DEBUG=false、ALLOWED_HOSTS=["*"]、SECRET_KEY の例 - 運用環境をカバーする必要があります。
-   Dynaconf のネストされたキーは二重アンダースコアを使用します。**"、例: PORSCHE_DATABASES**postgres\_\_HOST。
-   REST_FRAMEWORK は QueryParameterVersioning を使用します (デフォルトのバージョン = 1)。デフォルトの URL プレフィックスにはバージョンが含まれません。 API バージョン番号は設定から​​動的に取得できます。

## ローカルのクイックスタート

UV を使用します (推奨):

1) uv(<https://docs.astral.sh/uv/）>2) プロジェクトのルート ディレクトリで実行します。

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) データベース:

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) 移行して開始します。

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

ピップを使用します。

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`後で依存関係をインストールします (uv を使用することをお勧めします)
3) 移行と起動は上記と同じ

オプション: スーパーユーザーを作成します

    uv run python src/manage.py createsuperuser

## Docker (ネイティブ Postgres)

リポジトリは、最小限の docker-compose.yaml (Postgres のみを含む) を提供します。

1) プロジェクトのルート ディレクトリに .env を準備します (少なくとも次のものを含みます)。

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) 開始:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres はホストのポート 5432 にマッピングされます。 data/configuration は、deployment/postgres の下にマウントされます。

注: この作成では Django アプリケーションは起動しません。 uv/pip を使用してローカルで開始することも、Compose を自分で拡張してアプリケーション サービスを追加することもできます。

-   ヘルスチェック: イメージヘルスチェックのパスが指定されました`/api/health/`、コンテナ オーケストレーションの稼働状態/準備状態に使用できます。

## アプリケーションイメージのビルド (オプション)

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

例証します:

-   ビルド時の依存関係は、uv.lock と pyproject.toml から取得されます。
-   入口はガニコーンです。
-   Compose で Postgres に接続するには、ネットワークに到達可能であり、PORSCHE_DATABASES\_\_... 環境変数が正しく設定されていることを確認してください。

## APIの例

ヘルスチェック:

-   パス：`GET /api/health/`
-   応答 (統合構造):

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

src/porsche/api/endpoints/ の下にさらにインターフェイスを追加し、src/porsche/urls.py に集約します。

### フィルタリング、並べ替え、権限

-   フィルタ/検索: サポート`?search=关键字`
-   並べ替え: サポート`?ordering=字段`または`?ordering=-created_at`
-   権限: DRF 権限クラスとカスタム権限は必要に応じて構成できます。例は次のとおりです。`porsche/core/restframework`

### OpenAPI 3 とスキーマ

-   API 仕様のエクスポートと公開を容易にするために、OpenAPI 3 が採用され、AutoSchema がカスタマイズされ、PyYAML が統合されました。
-   インターフェイス仕様を生成または公開する必要がある場合は、プロジェクト内の対応するルート/コマンドを拡張できます。を参照してください。`porsche/core/restframework`

## ログと例外

-   ログ: 標準出力 (コンソール ハンドラー) に出力します。詳細については、settings.LOGGING を参照してください。
-   例外: porsche.core.restframework.views.Exception_handler によって均一に処理され、構造化された応答 (コード/データ/メッセージ) を返します。

## テストと適用範囲

基本的なテストは src/porsche/tests/ にあります。 Django の組み込みテスト ランナーを使用します (pytest は必要ありません)。

-   前提条件: 依存関係をインストールし、仮想環境をアクティブ化します (UV を推奨)
    -   `uv sync && source .venv/bin/activate`
    -   テストに DB が必要な場合は、Postgres が利用可能であることを確認するか、次のように compose を通じてテストを開始します。

-   すべてのテストを実行します。
    -   `uv run python src/manage.py test porsche`
    -   または`python src/manage.py test porsche`

-   マルチバージョンのローカルテストには tox を使用します。
    -   プレフィックス:`pip install tox`(構成は統合されています)`tox-uv`)
    -   サポートされているすべてのバージョン (py312、py313、py314) を実行します。`tox`
    -   指定されたバージョンを実行します。`tox -e py313`

-   指定されたパッケージ/モジュール/ユースケースを実行します。
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   カバレッジ：
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`(htmlcov/に出力)

-   CI とカバレッジのマージ: 複数の Python バージョンのテストが CI で行われ、カバレッジ データがマージされました。ページ上部のバッジとリンクは、統合されたレポートを指し、統合された表示を可能にします。

例: テストで使用できます`PorscheAPITestCase`の`request_client`提供的`RequestsClient`外部リクエストのシミュレーションを実行します。

```python
from porsche.core.restframework.test import PorscheAPITestCase


class TestSomething(PorscheAPITestCase):
    def test_request(self):
        resp = self.request_client.get("http://localhost:8000/api/health/")
        self.assertEqual(resp.status_code, 200)
```

## よくある質問 (FAQ)

1) データベース接続に問題がありますか?

-   Postgres が実行中であり、資格情報が一致していることを確認します (Compose は .env を使用します)。
-   PORSCHE_DATABASES を確認する**ポストグレ**ホスト/ポート/ユーザー/パスワード
-   コンテナ環境での実行時にネットワーク接続を確保する

2) SECRET_KEY と DEBUG?

-   本番環境では、強力なランダム PORSCHE_SECRET_KEY を設定し、PORSCHE_DEBUG=false を設定してください。

3) 言語/タイムゾーンは?

-   デフォルト: LANGUAGE_CODE=en-us、TIME_ZONE=UTC; Dynaconf を通じてオーバーライドできます (PORSCHE_LANGUAGE_CODE / PORSCHE_TIME_ZONE など)

## ライセンス

MIT ライセンス — を参照[ライセンス](../LICENSE)

## 参考

-   ジャンゴ:<https://docs.djangoproject.com/>
-   Django REST フレームワーク:<https://www.django-rest-framework.org/>
-   ダイナコンフ:<https://www.dynaconf.com/>
-   サイコパス:<https://www.psycopg.org/>
-   紫外線:<https://docs.astral.sh/uv/>

## やるべきこと
