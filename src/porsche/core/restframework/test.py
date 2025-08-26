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


class PorscheAPITransactionTestCase(APITransactionTestCase):
    client_class = PorscheAPIClient


class PorscheAPITestCase(APITestCase):
    client_class = PorscheAPIClient


class PorscheAPISimpleTestCase(APISimpleTestCase):
    client_class = PorscheAPIClient


class PorscheAPILiveServerTestCase(APILiveServerTestCase):
    client_class = PorscheAPIClient


class PorscheURLPatternsTestCase(URLPatternsTestCase):
    pass
