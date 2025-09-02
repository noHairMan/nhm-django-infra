from porsche.core.django.db.models import PorscheIntegerChoices

__all__ = [
    "BusinessCode",
]


class BusinessCode(PorscheIntegerChoices):
    SUCCESS = 0
    BAD_REQUEST = 1
    SERVER_ERROR = 2
