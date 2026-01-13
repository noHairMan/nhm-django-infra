from typing import Optional

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import ComponentRegistry
from drf_spectacular.utils import _SchemaType


class PorscheAutoSchema(AutoSchema):
    """
    自定义 AutoSchema，确保所有响应都符合 PorscheResponse 的标准格式：
    {
        "code": <业务状态码>,
        "message": <消息提示>,
        "data": <实际数据>
    }
    """

    def get_operation(
        self,
        path: str,
        path_regex: str,
        path_prefix: str,
        method: str,
        registry: ComponentRegistry,
    ) -> Optional[_SchemaType]:
        """
        重写操作生成逻辑，在全局级别处理响应包装
        """
        operation = super().get_operation(path, path_regex, path_prefix, method, registry)

        if not operation:
            return operation

        # 包装所有响应
        if "responses" in operation:
            for status_code, response in operation["responses"].items():
                operation["responses"][status_code] = self._wrap_response(response, registry)

        return operation

    def _wrap_response(self, response, registry):
        """
        在全局 registry 级别包装响应
        """
        if "content" not in response or "application/json" not in response["content"]:
            return response

        # 获取原始 schema
        json_content = response["content"]["application/json"]
        original_schema = json_content.get("schema", {})

        # 构建 PorscheResponse 的外层 schema
        # 使用 $ref 引用一个组件，而不是内联
        porsche_schema = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "description": "业务状态码",
                    "example": 0,
                },
                "message": {
                    "type": "string",
                    "description": "响应消息",
                    "example": "success",
                },
                "data": original_schema
                or {
                    "type": "object",
                    "description": "响应数据",
                },
            },
            "required": ["code", "message", "data"],
        }

        return {
            "description": response.get("description", "Successful response"),
            "content": {
                "application/json": {
                    "schema": porsche_schema,
                },
            },
        }
