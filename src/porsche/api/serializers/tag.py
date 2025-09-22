from porsche.core.restframework import PorscheModelSerializer
from porsche.core.restframework.fields import PorscheChoiceField
from porsche.core.restframework.validators import PorscheUniqueTogetherValidator
from porsche.models import Tag


class TagSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateSerializer(PorscheModelSerializer):
    category = PorscheChoiceField(choices=Tag.Category)

    class Meta:
        model = Tag
        fields = ["name", "category"]
        validators = [
            PorscheUniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=["name", "category"],
            ),
        ]


class TagListSerializer(PorscheModelSerializer):
    category = PorscheChoiceField(choices=Tag.Category)

    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]


class TagRetrieveSerializer(PorscheModelSerializer):
    category = PorscheChoiceField(choices=Tag.Category)

    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]
