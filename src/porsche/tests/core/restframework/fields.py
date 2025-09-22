from django.db import models

from porsche.core.django.db.models import PorscheModel
from porsche.core.restframework import PorscheModelSerializer
from porsche.core.restframework.fields import PorscheChoiceField, PorscheMultipleChoiceField
from porsche.core.restframework.test import PorscheAPITestCase
from porsche.models import Tag


class TestFields(PorscheAPITestCase):
    def test_porsche_choice_field(self):
        class Serializer(PorscheModelSerializer):
            category = PorscheChoiceField(choices=Tag.Category)

            class Meta:
                model = Tag
                fields = ["category"]

        tag = Tag.objects.create(name="test", category=Tag.Category.COMPANY)
        serializer = Serializer(instance=tag)
        self.assertEqual(
            serializer.data["category"],
            {
                "value": Tag.Category.COMPANY.value,
                "label": Tag.Category.COMPANY.label,
            },
        )

    def test_porsche_multiple_choice_field(self):
        class Serializer(PorscheModelSerializer):
            category = PorscheMultipleChoiceField(choices=Tag.Category)

            class Meta:
                model = Tag
                fields = ["category"]

        class TestTag(PorscheModel):
            category = models.JSONField(max_length=200)

        tag = TestTag(category=[Tag.Category.COMPANY.value, Tag.Category.COMPANY.value])
        serializer = Serializer(instance=tag)
        self.assertEqual(
            serializer.data["category"],
            [
                {
                    "value": Tag.Category.COMPANY.value,
                    "label": Tag.Category.COMPANY.label,
                },
            ],
        )
