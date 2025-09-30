from porsche.api.serializers.company import (
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyRetrieveSerializer,
    CompanyUpdateSerializer,
)
from porsche.core.restframework import PorscheModelViewSet
from porsche.models import Company


class CompanyViewSet(PorscheModelViewSet):
    """
    继承自 PorscheModelViewSet 的 CompanyViewSet 类。

    CompanyViewSet 是一个视图集，用于处理与 Company 模型相关的 API
    请求。它提供了一系列序列化器以应对不同操作的需求。

    Attributes:
        queryset (QuerySet): 查询集，定义了视图集操作的基础数据来源。
        list_serializer_class (type): 用于列表操作的序列化器。
        retrieve_serializer_class (type): 用于检索操作的序列化器。
        create_serializer_class (type): 用于创建操作的序列化器。
        update_serializer_class (type): 用于更新操作的序列化器。
    """

    queryset = Company.objects.all()
    list_serializer_class = CompanyListSerializer
    retrieve_serializer_class = CompanyRetrieveSerializer
    create_serializer_class = CompanyCreateSerializer
    update_serializer_class = CompanyUpdateSerializer

    search_fields = ("name",)
    ordering = ("name",)
