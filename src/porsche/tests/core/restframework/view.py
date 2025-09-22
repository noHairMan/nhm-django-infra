from pyexpat.errors import messages

import ujson
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException, _get_error_details

from porsche.core.restframework.exceptions import PorscheAPIException
from porsche.core.restframework.request import PorscheRequest
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.test import PorscheAPITestCase
from porsche.core.restframework.views import PorscheAPIView, exception_handler
from porsche.models.enums import BusinessCode


class TestView(PorscheAPITestCase):
    def setUp(self):
        self.view = PorscheAPIView()

    def test_initialize_request(self):
        request = self.request_factory.get("/api/health/")
        self.assertIsInstance(self.view.initialize_request(request), PorscheRequest)

    @staticmethod
    def exception_handler(exception: Exception, context: dict) -> PorscheResponse:
        try:
            raise exception
        except Exception as error:
            return exception_handler(error, context)

    def test_exception_handler(self):
        response = self.exception_handler(Http404(), {})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.business_code, BusinessCode.BAD_REQUEST)

        exc = APIException("Test Error")
        exc.auth_header = "Bearer"
        exc.wait = 10000
        response = self.exception_handler(exc, {})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.business_code, BusinessCode.BAD_REQUEST)
        self.assertEqual(response.headers["WWW-Authenticate"], exc.auth_header)
        self.assertEqual(response.headers["Retry-After"], str(exc.wait))

        response = self.exception_handler(DjangoPermissionDenied(), {})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.business_code, BusinessCode.BAD_REQUEST)

        message = {"foo": "bar", "code": 123, "message": "test error"}
        response = self.exception_handler(PorscheAPIException(message), {})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.business_code, BusinessCode.BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            ujson.dumps(_get_error_details(message), ensure_ascii=False, escape_forward_slashes=False),
        )

        response = self.exception_handler(Exception("测试异常handler"), {})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.business_code, BusinessCode.SERVER_ERROR)
