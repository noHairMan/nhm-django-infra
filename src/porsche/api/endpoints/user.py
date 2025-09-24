from porsche.api.serializers.user import (
    RoleListSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)
from porsche.core.restframework import PorscheGenericViewSet, PorscheListModelMixin, PorscheModelViewSet
from porsche.models import Role, User


class RoleViewSet(
    PorscheListModelMixin,
    PorscheGenericViewSet,
):
    queryset = Role.objects.all()
    list_serializer_class = RoleListSerializer


class UserViewSet(PorscheModelViewSet):
    queryset = User.objects.all()
    list_serializer_class = UserListSerializer
    retrieve_serializer_class = UserRetrieveSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
