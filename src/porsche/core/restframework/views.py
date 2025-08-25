from typing import override

from rest_framework.views import APIView

from porsche.core.restframework.request import PorscheRequest


class PorscheAPIView(APIView):
    @override
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        return PorscheRequest.from_request(request)
