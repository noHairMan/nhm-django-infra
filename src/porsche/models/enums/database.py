from django.db.models import TextChoices

__all__ = [
    "DatabaseNamespace",
]


class DatabaseNamespace(TextChoices):
    DEFAULT = "default"
    POSTGRES = "postgres"
