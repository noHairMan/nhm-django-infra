# -*- coding: utf-8 -*-
from typing import Any, Iterable, Optional, override
from uuid import uuid4

from django.db import transaction
from django.db.models import Manager, Model, fields
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy

from porsche.core.constants import UID
from porsche.core.django.db.manager import PorscheManager


class PorscheModelBase(ModelBase):
    pass


class PorscheModel(Model, metaclass=PorscheModelBase):
    objects = PorscheManager()
    _objects = Manager()

    deleted = fields.BooleanField(null=False, blank=False, default=False, verbose_name=gettext_lazy("是否删除"))

    create_time = fields.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        verbose_name=gettext_lazy("创建时间"),
    )
    update_time = fields.DateTimeField(null=False, blank=False, auto_now=True, verbose_name=gettext_lazy("更新时间"))

    uid = fields.UUIDField(
        null=False,
        blank=False,
        unique=True,
        default=uuid4,
        db_index=True,
        verbose_name=gettext_lazy("唯一标识"),
    )

    class Meta:
        abstract = True

    def get_related_objects(self):
        return [
            f for f in self._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
        ]

    @override
    def delete(
        self,
        using: Any | None = None,
        keep_parents: bool = False,
        soft: bool = True,
    ) -> tuple[int, dict[str, int]]:
        with transaction.atomic(using=using, savepoint=False):
            if soft:
                self.deleted = True
                self.save(update_fields=["deleted"], using=using)

                for relation in self.get_related_objects():
                    related_objects = getattr(self, relation.get_accessor_name()).all()
                    for obj in related_objects:
                        if hasattr(obj, "deleted"):
                            obj.delete(using=using, soft=True)
                return 0, {}  # todo: check this
            return super().delete(using, keep_parents)

    @override
    def save(
        self,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if update_fields is not None:
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
