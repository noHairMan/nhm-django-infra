from django.db import models

from porsche.core.django.db.models.base import PorscheModel


class Company(PorscheModel):
    name = models.CharField(max_length=100)
