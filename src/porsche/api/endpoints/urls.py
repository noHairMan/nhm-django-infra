from django.urls import path

from porsche.api.endpoints.health import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
