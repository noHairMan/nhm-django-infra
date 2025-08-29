# -*- coding: utf-8 -*-
from typing import Optional

from django.db import transaction
from django.db.models import Model, fields
from django.db.models.base import ModelBase
from django.utils.timezone import override

from porsche.core.django.db.manager import PorscheManager


class PorscheModelBase(ModelBase):
    pass


class PorscheModel(Model):
    """
    todo: wait for test, fuck!
    """

    objects = PorscheManager

    deleted = fields.BooleanField(default=False, null=False, blank=False, name="是否删除")

    create_time = fields.DateTimeField(null=False, blank=False, auto_now_add=True, name="创建时间")
    update_time = fields.DateTimeField(null=False, blank=False, auto_now=True, name="更新时间")

    uid = fields.UUIDField(null=False, blank=False, unique=True, db_index=True, name="唯一标识")

    class Meta:
        abstract = True

    def get_related_objects(self):
        return [
            f for f in self._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
        ]

    @override
    def delete(self, using=None, keep_parents=False, soft: bool = True):
        with transaction.atomic(using=using, savepoint=False):
            if soft:
                self.deleted = True
                self.save(update_fields=["deleted"], using=using)

                for relation in self.get_related_objects():
                    related_objects = getattr(self, relation.get_accessor_name()).all()
                    for obj in related_objects:
                        if hasattr(obj, "deleted"):
                            obj.delete(using=using, soft=True)
                return self
            return super().delete(using, keep_parents)

    @override
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if update_fields is not None:
            update_fields = list(update_fields)
            update_fields.append("update_time")

        super().save(force_insert, force_update, using, update_fields)


def get_object[T: PorscheModel | Model](model: type[T], raise_exception: bool = False, **kwargs) -> Optional[T]:
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        if raise_exception:
            raise
        return None
