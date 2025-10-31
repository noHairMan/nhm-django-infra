from django.db import IntegrityError

from porsche.core.restframework.test import PorscheAPITestCase
from porsche.models import Role, User


class TestUser(PorscheAPITestCase):
    def test_user(self):
        role = Role.objects.create(name=Role.BuiltInName.ADMIN, category=Role.Category.BUILTIN, description="fortest")
        user = User.objects.create_superuser(username="admin", email="", password="", role=role.uid)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.role, role)

        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(username="user", email="", password="")
