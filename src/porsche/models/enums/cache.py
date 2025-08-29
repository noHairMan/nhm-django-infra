from django.db.models import TextChoices

__all__ = ["CacheNamespace"]


class CacheNamespace(TextChoices):
    DEFAULT = "default"
    REDIS = "redis"
    DJANGO_REDIS = "django_redis"
