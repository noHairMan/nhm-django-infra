from typing import Any

from rest_framework.response import Response

from porsche.core.restframework import (
    PorscheAPITestCase,
    PorscheGenericAPIView,
    PorscheResponse,
    PorscheSerializer,
    PorscheServerException,
)
from porsche.models.enums import ViewAction


class TestGeneric(PorscheAPITestCase):
    def test_porsche_generic_api_view(self):
        class CreateSerializer(PorscheSerializer):
            pass

        class UpdateSerializer(PorscheSerializer):
            pass

        class RetrieveSerializer(PorscheSerializer):
            pass

        class ListSerializer(PorscheSerializer):
            pass

        class TestViewSet(PorscheGenericAPIView):
            create_serializer_class = CreateSerializer
            update_serializer_class = UpdateSerializer
            retrieve_serializer_class = RetrieveSerializer
            list_serializer_class = ListSerializer

        request = self.request_factory.get("test")
        self.assertEqual(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.CREATE).get_serializer_class(),
            CreateSerializer,
        )
        self.assertEqual(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.UPDATE).get_serializer_class(),
            UpdateSerializer,
        )
        self.assertEqual(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.RETRIEVE).get_serializer_class(),
            RetrieveSerializer,
        )
        self.assertEqual(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.LIST).get_serializer_class(),
            ListSerializer,
        )
        self.assertEqual(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.METADATA).get_serializer_class(),
            PorscheSerializer,
        )

        self.assertIsInstance(
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.METADATA).finalize_response(
                request,
                Response(),
            ),
            PorscheResponse,
        )
        with self.assertRaises(PorscheServerException):
            TestViewSet(request=request, format_kwarg={}, action=ViewAction.METADATA).finalize_response(request, Any)
