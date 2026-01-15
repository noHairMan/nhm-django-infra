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
        此模块提供将原始 OpenAPI 响应包装为
        PorscheResponse 格式的工具函数。

        功能包括：
        - 检查并过滤非 JSON 类型的响应
        - 依据原始响应构造统一的业务码、消息和数据字段
        - 将构造好的 schema 以组件引用形式嵌入
        """

        # 提取构建 schema 的通用逻辑
        def build_porsche_schema(use_original_schema: bool):
            data_schema = (
                original_schema
                if use_original_schema
                else {
                    "type": "object",
                    "description": "响应数据",
                }
            )
            return {
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
                    "data": data_schema,
                },
                "required": ["code", "message", "data"],
            }

        if "content" not in response or "application/json" not in response["content"]:
            # 没有 content 时使用默认结构
            original_schema = {}
            porsche_schema = build_porsche_schema(False)
            return {
                "description": response.get("description", "Successful response"),
                "content": {
                    "application/json": {
                        "schema": porsche_schema,
                    },
                },
            }

        # 存在 content 时使用原始 schema
        json_content = response["content"]["application/json"]
        original_schema = json_content.get("schema", {})
        porsche_schema = build_porsche_schema(True)

        return {
            "description": response.get("description", "Successful response"),
            "content": {
                "application/json": {
                    "schema": porsche_schema,
                },
            },
        }
