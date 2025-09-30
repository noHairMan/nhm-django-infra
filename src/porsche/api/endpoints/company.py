from porsche.api.serializers.company import (
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyRetrieveSerializer,
    CompanyUpdateSerializer,
)
from porsche.core.restframework import PorscheModelViewSet
from porsche.models import Company


class CompanyViewSet(PorscheModelViewSet):
    queryset = Company.objects.all()
    list_serializer_class = CompanyListSerializer
    retrieve_serializer_class = CompanyRetrieveSerializer
    create_serializer_class = CompanyCreateSerializer
    update_serializer_class = CompanyUpdateSerializer

    search_fields = ("name",)
    ordering = ("name",)
