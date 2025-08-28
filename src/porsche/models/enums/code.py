from django.db.models import IntegerChoices

__all__ = ["BusinessCode"]


class BusinessCode(IntegerChoices):
    SUCCESS = 0
    BAD_REQUEST = 1
    SERVER_ERROR = 2
