from django.db import models
from django.utils.translation import gettext_lazy

from porsche.core.django.db.models import PorscheForeignKey
from porsche.core.django.db.models.base import PorscheModel
from porsche.models.tag import Tag


class Company(PorscheModel):
    name = models.CharField(max_length=100, verbose_name=gettext_lazy("公司名称"))


class CompanyTag(PorscheModel):
    company = PorscheForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy("公司"),
    )
    tag = PorscheForeignKey(
        to=Tag,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy("标签"),
    )
