from typing import TypedDict

from django.utils.translation import gettext_lazy
from rest_framework.fields import CharField, ChoiceField, MultipleChoiceField

from porsche.core.django.db.models.enums import PorscheGenericChoices
from porsche.core.django.validators import PasswordValidator, PhoneValidator


class PorscheChoiceReturn(TypedDict):
    value: str | int
    label: str


class PorscheChoiceField(ChoiceField):
    def __init__(self, choices: type[PorscheGenericChoices], **kwargs):
        self.choices_clazz = choices
        choices = choices.choices
        super().__init__(choices=choices, **kwargs)

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


class PorschePhoneField(CharField):
    default_error_messages = {"invalid": gettext_lazy("Enter a valid mobile phone number.")}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = PhoneValidator(message=self.error_messages["invalid"])
        self.validators.append(validator)


class PorschePasswordField(CharField):
    default_error_messages = {"invalid": gettext_lazy("Enter a valid password.")}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = PasswordValidator(message=self.error_messages["invalid"], min_length=8, require_lowercase=True)
        self.validators.append(validator)
