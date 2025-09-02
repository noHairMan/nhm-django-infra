from rest_framework import serializers

from porsche.core.restframework import PorscheModelSerializer
from porsche.core.restframework.validators import PorscheUniqueTogetherValidator
from porsche.models import Tag


class TagSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateSerializer(PorscheModelSerializer):
    category = serializers.ChoiceField(choices=Tag.Category.choices)

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
    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]


class TagRetrieveSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]
