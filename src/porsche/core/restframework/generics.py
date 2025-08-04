# -*- coding: utf-8 -*-
from typing import override

from rest_framework.generics import GenericAPIView


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
                return self.create_serializer_class
            case "retrieve":
                return self.retrieve_serializer_class
            case "list":
                return self.list_serializer_class
            case "update":
                return self.update_serializer_class
            case _:
                return super().get_serializer_class()
