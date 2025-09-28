# नाज़िदजंजफ्रा

[सरलीकृत चीनी]\|[अंग्रेज़ी](docs/README.en.md)\|[जापानी](docs/README.ja.md)\|[फ्रांसीसी](docs/README.fr.md)\|[स्पैनिश](docs/README.es.md)\|[जर्मन](docs/README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

एक हल्के Django 5 + Django REST फ्रेमवर्क बैकएंड सेवाओं के लिए मचान, जिसमें निम्नलिखित सुविधाएँ शामिल हैं:

-   स्वास्थ्य जांच इंटरफ़ेस: प्राप्त/एपीआई/स्वास्थ्य/
-   एकीकृत एपीआई प्रतिक्रिया संरचना (कोड/डेटा/संदेश) और वैश्विक अपवाद हैंडलिंग
-   SQLite का उपयोग डिफ़ॉल्ट रूप से किया जाता है; वैकल्पिक PostgreSQL कॉन्फ़िगरेशन (आरक्षित psycopg कनेक्शन पूल उदाहरण) और Redis उदाहरण
-   Dynaconf- आधारित पर्यावरण चर कॉन्फ़िगरेशन (समर्थन .ENV)
-   Gunicorn कॉन्फ़िगरेशन और डॉकर उदाहरण प्रदान करें
-   निर्भरता प्रबंधन के लिए यूवी का उपयोग करने की सिफारिश की जाती है

## परियोजना संरचना (संक्षिप्त)

-   परिनियोजन/
    -   Dockerfile (पायथन पर आधारित: 3.13-SLIM, अंतर्निहित UV + GUNICORN)
    -   docker-compose.yaml (PostgreSQL सेवा)
    -   gunicorn.py （wsgi_app = porsche.wsgi: अनुप्रयोग）
    -   Postgres/ (Postgres.conf के साथ स्क्रिप्ट इनिशियलाइज़ करें)
-   एसआरसी/
    -   manage.py
    -   पोर्श/
        -   Settings.py (dynaconf: ऐप नाम "पोर्श" सक्षम)
        -   urls.py (एपीआई पथ उपसर्ग /एपीआई /)
        -   एपीआई/ समापन बिंदु/ (स्वास्थ्य जांच उदाहरण)
        -   कोर/रेस्टफ्रेमवर्क (DRF पैकेजिंग: अनुरोध/प्रतिक्रिया, अपवाद, मिक्सिन, आदि)

## पर्यावरण आवश्यकताएं

-   पायथन 3.13+
-   Sqlite (डिफ़ॉल्ट; बॉक्स से बाहर)
-   वैकल्पिक: PostgreSQL 17+, Redis, Docker और Docker Compose
-   यूवी या पिप

## विन्यास

-   पर्यावरण चर उपसर्ग: पोर्श\_
-   प्रोजेक्ट रूट निर्देशिका में .ENV फ़ाइलों के प्लेसमेंट का समर्थन करता है

उदाहरण .env:

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

चित्रण:

-   डिफ़ॉल्ट: debug = गलत, अनुमत\_हॉस्ट =["*"], उदाहरण SECRET_KEY - उत्पादन वातावरण को कवर किया जाना चाहिए।
-   Dynaconf की नेस्टेड कुंजियाँ डबल अंडरस्कोर्स का उपयोग करती हैं "**", उदा। पोर्श\_डैबेस**Postgres\_\_host。
-   REST_FRAMEWORK QUERYPARAMETERVERSING (डिफ़ॉल्ट संस्करण = 1) का उपयोग करें; डिफ़ॉल्ट URL उपसर्ग में संस्करण नहीं है।

## त्वरित शुरुआत स्थानीय

यूवी (अनुशंसित) का उपयोग करें:

1) यूवी स्थापित करें (<https://docs.astral.sh/uv/）>2) प्रोजेक्ट रूट डायरेक्टरी में निष्पादित करें:

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) डेटाबेस:

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) माइग्रेट करें और शुरू करें:

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

PIP का उपयोग करना:

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`पोस्ट-इंस्टॉल निर्भरता (यूवी अधिक अनुशंसित है)
3) माइग्रेशन और स्टार्टअप ऊपर के समान हैं

वैकल्पिक: एक सुपर उपयोगकर्ता बनाएं

    uv run python src/manage.py createsuperuser

## डॉकटर (स्थानीय पद)

रिपॉजिटरी एक न्यूनतम डॉकटर-कॉम्पस प्रदान करता है ।yaml (केवल पोस्टग्रेस सहित):

1) प्रोजेक्ट रूट डायरेक्टरी में .env तैयार करें (कम से कम):

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) प्रारंभ:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres को पोर्ट 5432 की मेजबानी करने के लिए मैप किया जाता है; डेटा/कॉन्फ़िगरेशन परिनियोजन/पोस्टग्रेज के तहत माउंट किया गया है।

नोट: यह रचना Django आवेदन शुरू नहीं करेगी; आप इसे स्थानीय रूप से यूवी/पीआईपी के साथ शुरू कर सकते हैं, या एप्लिकेशन सेवा को स्वयं बढ़ाने के लिए रचना का विस्तार कर सकते हैं।

## एक एप्लिकेशन इमेज (वैकल्पिक) का निर्माण करें

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

चित्रण:

-   बिल्ड-टाइम डिपेंडेंसी Pyproject.toml के साथ uv.lock से आती है।
-   प्रवेश द्वार गनीकोर्न है।
-   Dockerfile का HealthCheck http&#x3A; // localhost: 8000/API/v1/स्वास्थ्य को इंगित करता है। यदि आपका एप्लिकेशन /एपीआई /स्वास्थ्य का उपयोग करता है, तो कृपया पथ को अपडेट करें या
    पोर्नचे/urls.py में एक संस्करण का उपसर्ग जोड़ें।
-   रचना में पोस्टग्रेस से कनेक्ट करने के लिए, सुनिश्चित करें कि नेटवर्क सुलभ है और पोर्श\_डैबेस \_\_... पर्यावरण चर सही तरीके से सेट किया गया है।

## एपीआई उदाहरण

स्वास्थ्य जांच:

-   पथ:`GET /api/health/`
-   प्रतिक्रिया (एकीकृत संरचना):

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

-   कर्ल ：

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

SRC/Porsche/API/ENDPOINTS/और SRC/Porsche/urls.py में एकत्रीकरण के तहत अधिक इंटरफेस जोड़ें।

## लॉग और अपवाद

-   लॉग: Stdout (कंसोल हैंडलर) के लिए आउटपुट, विवरण के लिए सेटिंग्स।
-   अपवाद: समान रूप से pornsche.core.restframework.views.exception_handler द्वारा संभाला जाता है और एक संरचित प्रतिक्रिया (कोड/डेटा/संदेश) देता है

## परीक्षण और कवरेज

मूल परीक्षण SRC/Porsche/परीक्षणों/में स्थित है। Django के अपने टेस्ट रनर (कोई पाइटेस्ट की आवश्यकता नहीं) का उपयोग करें।

-   शर्त: निर्भरता स्थापित करें और आभासी वातावरण को सक्रिय करें (अनुशंसित यूवी)
    -   `uv sync && source .venv/bin/activate`
    -   यदि परीक्षण को DB की आवश्यकता है, तो सुनिश्चित करें कि Postgres उपलब्ध है, या निम्नलिखित के साथ शुरू करें

-   सभी परीक्षण चलाएं:
    -   `uv run python src/manage.py test porsche`
    -   या`python src/manage.py test porsche`

-   निर्दिष्ट पैकेज/मॉड्यूल/उपयोग केस चलाएं:
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   कवरेज:
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`(HTMLCOV को आउटपुट/)

## उपवास

1) डेटाबेस कनेक्शन समस्या?

-   पुष्टि करें कि Postgres चल रहा है और क्रेडेंशियल्स मैच (उपयोग करता है .ENV)
-   Porsche_databases की जाँच करें**postgres**होस्ट/पोर्ट/उपयोगकर्ता/पासवर्ड
-   कंटेनर वातावरण में चलते समय नेटवर्क कनेक्टिविटी सुनिश्चित करें

2) सीक्रेट\_की और डिबग?

-   कृपया उत्पादन वातावरण में मजबूत यादृच्छिक porsche_secret_key सेट करें और porsche_debug = गलत सेट करें

3) भाषा/समय क्षेत्र?

-   डिफ़ॉल्ट: language_code = en-us, time_zone = utc; dynaconf द्वारा अधिलेखित किया जा सकता है (जैसे कि porsche_language_code / porsche_time_zone)

## लाइसेंस

एमआईटी लाइसेंस - देखें[लाइसेंस](../LICENSE)

## संदर्भ

-   Django:<https://docs.djangoproject.com/>
-   Django REST फ्रेमवर्क:<https://www.django-rest-framework.org/>
-   Dynaconf:<https://www.dynaconf.com/>
-   psycopg:<https://www.psycopg.org/>
-   UV:<https://docs.astral.sh/uv/>

## किया गया
