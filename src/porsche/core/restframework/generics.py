# -*- coding: utf-8 -*-
from typing import override

from rest_framework.generics import GenericAPIView

from porsche.core.restframework.exceptions import PorscheServerException


class PorscheGenericAPIView(GenericAPIView):
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    serializer_class = None
    create_serializer_class = None
    update_serializer_class = None
    list_serializer_class = None
    retrieve_serializer_class = None

    @override
    def get_serializer_class(self):
        match self.action:
            case "create":
                clazz = self.create_serializer_class
            case "retrieve":
                clazz = self.retrieve_serializer_class
            case "list":
                clazz = self.list_serializer_class
            case "update":
                clazz = self.update_serializer_class
            case _:
                clazz = super().get_serializer_class()

        if not clazz:
            clazz = self.serializer_class

        if not clazz:
            raise PorscheServerException("No serializer class found")

        return clazz
