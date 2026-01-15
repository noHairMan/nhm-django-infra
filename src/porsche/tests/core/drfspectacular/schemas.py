import yaml
from rest_framework.reverse import reverse

from porsche.core.restframework.test import PorscheAPITestCase


class TestSchemas(PorscheAPITestCase):
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
