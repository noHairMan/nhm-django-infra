from django.conf import settings

from porsche.api.serializers.health import HealthCheckResponseSerializer
from porsche.core.restframework import PorscheGenericAPIView
from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse


class HealthCheckView(PorscheGenericAPIView):
    permission_classes = ()
    action = "retrieve"
    serializer_class = HealthCheckResponseSerializer

    def get(self, request: PorscheRequest):
        serializer = self.get_serializer(
            data={
                "app": settings.APP,
                "version": settings.VERSION,
            },
        )
        serializer.is_valid(raise_exception=True)
        return PorscheResponse(serializer.validated_data)
