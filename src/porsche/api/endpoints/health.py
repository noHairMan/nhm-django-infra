from django.conf import settings

from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.views import PorscheAPIView


class HealthCheckView(PorscheAPIView):
    """
    Handles the health check functionality for the application.

    This class provides API endpoints to check the health and operational
    status of the service. Clients can query this endpoint to ensure the
    service is running and available.
    """

    def get(self, request: PorscheRequest):
        return PorscheResponse(
            {
                "app": settings.APP,
                "version": settings.VERSION,
            },
        )
