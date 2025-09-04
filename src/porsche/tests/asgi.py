from django.core.handlers.asgi import ASGIHandler

from porsche.asgi import application
from porsche.core.restframework.test import PorscheAPITestCase


class TestASGIApplication(PorscheAPITestCase):
    def test_application(self):
        self.assertIsInstance(application, ASGIHandler)
