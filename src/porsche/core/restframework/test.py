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


class PorscheAPIRequestFactory(APIRequestFactory):
    pass


class PorscheForceAuthClientHandler(ForceAuthClientHandler):
    pass


class PorscheAPIClient(APIClient):
    pass


class PorscheGenericTestCase:
    client_class = PorscheAPIClient
    request_factory_class = PorscheAPIRequestFactory

    @property
    @lru_cache
    def request_factory(self):
        return self.request_factory_class()


class PorscheAPITransactionTestCase(APITransactionTestCase, PorscheGenericTestCase):
    pass


class PorscheAPITestCase(APITestCase, PorscheGenericTestCase):
    pass


class PorscheAPISimpleTestCase(APISimpleTestCase, PorscheGenericTestCase):
    pass


class PorscheAPILiveServerTestCase(APILiveServerTestCase, PorscheGenericTestCase):
    pass


class PorscheURLPatternsTestCase(URLPatternsTestCase):
    pass
