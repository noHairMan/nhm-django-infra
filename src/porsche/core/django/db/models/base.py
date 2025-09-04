# -*- coding: utf-8 -*-
from typing import Any, Iterable, Optional, override
from uuid import uuid4

from django.conf import settings
from django.db import transaction
from django.db.models import Manager, Model, fields
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy

from porsche.core.django.db.manager import PorscheManager
from porsche.models.constants import UID
from porsche.utils.text import camel_case_to_snake_case


class PorscheModelBase(ModelBase):
    def __new__(cls, name, bases, namespace, **kwargs):
        if "Meta" in namespace:
            Meta = namespace["Meta"]
        else:

            class Meta:
                pass

        if not getattr(Meta, "default_related_name", None):
            Meta.default_related_name = camel_case_to_snake_case(name)

        namespace["Meta"] = Meta
        return super().__new__(cls, name, bases, namespace, **kwargs)


class PorscheModel(Model, metaclass=PorscheModelBase):
    objects = PorscheManager()
    _objects = Manager()

    deleted = fields.BooleanField(default=False, verbose_name=gettext_lazy("是否删除"))

    create_time = fields.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy("创建时间"))
    update_time = fields.DateTimeField(auto_now=True, verbose_name=gettext_lazy("更新时间"))

    uid = fields.UUIDField(unique=True, default=uuid4, db_index=True, verbose_name=gettext_lazy("唯一标识"))

    class Meta:
        abstract = True

    def get_related_objects(self):
        related_objects = [
            f for f in self._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
        ]
        return related_objects

    @override
    def delete(
        self,
        using: Any | None = None,
        keep_parents: bool = False,
        soft: bool = True,
    ) -> tuple[int, dict[str, int]]:
        with transaction.atomic(using=using, savepoint=False):
            if soft:
                soft_count = 1
                soft_delete_objects = {}
                for relation in self.get_related_objects():
                    related_objects = getattr(self, relation.get_accessor_name()).all()
                    for obj in related_objects:
                        count, related_dict = obj.delete(using=using, soft=True)
                        soft_delete_objects |= related_dict
                        soft_count += count

                self.deleted = True
                self.save(update_fields=["deleted"], using=using)

                return soft_count, (soft_delete_objects | {f"{settings.APP}.{self.__class__.__name__}": 1})
            return super().delete(using, keep_parents)

    @override
    def save(
        self,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if update_fields is not None and "update_time" not in update_fields:
            update_fields = list(update_fields)
            update_fields.append("update_time")

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


def get_object[T: PorscheModel | Model](
    model: type[T],
    uid: Optional[UID] = None,
    *,
    raise_exception: bool = False,
    **kwargs,
) -> Optional[T]:
    if uid:
        kwargs.setdefault("uid", uid)
    try:
        instance = model.objects.get(**kwargs)
    except model.DoesNotExist:
        if raise_exception:
            raise
        instance = None
    return instance
