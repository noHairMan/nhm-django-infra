from typing import override

from rest_framework.pagination import CursorPagination, PageNumberPagination

from porsche.core.restframework.response import PorscheResponse
from porsche.models.enums import BusinessCode


class PorschePageNumberPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 100

    @override
    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["count", "results"],
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                self.page_query_param: {
                    "type": "integer",
                    "example": 2,
                },
                self.page_size_query_param: {
                    "type": "integer",
                    "example": 50,
                },
                "results": schema,
            },
        }

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        return PorscheResponse(
            data={
                "count": response.data["count"],
                self.page_query_param: self.page.number,
                self.page_size_query_param: self.get_page_size(self.request),
                "results": response.data["results"],
            },
            code=BusinessCode.SUCCESS,
        )


class PorscheLimitOffsetPagination(PageNumberPagination):
    limit_query_param = "limit"
    offset_query_param = "offset"


class PorscheCursorPagination(CursorPagination):
    max_page_size = 100
    page_size_query_param = "size"
    ordering = "-create_time"
