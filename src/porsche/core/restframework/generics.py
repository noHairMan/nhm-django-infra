from typing import Iterable, Optional, override

from django.utils.translation import gettext_lazy
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from porsche.core.restframework.exceptions import PorscheServerException
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.serializer import PorscheSerializer
from porsche.core.restframework.views import PorscheAPIView
from porsche.models.enums import ViewAction


class PorscheGenericAPIView(PorscheAPIView, GenericAPIView):
    headers = {}
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    action: Optional[ViewAction | str] = None
    serializer_class = PorscheSerializer

    search_fields: Optional[Iterable[str]] = None
    ordering: Optional[Iterable[str]] = None

    # Custom
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None

    @override
    def get_serializer_class(self):
        match self.action:
            case ViewAction.METADATA:
                clazz = self.serializer_class
            case ViewAction.LIST:
                clazz = self.list_serializer_class
            case ViewAction.RETRIEVE:
                clazz = self.retrieve_serializer_class
            case ViewAction.CREATE:
                clazz = self.create_serializer_class
            case ViewAction.UPDATE:
                clazz = self.update_serializer_class
            case ViewAction.PARTIAL_UPDATE:
                clazz = self.update_serializer_class
            case _:
                clazz = None

        if not clazz:
            try:
                clazz = super().get_serializer_class()
            except AssertionError:
                clazz = None

        if not clazz:
            raise PorscheServerException("No serializer class found")

        return clazz

    def finalize_response(self, request, response, *args, **kwargs) -> PorscheResponse:
        if not isinstance(response, PorscheResponse) and isinstance(response, Response):
            response = PorscheResponse(data=response.data)
        if not isinstance(response, PorscheResponse):
            raise PorscheServerException(gettext_lazy("Response must be a PorscheResponse instance"))
        return super().finalize_response(request, response, *args, **kwargs)
