from django.core.handlers.wsgi import WSGIHandler

from porsche.core.restframework.test import PorscheAPITestCase
from porsche.wsgi import application


class TestWSGIApplication(PorscheAPITestCase):
    def test_application(self):
        self.assertIsInstance(application, WSGIHandler)
