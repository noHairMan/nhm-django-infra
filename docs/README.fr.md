# Nazidjnjfra

[Chinois simplifié]\|[Anglais](docs/README.en.md)\|[japonais](docs/README.ja.md)\|[Français](docs/README.fr.md)\|[Espagnol](docs/README.es.md)\|[Allemand](docs/README.de.md)

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/noHairMan/nhm-django-infra/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/noHairMan/nhm-django-infra/blob/python-coverage-comment-action-data/htmlcov/index.html)![GitHub License](https://img.shields.io/github/license/noHairMan/nhm-django-infra)

Un échafaudage de framework Django 5 + Django REST léger pour les services backend, y compris les fonctionnalités suivantes:

-   Interface de vérification de la santé: obtenez / API / SANTÉ /
-   Structure de réponse à l'API unifiée (code / données / message) et gestion globale des exceptions
-   SQLite est utilisé par défaut; Configuration postgresql facultative (réserve PSYCOPG Connection Pool Exemple) et exemple de redis
-   Configuration variable d'environnement basée sur Dynaconf (prend en charge .env)
-   Fournir des exemples de configuration de Gunicorn et de docker
-   Il est recommandé d'utiliser des UV pour la gestion des dépendances

## Structure du projet (bref)

-   déploiement/
    -   Dockerfile (basé sur Python: 3.13-slim, UV + Gunicorn intégré)
    -   docker-compose.yaml (service postgresql)
    -   gunicorn.py （wsgi_app = porsche.wsgi: application）
    -   Postgres / (Initialiser le script avec postgres.conf)
-   src /
    -   manage.py
    -   Porsche /
        -   Settings.py (Dynaconf: Nom de l'application "Porsche" activé)
        -   urls.py (API Path Prefix / API /)
        -   API / Points de terminaison / (Exemple de vérification de la santé)
        -   Core / RestFramework (emballage DRF: demande / réponse, exception, mixins, etc.)

## Exigences environnementales

-   Python 3.13+
-   Sqlite (par défaut; hors de la boîte)
-   Facultatif: postgresql 17+, redis, docker et docker compose
-   UV ou PIP

## Configuration (dynaconf)

-   Préfixe de variable d'environnement: Porsche\_
-   Prend en charge le placement des fichiers .env dans le répertoire racine du projet

Exemple .env:

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

illustrer:

-   Par défaut: debug = false, autorisé_hosts =["*"], exemple secret_key - L'environnement de production doit être couvert.
-   Les clés imbriquées de Dynaconf utilisent des doubles soulignements "**", par exemple Porsche_databases**postgres\_\_host。
-   REST_FRAMEWROWN Utilisez QueryParAmEterVerSioning (version par défaut = 1); Le préfixe d'URL par défaut ne contient pas la version.

## Démarrage rapide local

Utilisez UV (recommandé):

1) Installer UV (<https://docs.astral.sh/uv/）>2) Exécuter dans le répertoire racine du projet:

    - 同步依赖：`uv sync`
    - 激活虚拟环境：`source .venv/bin/activate`（或直接使用 `uv run`）

3) Base de données:

    - 使用本地 Postgres（创建 porsche 数据库并设置 .env），或
    - 使用 Docker Compose 启动 Postgres（见下文）

4) Migrer et démarrer:

    - `uv run python src/manage.py migrate`
    - `uv run python src/manage.py runserver 0.0.0.0:8000`
    - 或 `PYTHONPATH=src uv run gunicorn -c deployment/gunicorn.py`

Utilisation de PIP:

1)`python -m venv .venv && source .venv/bin/activate`2)`pip install -U pip`Dépendances après l'installation (UV est plus recommandé)
3) La migration et le démarrage sont les mêmes que ci-dessus

Facultatif: créer un super utilisateur

    uv run python src/manage.py createsuperuser

## Docker (Postgres local)

Le référentiel fournit un docker-compose.yaml minimisé (y compris les postgres uniquement):

1) Préparer .env dans le répertoire racine du projet (au moins):

    POSTGRES_DB=porsche
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.utf8

2) Démarrer:

    docker compose --env-file .env -f deployment/docker-compose.yaml up -d --build

3) Postgres est mappé pour hôte du port 5432; Les données / configuration sont montées sous déploiement / Postgres.

Remarque: Cette composition ne démarrera pas l'application Django; Vous pouvez le démarrer localement avec UV / PIP, ou développer la composition pour augmenter le service d'application par vous-même.

## Créer une image d'application (facultative)

    # 在项目根目录（Docker 24+）执行
    docker build -f deployment/Dockerfile -t nhm-django-infra:latest deployment

    # 运行示例
    docker run --rm -p 8000:8000 \
      --env-file .env \
      nhm-django-infra:latest

illustrer:

-   Les dépendances de build-time proviennent de uv.lock avec pyproject.toml.
-   L'entrée est Gunicorn.
-   Le HealthCheck du Dockerfile pointe vers http&#x3A; // localhost: 8000 / API / V1 / Health. Si votre application utilise / API / Santé, veuillez mettre à jour le chemin ou
    Ajoutez un préfixe versé dans Pornche / urls.py.
-   Pour se connecter à Postgres en composition, assurez-vous que le réseau est accessible et les Porsche_databases \_\_... La variable d'environnement est définie correctement.

## Exemple API

Vérification de la santé:

-   chemin:`GET /api/health/`
-   Réponse (structure unifiée):

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

-   Boucle:

```bash
curl -s http://127.0.0.1:8000/api/health/
# 使用 QueryParameterVersioning
curl -s "http://127.0.0.1:8000/api/health/?version=1"
```

Ajoutez plus d'interfaces sous SRC / Porsche / API / Points de terminaison / et agrégat dans SRC / Porsche / urls.py.

## Journaux et exceptions

-   Journal: sortie vers STDOUT (gestionnaire de console), voir les paramètres.logging pour plus de détails
-   Exception: uniformément géré par pornsche.core.restframework.views.exception_handler et renvoie une réponse structurée (code / données / message)

## Tests et couverture

Le test de base est situé dans SRC / Porsche / Tests /. Utilisez le propre coureur de test de Django (aucun pytest requis).

-   Préalable: installez les dépendances et activez l'environnement virtuel (UV recommandé)
    -   `uv sync && source .venv/bin/activate`
    -   Si le test nécessite une base de données, assurez-vous que Postgres est disponible, ou commencez par composer comme suit

-   Exécutez tous les tests:
    -   `uv run python src/manage.py test porsche`
    -   ou`python src/manage.py test porsche`

-   Exécutez le package / module spécifié / cas d'utilisation:
    -   `uv run python src/manage.py test porsche.tests.core`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base`
    -   `uv run python src/manage.py test porsche.tests.core.django.db.models.base.TestPorscheModel.test_create_model`

-   Couverture:
    -   `uv run coverage run src/manage.py test porsche`
    -   `uv run coverage report`
    -   `uv run coverage html`(Sortie à Htmlcov /)

## FAQ

1) Problème de connexion de la base de données?

-   Confirmez que Postgres est en cours d'exécution et que les informations d'identification correspondent (Compose utilise .env)
-   Vérifiez Porsche_Databases**postgres**Hôte / port / utilisateur / mot de passe
-   Assurer la connectivité réseau lors de l'exécution dans un environnement de conteneur

2) Secret_key et débogage?

-   Veuillez définir une forte Porsche_Secret_key aléatoire dans l'environnement de production et définir Porsche_debug = false

3) Langue / fuseau horaire?

-   Default: Language_code = en-us, time_zone = UTC; Peut être écrasé par Dynaconf (comme Porsche_Language_Code / Porsche_time_Zone)

## licence

Licence MIT - Voir[LICENCE](../LICENSE)

## référence

-   Django:<https://docs.djangoproject.com/>
-   Framework Django REST:<https://www.django-rest-framework.org/>
-   Dynaconf:<https://www.dynaconf.com/>
-   psycopg:<https://www.psycopg.org/>
-   UV:<https://docs.astral.sh/uv/>

## À faire
