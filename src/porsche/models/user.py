from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django.utils.translation import gettext_lazy

from porsche.core.django.db.manager import PorscheManager
from porsche.core.django.db.models import PorscheForeignKey, PorscheModel, PorscheTextChoices, get_object


class Role(PorscheModel):
    class Category(PorscheTextChoices):
        BUILTIN = "builtin", gettext_lazy("内置")
        CUSTOM = "custom", gettext_lazy("自定义")

    class BuiltInName(PorscheTextChoices):
        ADMIN = "admin", gettext_lazy("管理员")
        USER = "user", gettext_lazy("普通用户")

    name = models.CharField(max_length=20, verbose_name=gettext_lazy("角色名"))
    category = models.CharField(max_length=20, verbose_name=gettext_lazy("角色类型"))
    description = models.TextField(blank=True, verbose_name=gettext_lazy("描述"))

    @classmethod
    def get_admin_uid(cls):
        return get_object(cls, name=cls.BuiltInName.ADMIN).uid


class UserManager(PorscheManager, _UserManager):
    pass


class User(PorscheModel, AbstractUser):
    objects = UserManager()
    _objects = _UserManager()

    phone = models.CharField(max_length=15, blank=True, verbose_name=gettext_lazy("手机号码"))
    avatar = models.FileField(upload_to="avatar", blank=True, verbose_name=gettext_lazy("头像"))
    role = PorscheForeignKey(to=Role, on_delete=models.PROTECT, verbose_name=gettext_lazy("角色"))

    REQUIRED_FIELDS = ["email", "phone", "role"]

    class Meta:
        pass
