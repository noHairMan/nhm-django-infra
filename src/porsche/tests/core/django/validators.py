from django.core.exceptions import ValidationError

from porsche.core.django.validators import PasswordValidator, PhoneValidator
from porsche.core.restframework import PorscheAPITestCase


class TestValidators(PorscheAPITestCase):
    def test_phone_validator(self):
        validator = PhoneValidator(code="invalid_phone_number", strict=False)
        self.assertEqual(validator.message, PhoneValidator.message)
        self.assertEqual(hash(validator), hash((validator.message, validator.code, validator.strict)))

        validator = PhoneValidator(message="Invalid phone number", code="invalid_phone_number", strict=False)
        with self.assertRaises(ValidationError):
            validator("")
        with self.assertRaises(ValidationError):
            validator("123456789")
        with self.assertRaises(ValidationError):
            validator("1234567890a")
        with self.assertRaises(ValidationError):
            validator("21123456789")
        validator("11123456789")

        strict_validator = PhoneValidator(message="Invalid phone number", code="invalid_phone_number", strict=True)
        with self.assertRaises(ValidationError):
            strict_validator("11123456789")

        self.assertNotEqual(validator, strict_validator)
        self.assertEqual(
            strict_validator,
            PhoneValidator(message="Invalid phone number", code="invalid_phone_number", strict=True),
        )
        self.assertNotEqual(
            strict_validator,
            PhoneValidator(message="Invalid phone number", code="invalid_phone_number", strict=False),
        )
        self.assertNotEqual(
            strict_validator,
            PhoneValidator(message="Invalid phone number", code="1", strict=True),
        )
        self.assertNotEqual(
            strict_validator,
            PhoneValidator(message="1", code="invalid_phone_number", strict=True),
        )

    def test_password_validator(self):
        PasswordValidator(min_length=6)("123456")
        with self.assertRaises(ValidationError):
            PasswordValidator(min_length=6)("12345")

        with self.assertRaises(ValidationError):
            PasswordValidator(min_length=6)("")

        with self.assertRaises(ValidationError):
            PasswordValidator(require_lowercase=True)("12345678")
        PasswordValidator(require_lowercase=True)("a12345678")
        with self.assertRaises(ValidationError):
            PasswordValidator(require_uppercase=True)("a12345678")
        PasswordValidator(require_uppercase=True)("A12345678")
        with self.assertRaises(ValidationError):
            PasswordValidator(require_digit=True)("abcdefgh")
        PasswordValidator(require_digit=True)("abcdefgh123")
        with self.assertRaises(ValidationError):
            PasswordValidator(require_special_char=True)("12345678")
        PasswordValidator(require_special_char=True)("!@12345678")

        validator = PasswordValidator(code="test code")
        self.assertEqual(validator.code, "test code")
        self.assertEqual(
            hash(validator),
            hash(
                (
                    validator.message,
                    validator.code,
                    validator.min_length,
                    validator.require_uppercase,
                    validator.require_lowercase,
                    validator.require_digit,
                    validator.require_special_char,
                ),
            ),
        )

        self.assertEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="1",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="1",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=18,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=True,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=True,
                require_uppercase=False,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=True,
                require_special_char=False,
            ),
        )
        self.assertNotEqual(
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=False,
            ),
            PasswordValidator(
                message="",
                code="",
                min_length=8,
                require_lowercase=False,
                require_digit=False,
                require_uppercase=False,
                require_special_char=True,
            ),
        )
