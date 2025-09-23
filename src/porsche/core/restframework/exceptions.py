from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy
from rest_framework.exceptions import APIException, ErrorDetail

from porsche.core.exceptions import PorscheException
from porsche.models.enums import BusinessCode


def get_error_details(data, default_code=None):
    if isinstance(data, (list, tuple)):
        ret = [get_error_details(item, default_code) for item in data]
        return ", ".join(value for value in ret)
    elif isinstance(data, dict):
        ret = {key: get_error_details(value, default_code) for key, value in data.items()}
        return ", ".join(f"{key}: {value}" for key, value in ret.items())

    text = force_str(data)
    code = getattr(data, "code", default_code)
    return ErrorDetail(text, code)


class PorscheAPIException(APIException, PorscheException):
    business_code = BusinessCode.BAD_REQUEST
    message = gettext_lazy("Api Exception")

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.detail = get_error_details(detail, code)


class PorscheServerException(PorscheException):
    business_code = BusinessCode.SERVER_ERROR
    message = gettext_lazy("Server Exception")
