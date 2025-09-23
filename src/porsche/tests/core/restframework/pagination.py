from porsche.core.restframework import (
    PorscheAPITestCase,
    PorschePageNumberPagination,
    PorscheRequest,
    PorscheResponse,
)
from porsche.models import Tag


class TestPaginator(PorscheAPITestCase):
    def setUp(self):
        Tag.objects.bulk_create([Tag(name=f"tag_{i}", category=Tag.Category.COMPANY) for i in range(100)])

    def test_porsche_page_number_pagination(self):
        paginator = PorschePageNumberPagination()
        self.assertEqual(
            paginator.get_paginated_response_schema({}),
            {
                "type": "object",
                "required": ["count", "results"],
                "properties": {
                    "count": {"type": "integer", "example": 123},
                    "page": {"type": "integer", "example": 2},
                    "size": {"type": "integer", "example": 50},
                    "results": {},
                },
            },
        )
        request = PorscheRequest(self.request_factory.get("/api/tag?page=1&size=10"))
        paginator.paginate_queryset(Tag.objects.all(), request, view=None)
        response = paginator.get_paginated_response({})
        self.assertIsInstance(response, PorscheResponse)
        self.assertEqual(response.data["data"], {"count": 100, "page": 1, "size": 10, "results": {}})
