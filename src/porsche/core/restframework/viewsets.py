# -*- coding: utf-8 -*-
from rest_framework.viewsets import ViewSetMixin

from porsche.core.restframework import generics, mixins

__all__ = [
    "PorscheModelViewSet",
]


class PorscheGenericViewSet(ViewSetMixin, generics.PorscheGenericAPIView):
    pass


class PorscheModelViewSet(
    mixins.PorscheCreateModelMixin,
    mixins.PorscheUpdateModelMixin,
    mixins.PorscheDestroyModelMixin,
    mixins.PorscheListModelMixin,
    mixins.PorscheRetrieveModelMixin,
    PorscheGenericViewSet,
):
    pass
