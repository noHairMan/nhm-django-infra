from typing import Optional

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import ComponentRegistry
from drf_spectacular.utils import _SchemaType


class PorscheAutoSchema(AutoSchema):
    def get_operation(
        self,
        path: str,
        path_regex: str,
        path_prefix: str,
        method: str,
        registry: ComponentRegistry,
    ) -> Optional[_SchemaType]:
        operation = super().get_operation(path, path_regex, path_prefix, method, registry)
        if not operation or "responses" not in operation:
            return operation
        for status_code, response in operation["responses"].items():
            operation["responses"][status_code] = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer"},
                                "message": {"type": "string"},
                                "data": response.get("content", {}).get("application/json", {}).get("schema", {}),
                            },
                            "required": ["code", "message", "data"],
                        },
                    },
                },
                "description": response.get("content", {}).get("application/json", {}).get("description", ""),
            }
        return operation
