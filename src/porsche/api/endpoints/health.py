from django.conf import settings

from porsche.core.restframework import PorscheGenericAPIView
from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse


class HealthCheckView(PorscheGenericAPIView):
    permission_classes = ()

    @staticmethod
    def get(request: PorscheRequest):
        return PorscheResponse(
            {
                "app": settings.APP,
                "version": settings.VERSION,
            },
        )
