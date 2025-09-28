# nhm-django-infra

[مبسطة الصينية]\|[إنجليزي](docs/README.en.md)\|[اليابانية](docs/README.ja.md)\|[فرنسي](docs/README.fr.md)\|[الأسبانية](docs/README.es.md)\|[الألمانية](docs/README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

سقالة خفيفة الوزن Django 5 + Django Rest Framework لخدمات الواجهة الخلفية ، بما في ذلك الميزات التالية:

-   واجهة التحقق الصحية: GET/API/Health/
-   بنية استجابة واجهة برمجة التطبيقات الموحدة (رمز/بيانات/رسالة) ومعالجة الاستثناءات العالمية
-   يستخدم SQLite افتراضيًا ؛ تكوين postgresql اختياري (مثال تجمع اتصال Psycopg الاحتياطي) ومثال Redis
-   تكوين متغير البيئة المستند إلى Dynaconf (يدعم .env)
-   توفير تكوين Gunicorn وأمثلة Docker
-   يوصى باستخدام الأشعة فوق البنفسجية لإدارة التبعية

## هيكل المشروع (موجز)

-   النشر/
    -   Dockerfile (استنادًا إلى Python: 3.13-SPLIM ، UV + Gunicorn)
    -   Docker-corm.yaml (خدمة postgresql)
    -   gunicorn.py （wsgi_app = porsche.wsgi: التطبيق）
    -   postgres/ (تهيئة البرنامج النصي مع postgres.conf)
-   SRC/
    -   manage.py
    -   بورش/
        -   الإعدادات
        -   urls.py (بادئة مسار API /API /)
        -   API/ endpoints/ (مثال التحقق الصحي)
        -   Core/RestRamework (عبوة DRF: الطلب/الاستجابة ، الاستثناء ، Mixins ، إلخ)

## المتطلبات البيئية

-   بيثون 3.13+
-   sqlite (افتراضي ؛ خارج الصندوق)
-   اختياري: PostgreSQL 17+ ، Redis ، Docker و Docker Compose
-   UV أو PIP

## التكوين (dynaconf)

-   بادئة متغير البيئة: Porsche\_
-   يدعم وضع ملفات .env في دليل جذر المشروع

مثال. ENV:

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

يوضح:

-   الافتراضي: debug = false ، المسموح بها \_hosts =["*"]، مثال Secret_key - يجب تغطية بيئة الإنتاج.
-   تستخدم مفاتيح Dynaconf المتداخلة الساحرة المزدوجة "**"، على سبيل المثال Porsche_Databases**postgres\_\_host。
-   REST_FRAMEWORK 使用 QueryParameterVersioning（默认版本=1）；默认 URL 前缀不包含版本。

## بداية سريعة محلية

استخدم الأشعة فوق البنفسجية (الموصى بها):

1) تثبيت الأشعة فوق البنفسجية (<https://docs.astral.sh/uv/）>2) تنفيذ في دليل جذر المشروع:

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) قاعدة البيانات:

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) الهجرة والبدء:

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

باستخدام PIP:

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`تبعيات ما بعد التثبيت (يوصى بالأشعة فوق البنفسجية أكثر)
3) الهجرة وبدء التشغيل متماثلان كما هو مذكور أعلاه

اختياري: إنشاء مستخدم سوبر

    uv run python src/manage.py createsuperuser

## Docker (Postgres المحلي)

يوفر المستودع مصيحًا إلى حد أدنى من docker.yaml (بما في ذلك postgres فقط):

1) إعداد .env في دليل جذر المشروع (على الأقل):

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) ابدأ:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) يتم تعيين Postgres لمضيف المنفذ 5432 ؛ يتم تثبيت البيانات/التكوين تحت النشر/postgres.

ملاحظة: لن يبدأ هذا التأليف تطبيق Django ؛ يمكنك بدء تشغيله محليًا باستخدام UV/PIP ، أو توسيع التأليف لزيادة خدمة التطبيق بنفسك.

## إنشاء صورة تطبيق (اختياري)

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

يوضح:

-   تبعيات وقت البناء تأتي من UV.lock مع pyproject.toml.
-   المدخل هو Gunicorn.
-   نقاط HealthCheck من Dockerfile إلى http&#x3A; // localhost: 8000/API/V1/Health. إذا كان التطبيق الخاص بك يستخدم /API /Health ، يرجى تحديث المسار أو
    إضافة بادئة إصدار في Pornche/urls.py.
-   للاتصال بـ Postgres في Compose ، تأكد من أن الشبكة يمكن الوصول إليها ، ويتم ضبط Porsche_Databases \_\_... متغير البيئة بشكل صحيح.

## مثال API

فحص الصحة:

-   طريق:`GET /api/health/`
-   الاستجابة (بنية موحدة):

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

-   حليقة:

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

أضف المزيد من الواجهات تحت SRC/Porsche/API/endpoints/و excregate في src/porsche/urls.py.

## سجلات واستثناءات

-   السجل: الإخراج إلى stdout (معالج وحدة التحكم) ، راجع الإعدادات.
-   استثناء: تم التعامل معها بشكل موحد بواسطة pornsche.core.restframework.views.exception_handler وإرجاع استجابة منظمة (رمز/بيانات/رسالة)

## الاختبار والتغطية

يقع الاختبار الأساسي في SRC/Porsche/Tests/. استخدم عداء اختبار Django الخاص (لا يوجد حاجة إلى Pytest).

-   المتطلب السابق: تثبيت التبعيات وتفعيل البيئة الافتراضية (UV الموصى بها)
    -   `uv sync && source .venv/bin/activate`
    -   إذا كان الاختبار يتطلب dB ، فتأكد من توفر Postgres ، أو ابدأ بـ Compose على النحو التالي

-   قم بتشغيل جميع الاختبارات:
    -   `uv run python src/manage.py test porsche`
    -   أو`python src/manage.py test porsche`

-   قم بتشغيل الحزمة/الوحدة النمطية المحددة/الاستخدام:
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   التغطية:
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`(الإخراج إلى HTMLCOV/)

## التعليمات

1) مشكلة اتصال قاعدة البيانات؟

-   تأكد من أن Postgres قيد التشغيل وتطابق بيانات الاعتماد (تأليف الاستخدامات .env)
-   تحقق من porsche_databases**postgres**المضيف/المنفذ/المستخدم/كلمة المرور
-   تأكد من اتصال الشبكة أثناء التشغيل في بيئة الحاويات

2) Secret_key و Debug؟

-   يرجى تعيين porsche_secret_keke العشوائي العشوائي في بيئة الإنتاج وتعيين Porsche_debug = false

3) اللغة/المنطقة الزمنية؟

-   الافتراضي: language_code = en-us ، time_zone = utc ؛ يمكن الكتابة فوقها بواسطة Dynaconf (مثل porsche_language_code / porsche_time_zone)

## رخصة

رخصة معهد ماساتشوستس للتكنولوجيا - انظر[رخصة](../LICENSE)

## مرجع

-   Django:<https://docs.djangoproject.com/>
-   إطار REST DJANGO:<https://www.django-rest-framework.org/>
-   Dynaconf:<https://www.dynaconf.com/>
-   psycopg:<https://www.psycopg.org/>
-   الأشعة فوق البنفسجية:<https://docs.astral.sh/uv/>

## للقيام
