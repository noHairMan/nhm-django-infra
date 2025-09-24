from django.db.models import IntegerChoices, TextChoices
from django.db.models.enums import ChoicesType


class PorscheChoicesType(ChoicesType):
    pass


class PorscheGenericChoices(metaclass=PorscheChoicesType):
    choices: list[tuple[str | int, str]]
    values: list[str | int]
    labels: list[str]
    names: list[str]
    value: str | int
    label: str
    name: str


class PorscheTextChoices(TextChoices, PorscheGenericChoices, metaclass=PorscheChoicesType):
    pass


class PorscheIntegerChoices(IntegerChoices, PorscheGenericChoices, metaclass=PorscheChoicesType):
    pass
