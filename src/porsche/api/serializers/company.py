from porsche.core.restframework import PorscheModelSerializer
from porsche.models import Company


class CompanySerializer(PorscheModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
