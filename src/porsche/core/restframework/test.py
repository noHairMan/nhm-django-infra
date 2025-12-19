from functools import lru_cache

from cacheops import invalidate_all
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    APITestCase,
    ForceAuthClientHandler,
    RequestsClient,
)

from porsche.core.django.db.models import get_object
from porsche.models import Role, User


class PorscheAPIRequestFactory(APIRequestFactory):
    pass


class PorscheForceAuthClientHandler(ForceAuthClientHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        invalidate_all()

        self._force_user, _ = User.objects.get_or_create(
            username="sdet",
            email="sdet@fortest.cn",
            phone="88888888888",
            password="fake_password",
            role=get_object(Role, category=Role.Category.BUILTIN, name=Role.BuiltInName.USER),
        )
        self._force_token = None


class PorscheAPIClient(APIClient):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks, **defaults)
        self.handler = PorscheForceAuthClientHandler(enforce_csrf_checks)

    @property
    def session(self):
        return None


class PorscheGenericTestCase:
    request_client_class = RequestsClient
    client_class = PorscheAPIClient
    request_factory_class = PorscheAPIRequestFactory

    client: PorscheAPIClient

    @property
    @lru_cache
    def request_factory(self) -> PorscheAPIRequestFactory:
        return self.request_factory_class()

    @property
    @lru_cache
    def request_client(self) -> RequestsClient:
        return self.request_client_class()


class PorscheAPITestCase(PorscheGenericTestCase, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        invalidate_all()

    def setUp(self):
        super().setUp()
        invalidate_all()
