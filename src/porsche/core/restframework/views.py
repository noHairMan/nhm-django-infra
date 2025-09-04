from os import wait3
from traceback import format_exc
from typing import Any, override

import ujson
from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404, HttpRequest
from rest_framework.exceptions import APIException, NotFound
from rest_framework.exceptions import PermissionDenied as RestFrameworkPermissionDenied
from rest_framework.views import APIView, set_rollback
from sqlparse.utils import offset

from porsche.core.restframework.exceptions import PorscheAPIException
from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse
from porsche.models.enums import BusinessCode
from porsche.utils.log import logger


class PorscheAPIView(APIView):
    @override
    def initialize_request(self, request: HttpRequest, *args, **kwargs) -> PorscheRequest:
        request = super().initialize_request(request, *args, **kwargs)
        return PorscheRequest.from_request(request)


def exception_handler(exc: Any, context) -> PorscheResponse:
    """
    override from `rest_framework.views.exception_handler`
    """
    origin_exc = exc
    if isinstance(origin_exc, Http404):
        exc = NotFound(*origin_exc.args)
    elif isinstance(origin_exc, DjangoPermissionDenied):
        exc = RestFrameworkPermissionDenied(*origin_exc.args)
    elif isinstance(origin_exc, APIException):
        exc = PorscheAPIException(*origin_exc.args)
        if auth_header := getattr(origin_exc, "auth_header", None):
            exc.auth_header = auth_header
        if wait := getattr(origin_exc, "wait", None):
            exc.wait = wait

    logger.error(format_exc())
    if isinstance(exc, NotFound):
        return PorscheResponse(code=BusinessCode.BAD_REQUEST, message="Not found")
    elif isinstance(exc, DjangoPermissionDenied):
        return PorscheResponse(code=BusinessCode.BAD_REQUEST, message="Permission denied")
    elif isinstance(exc, PorscheAPIException):
        headers = {}
        if auth_header := getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = auth_header
        if wait := getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % wait

        if isinstance(exc.detail, (list, dict)):
            message = ujson.dumps(exc.detail, ensure_ascii=False, escape_forward_slashes=False)
        else:
            message = exc.detail
        set_rollback()
        return PorscheResponse(code=exc.business_code, headers=headers, message=message or exc.message)
    # any other exception, raise server error.
    return PorscheResponse(code=BusinessCode.SERVER_ERROR, message=str(exc) if settings.DEBUG else None)
