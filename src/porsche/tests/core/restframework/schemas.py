import pathlib
import tempfile

import ujson
from django.core.management import call_command

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
        with tempfile.TemporaryDirectory() as tmpdir:
            schema_file = pathlib.Path(tmpdir) / "schema.json"
            call_command("generateschema", format="openapi-json", file=schema_file)
            openapi_spec = ujson.load(open(schema_file))

            # Validate OpenAPI spec structure
            self.assertIn("openapi", openapi_spec)
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
