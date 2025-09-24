from django.db import transaction
from rest_framework import mixins


class PorscheCreateModelMixin(mixins.CreateModelMixin):
    def perform_create(self, serializer):
        with transaction.atomic():
            super().perform_create(serializer)


class PorscheUpdateModelMixin(mixins.UpdateModelMixin):
    def perform_update(self, serializer):
        with transaction.atomic():
            super().perform_update(serializer)


class PorscheDestroyModelMixin(mixins.DestroyModelMixin):
    def perform_destroy(self, instance):
        with transaction.atomic():
            super().perform_destroy(instance)


class PorscheListModelMixin(mixins.ListModelMixin):
    pass


class PorscheRetrieveModelMixin(mixins.RetrieveModelMixin):
    pass
