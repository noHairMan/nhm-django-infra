import re
from typing import Optional, override

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import ComponentRegistry
from drf_spectacular.settings import spectacular_settings
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
        def build_porsche_schema():
            # 使用 oneOf 来定义 data 字段可以是 null 或 object
            data_type = {
                "oneOf": [
                    {"type": "null"},
                    original_schema,
                ],
            }

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
                    "data": data_type,
                },
                "required": ["code", "message", "data"],
            }

        if "content" not in response or "application/json" not in response["content"]:
            # 没有 content 时使用默认结构
            original_schema = {
                "type": "object",
                "description": "响应数据",
            }
            porsche_schema = build_porsche_schema()
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
        porsche_schema = build_porsche_schema()

        return {
            "description": response.get("description", "Successful response"),
            "content": {
                "application/json": {
                    "schema": porsche_schema,
                },
            },
        }

    @override
    def get_operation_id(self) -> str:
        """override this for custom behaviour"""
        tokenized_path = self._tokenize_path()
        # replace dashes as they can be problematic later in code generation
        tokenized_path = [t.replace("-", "_") for t in tokenized_path]

        action = self.view.action

        if not tokenized_path:
            tokenized_path.append("root")

        if re.search(r"<drf_format_suffix\w*:\w+>", self.path_regex):
            tokenized_path.append("formatted")

        if spectacular_settings.OPERATION_ID_METHOD_POSITION == "PRE":
            return "_".join([action] + tokenized_path)
        elif spectacular_settings.OPERATION_ID_METHOD_POSITION == "POST":
            return "_".join(tokenized_path + [action])
        else:
            assert False, "Invalid value for OPERATION_ID_METHOD_POSITION. Allowed: PRE, POST"
