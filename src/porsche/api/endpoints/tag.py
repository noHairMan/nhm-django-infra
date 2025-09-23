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
    """
    提供与标签相关的创建、删除、列表和检索操作的视图集。

    此类主要用于定义与标签相关的操作，继承自多个扩展的视图集和
    混入类。适用于处理标签模型的标准 RESTful 操作。

    Attributes:
        queryset (QuerySet): 定义要操作的标签模型查询集。
        create_serializer_class (Type[Serializer]): 用于创建操作的序列化器。
        list_serializer_class (Type[Serializer]): 用于列表操作的序列化器。
        retrieve_serializer_class (Type[Serializer]): 用于检索操作的序列化器。
    """

    queryset = Tag.objects.all()
    create_serializer_class = TagCreateSerializer
    list_serializer_class = TagListSerializer
    retrieve_serializer_class = TagRetrieveSerializer
