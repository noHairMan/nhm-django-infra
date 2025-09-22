from typing import TypedDict

from rest_framework.fields import ChoiceField, MultipleChoiceField

from porsche.core.django.db.models.enums import PorscheGenericChoices


class PorscheChoiceReturn(TypedDict):
    value: str | int
    label: str


class PorscheChoiceField(ChoiceField):
    def __init__(self, choices: type[PorscheGenericChoices], **kwargs):
        super().__init__(choices=choices.choices, **kwargs)
        self.choices_clazz = choices

    def to_representation(self, value) -> PorscheChoiceReturn:
        value = super().to_representation(value)
        clazz = self.choices_clazz(value)
        return {
            "value": clazz.value,
            "label": clazz.label,
        }


class PorscheMultipleChoiceField(MultipleChoiceField):

    def __init__(self, choices: type[PorscheGenericChoices], **kwargs):
        super().__init__(choices=choices.choices, **kwargs)
        self.choices_clazz = choices

    def to_representation(self, value) -> list[PorscheChoiceReturn]:
        value = super().to_representation(value)
        results = []
        for item in value:
            clazz = self.choices_clazz(item)
            results.append(
                {
                    "value": clazz.value,
                    "label": clazz.label,
                },
            )
        return results
