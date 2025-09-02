from django.urls import include, path

from porsche.api.endpoints.company import CompanyViewSet
from porsche.api.endpoints.health import HealthCheckView
from porsche.api.endpoints.tag import TagViewSet
from porsche.core.restframework import PorscheRouter

router = PorscheRouter()
router.register("company", CompanyViewSet, basename="company")
router.register("tag", TagViewSet, basename="tag")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("", include(router.urls)),
]
