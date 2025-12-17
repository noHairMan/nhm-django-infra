import django_filters

from porsche.models import Company


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.ModelMultipleChoiceFilter(queryset=Company.objects.all(), to_field_name="name")

    class Meta:
        model = Company
        fields = ["name"]
