from django.db.models import TextChoices

__all__ = [
    "CacheNamespace",
    "DatabaseNamespace",
]


class CacheNamespace(TextChoices):
    DEFAULT = "default"
    REDIS = "redis"
    DJANGO_REDIS = "django_redis"


class DatabaseNamespace(TextChoices):
    DEFAULT = "default"
    POSTGRES = "postgres"
