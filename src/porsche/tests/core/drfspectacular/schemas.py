from types import SimpleNamespace
from unittest.mock import patch

import yaml
from rest_framework.reverse import reverse

from porsche.core.drfspectacular.schemas import PorscheAutoSchema
from porsche.core.restframework.test import PorscheAPITestCase


class TestSchemas(PorscheAPITestCase):
    def test_operation_without_responses_is_returned_unchanged(self):
        schema = PorscheAutoSchema()
        operation = {"operationId": "items_list"}

        with patch("drf_spectacular.openapi.AutoSchema.get_operation", return_value=operation):
            result = schema.get_operation("/items/", "^items/$", "", "GET", None)

        self.assertIs(result, operation)

    def test_operation_id_root_and_pre_position(self):
        schema = PorscheAutoSchema()
        schema.view = SimpleNamespace(action="list")
        schema.path_regex = "^/$"

        with (
            patch.object(schema, "_tokenize_path", return_value=[]),
            patch(
                "porsche.core.drfspectacular.schemas.spectacular_settings.OPERATION_ID_METHOD_POSITION",
                "PRE",
            ),
        ):
            self.assertEqual(schema.get_operation_id(), "list_root")

    def test_operation_id_formatted_post_position(self):
        schema = PorscheAutoSchema()
        schema.view = SimpleNamespace(action="retrieve")
        schema.path_regex = "^items<drf_format_suffix:format>$"

        with (
            patch.object(schema, "_tokenize_path", return_value=["items-item"]),
            patch(
                "porsche.core.drfspectacular.schemas.spectacular_settings.OPERATION_ID_METHOD_POSITION",
                "POST",
            ),
        ):
            self.assertEqual(schema.get_operation_id(), "items_item_formatted_retrieve")

    def test_operation_id_rejects_invalid_method_position(self):
        schema = PorscheAutoSchema()
        schema.view = SimpleNamespace(action="list")
        schema.path_regex = "^items/$"

        with (
            patch.object(schema, "_tokenize_path", return_value=["items"]),
            patch(
                "porsche.core.drfspectacular.schemas.spectacular_settings.OPERATION_ID_METHOD_POSITION",
                "INVALID",
            ),
            self.assertRaises(AssertionError),
        ):
            schema.get_operation_id()

    @staticmethod
    def _validate_response_schema(schema):
        if not isinstance(schema, dict):
            return False
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        return (
            "code" in properties
            and "message" in properties
            and "data" in properties
            and all(field in required for field in ["code", "message", "data"])
        )

    def test_porsche_auto_schema(self):
        response = self.client.get(reverse("schema"))
        openapi_spec = yaml.safe_load(response.content)

        # Validate OpenAPI spec structure
        self.assertIn("openapi", openapi_spec)
        self.assertEqual(openapi_spec["openapi"], "3.1.0")
        self.assertIn("paths", openapi_spec)

        # Validate each endpoint response
        for path, methods in openapi_spec["paths"].items():
            for method, operation in methods.items():
                if method.lower() == "parameters":
                    continue
                responses = operation.get("responses", {})
                for status_code, response in responses.items():
                    content = response.get("content", {}).get("application/json", {})
                    schema = content.get("schema", {})
                    self.assertTrue(
                        self._validate_response_schema(schema),
                        f"Invalid response schema for {method.upper()} {path} {status_code}",
                    )
