# -*- coding: utf-8 -*-
from typing import Literal, Optional, override

from rest_framework.generics import GenericAPIView

from porsche.core.restframework.exceptions import PorscheServerException
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.views import PorscheAPIView

__all__ = [
    "PorscheGenericAPIView",
]


class PorscheGenericAPIView(PorscheAPIView, GenericAPIView):
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    action: Optional[Literal["create", "retrieve", "list", "update"]] = None
    serializer_class = None

    # Custom
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None

    @override
    def get_serializer_class(self):
        match self.action:
            case "metadata":
                clazz = self.list_serializer_class
            case "list":
                clazz = self.list_serializer_class
            case "retrieve":
                clazz = self.retrieve_serializer_class
            case "create":
                clazz = self.create_serializer_class
            case "update":
                clazz = self.update_serializer_class
            case _:
                clazz = super().get_serializer_class()

        if not clazz:
            clazz = self.serializer_class

        if not clazz:
            raise PorscheServerException("No serializer class found")

        return clazz

    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response, PorscheResponse):
            response = PorscheResponse(data=response.data)
        return super().finalize_response(request, response, *args, **kwargs)
