from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from porsche.api.endpoints import *
from porsche.core.restframework import PorscheRouter

router = PorscheRouter()
router.register("company", CompanyViewSet, basename="company")
router.register("tag", TagViewSet, basename="tag")
router.register("user", UserViewSet, basename="user")
router.register("role", RoleViewSet, basename="role")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(router.urls)),
]
