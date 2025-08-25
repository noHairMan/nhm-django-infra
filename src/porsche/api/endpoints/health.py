from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.views import PorscheAPIView


class HealthCheckView(PorscheAPIView):
    def get(self, request: PorscheRequest):
        return PorscheResponse({"status": "ok"})
