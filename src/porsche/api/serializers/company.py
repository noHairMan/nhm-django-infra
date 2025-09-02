from porsche.core.restframework import PorscheModelSerializer
from porsche.core.restframework.validators import PorscheUniqueTogetherValidator
from porsche.models import Company

company_validators = [
    PorscheUniqueTogetherValidator(
        queryset=Company.objects.all(),
        fields=["name"],
    ),
]


class CompanyListSerializer(PorscheModelSerializer):
    class Meta:
        model = Company
        fields = ["uid", "name"]


class CompanyRetrieveSerializer(PorscheModelSerializer):
    class Meta:
        model = Company
        fields = ["uid", "name"]


class CompanyCreateSerializer(PorscheModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]
        validators = company_validators


class CompanyUpdateSerializer(PorscheModelSerializer):
    class Meta:
        model = Company
        fields = ["name"]
        validators = company_validators
