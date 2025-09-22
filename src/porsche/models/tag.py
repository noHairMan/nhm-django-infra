from django.db import models
from django.utils.translation import gettext_lazy

from porsche.core.django.db.models import PorscheModel, PorscheTextChoices

__all__ = [
    "Tag",
]


class Tag(PorscheModel):
    class Category(PorscheTextChoices):
        COMPANY = "company", gettext_lazy("公司")

    name = models.CharField(max_length=20, verbose_name=gettext_lazy("标签名称"))
    category = models.CharField(max_length=20, verbose_name=gettext_lazy("标签类型"))
