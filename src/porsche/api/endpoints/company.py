from porsche.api.serializers.company import CompanySerializer
from porsche.core.restframework import PorscheModelViewSet
from porsche.models import Company


class CompanyViewSet(PorscheModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
