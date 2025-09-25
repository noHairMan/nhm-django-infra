from django.contrib.auth.hashers import make_password

from porsche.api.serializers.user import RoleListSerializer, UserCreateSerializer
from porsche.core.django.db.models import get_object
from porsche.core.restframework import PorscheAPITestCase
from porsche.models import Role


class TestSerializerUser(PorscheAPITestCase):
    def test_role(self):
        queryset = Role.objects.all()
        list_serializer = RoleListSerializer(instance=queryset, many=True)
        self.assertEqual(len(list_serializer.data), queryset.count())
        for field in RoleListSerializer.Meta.fields:
            self.assertIn(field, list_serializer.data[0])

    def test_user(self):
        password = "SqrIqJqhuVerHa"
        serializer = UserCreateSerializer(
            data={
                "username": "test",
                "password": password,
                "email": "test@test.com",
                "phone": "12345678902",
                "role": get_object(Role, name="user").uid,
            },
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertTrue(user.check_password(password))
