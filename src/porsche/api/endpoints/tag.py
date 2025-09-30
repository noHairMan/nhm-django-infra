from porsche.api.serializers.tag import (
    TagCreateSerializer,
    TagListSerializer,
    TagRetrieveSerializer,
)
from porsche.core.restframework import (
    PorscheCreateModelMixin,
    PorscheDestroyModelMixin,
    PorscheListModelMixin,
    PorscheRetrieveModelMixin,
)
from porsche.core.restframework.viewsets import PorscheGenericViewSet
from porsche.models import Tag


class TagViewSet(
    PorscheCreateModelMixin,
    PorscheDestroyModelMixin,
    PorscheListModelMixin,
    PorscheRetrieveModelMixin,
    PorscheGenericViewSet,
):
    queryset = Tag.objects.all()
    create_serializer_class = TagCreateSerializer
    list_serializer_class = TagListSerializer
    retrieve_serializer_class = TagRetrieveSerializer
