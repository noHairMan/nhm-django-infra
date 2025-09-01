from traceback import format_exc
from typing import override

import ujson
from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException, NotFound
from rest_framework.exceptions import PermissionDenied as RestFrameworkPermissionDenied
from rest_framework.views import APIView, set_rollback

from porsche.core.restframework.exceptions import PorscheAPIException
from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse
from porsche.models.enums import BusinessCode
from porsche.utils.log import logger


class PorscheAPIView(APIView):
    @override
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        return PorscheRequest.from_request(request)


def exception_handler(exc, context):
    """
    override from `rest_framework.views.exception_handler`
    """
    if isinstance(exc, Http404):
        exc = NotFound(*exc.args)
    elif isinstance(exc, DjangoPermissionDenied):
        exc = RestFrameworkPermissionDenied(*exc.args)
    elif isinstance(exc, APIException):
        exc = PorscheAPIException(*exc.args)

    logger.error(format_exc())
    if isinstance(exc, PorscheAPIException):
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
    return PorscheResponse(code=BusinessCode.SERVER_ERROR, message=str(exc) if settings.DEBUG else None)
