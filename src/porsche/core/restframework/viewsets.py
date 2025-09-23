from rest_framework.viewsets import ViewSetMixin

from porsche.core.restframework import (
    PorscheCreateModelMixin,
    PorscheDestroyModelMixin,
    PorscheListModelMixin,
    PorscheRetrieveModelMixin,
    PorscheUpdateModelMixin,
    generics,
)


class PorscheGenericViewSet(ViewSetMixin, generics.PorscheGenericAPIView):
    pass


class PorscheModelViewSet(
    PorscheCreateModelMixin,
    PorscheUpdateModelMixin,
    PorscheDestroyModelMixin,
    PorscheListModelMixin,
    PorscheRetrieveModelMixin,
    PorscheGenericViewSet,
):
    pass
