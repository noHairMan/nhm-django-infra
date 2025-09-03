from django.utils.text import re_camel_case


def camel_case_to_snake_case(value):
    return re_camel_case.sub(r"_\1", value).strip().lstrip("_").lower()
