import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy


@deconstructible
class PhoneValidator:
    """
    中国大陆手机号码验证器

    规则：
    - 长度必须为11位
    - 必须全部为数字
    - 必须以1开头
    - 第二位数字必须是3,4,5,6,7,8,9中的一个（符合运营商号段规则）
    """

    message = gettext_lazy("Enter a valid mobile phone number.")
    code = "invalid"

    # 详细的号段规则（可选，用于更严格的验证）
    detailed_phone_regex = re.compile(r"^1(3[0-9]|4[01456879]|5[0-35-9]|6[2567]|7[0-8]|8[0-9]|9[0-35-9])\d{8}$")

    def __init__(self, message=None, code=None, strict=False):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.strict = strict

    def __call__(self, value: str):
        if not value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        # 去除可能的空格和特殊字符
        cleaned_value = re.sub(r"[\s\-\(\)]", "", str(value))

        # 基本格式检查
        if len(cleaned_value) != 11:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if not cleaned_value.isdigit():
            raise ValidationError(self.message, code=self.code, params={"value": value})

        # 必须以1开头
        if not cleaned_value.startswith("1"):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if self.strict and not self.detailed_phone_regex.match(cleaned_value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and (self.message == other.message)
            and (self.code == other.code)
            and (self.strict == other.strict)
        )

    def __hash__(self):
        return hash((self.message, self.code, self.strict))


@deconstructible
class PasswordValidator:
    """
    密码验证器

    规则：
    - 至少包含一个大写字母
    - 至少包含一个小写字母
    - 至少包含一个数字
    - 至少包含一个特殊字符（非字母数字和空格）
    - 长度至少8位
    """

    message = gettext_lazy("Enter a valid password.")
    code = "invalid"

    # 密码强度规则的正则表达式
    uppercase_regex = re.compile(r"[A-Z]")  # 至少一个大写字母
    lowercase_regex = re.compile(r"[a-z]")  # 至少一个小写字母
    digit_regex = re.compile(r"\d")  # 至少一个数字
    special_char_regex = re.compile(r"[^A-Za-z0-9\s]")  # 至少一个特殊字符（非字母数字和空格）

    def __init__(
        self,
        message=None,
        code=None,
        min_length=8,
        require_uppercase=False,
        require_lowercase=False,
        require_digit=False,
        require_special_char=False,
    ):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special_char = require_special_char

    def __call__(self, value: str):
        if not value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        password = str(value)

        # 检查最小长度
        if len(password) < self.min_length:
            raise ValidationError(
                gettext_lazy("Password must be at least {min_length} characters long."),
                code="too_short",
                params={"value": value, "min_length": self.min_length},
            )

        # 检查是否包含大写字母
        if self.require_uppercase and not self.uppercase_regex.search(password):
            raise ValidationError(
                gettext_lazy("Password must contain at least one uppercase letter."),
                code="missing_uppercase",
                params={"value": value},
            )

        # 检查是否包含小写字母
        if self.require_lowercase and not self.lowercase_regex.search(password):
            raise ValidationError(
                gettext_lazy("Password must contain at least one lowercase letter."),
                code="missing_lowercase",
                params={"value": value},
            )

        # 检查是否包含数字
        if self.require_digit and not self.digit_regex.search(password):
            raise ValidationError(
                gettext_lazy("Password must contain at least one digit."),
                code="missing_digit",
                params={"value": value},
            )

        # 检查是否包含特殊字符
        if self.require_special_char and not self.special_char_regex.search(password):
            raise ValidationError(
                gettext_lazy("Password must contain at least one special character."),
                code="missing_special_char",
                params={"value": value},
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and (self.message == other.message)
            and (self.code == other.code)
            and (self.min_length == other.min_length)
            and (self.require_uppercase == other.require_uppercase)
            and (self.require_lowercase == other.require_lowercase)
            and (self.require_digit == other.require_digit)
            and (self.require_special_char == other.require_special_char)
        )

    def __hash__(self):
        return hash(
            (
                self.message,
                self.code,
                self.min_length,
                self.require_uppercase,
                self.require_lowercase,
                self.require_digit,
                self.require_special_char,
            ),
        )
