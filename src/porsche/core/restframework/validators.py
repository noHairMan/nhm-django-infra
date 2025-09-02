from django.utils.translation import gettext_lazy
from rest_framework.validators import UniqueTogetherValidator


class PorscheUniqueTogetherValidator(UniqueTogetherValidator):
    message = gettext_lazy("{field_names} 不能重复")
    missing_message = gettext_lazy("字段缺失")
