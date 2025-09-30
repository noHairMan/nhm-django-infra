from rest_framework.test import RequestsClient

from porsche.core.restframework import PorscheAPIRequestFactory, PorscheAPITestCase


class TestRestFrameworkTest(PorscheAPITestCase):
    def test_porsche_generic_test_case(self):
        self.assertIsInstance(self.request_factory, PorscheAPIRequestFactory)
        self.assertIsInstance(self.request_client, RequestsClient)
