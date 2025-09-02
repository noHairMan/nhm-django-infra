from django.db.models import IntegerChoices, TextChoices

__all__ = [
    "PorscheTextChoices",
    "PorscheIntegerChoices",
]


class PorscheTextChoices(TextChoices):
    pass


class PorscheIntegerChoices(IntegerChoices):
    pass
