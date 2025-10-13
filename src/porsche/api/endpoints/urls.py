from django.urls import include, path

from porsche.api.endpoints import *
from porsche.core.restframework import PorscheRouter

router = PorscheRouter()
router.register("company", CompanyViewSet, basename="company")
router.register("tag", TagViewSet, basename="tag")
router.register("user", UserViewSet, basename="user")
router.register("role", RoleViewSet, basename="role")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("", include(router.urls)),
]
