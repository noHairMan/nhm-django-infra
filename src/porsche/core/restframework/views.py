from typing import override

from rest_framework.views import APIView
from rest_framework.views import exception_handler as exception_handler_

from porsche.core.restframework.request import PorscheRequest


class PorscheAPIView(APIView):
    @override
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        return PorscheRequest.from_request(request)


def exception_handler(exc, context):
    return exception_handler_(exc, context)
