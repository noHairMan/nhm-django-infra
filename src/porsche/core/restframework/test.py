from functools import lru_cache

from rest_framework.test import (
    APIClient,
    APILiveServerTestCase,
    APIRequestFactory,
    APISimpleTestCase,
    APITestCase,
    APITransactionTestCase,
    ForceAuthClientHandler,
    URLPatternsTestCase,
)

from porsche.core.django.db.models import get_object
from porsche.models import Role, User


class PorscheAPIRequestFactory(APIRequestFactory):
    pass


class PorscheForceAuthClientHandler(ForceAuthClientHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    client_class = PorscheAPIClient
    client: PorscheAPIClient
    request_factory_class = PorscheAPIRequestFactory

    @property
    @lru_cache
    def request_factory(self) -> PorscheAPIRequestFactory:
        return self.request_factory_class()


class PorscheAPITransactionTestCase(APITransactionTestCase, PorscheGenericTestCase):
    pass


class PorscheAPITestCase(PorscheGenericTestCase, APITestCase):
    pass


class PorscheAPISimpleTestCase(APISimpleTestCase, PorscheGenericTestCase):
    pass


class PorscheAPILiveServerTestCase(APILiveServerTestCase, PorscheGenericTestCase):
    pass


class PorscheURLPatternsTestCase(URLPatternsTestCase):
    pass
