from typing import AnyStr, Optional, override

from rest_framework.response import Response

from porsche.models.enums import BusinessCode


class PorscheResponse(Response):
    @override
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        code: BusinessCode | int = BusinessCode.SUCCESS,
        message: Optional[AnyStr] = None,
    ):
        if isinstance(code, int):
            code = BusinessCode(code)
        data = {
            "code": code.value,
            "data": data,
            "message": code.label if message is None else message,
        }
        super().__init__(data, status, template_name, headers, exception, content_type)
