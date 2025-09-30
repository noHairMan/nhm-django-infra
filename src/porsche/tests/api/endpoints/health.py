from django.conf import settings

from porsche.core.restframework.test import PorscheAPITestCase
from porsche.models.enums import BusinessCode


class TestHealthCheckView(PorscheAPITestCase):
    def test_get(self):
        self.client.logout()
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["code"], BusinessCode.SUCCESS)
        data = result["data"]
        self.assertEqual(data["app"], settings.APP)
        self.assertEqual(data["version"], settings.VERSION)
