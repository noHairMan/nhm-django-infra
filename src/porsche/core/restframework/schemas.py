from rest_framework.schemas.openapi import AutoSchema


class PorscheAutoSchema(AutoSchema):
    def get_responses(self, path, method):
        responses = super().get_responses(path, method)
        wrapped_responses = {}
        for status_code, response in responses.items():
            wrapped_responses[status_code] = {
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
        return wrapped_responses
