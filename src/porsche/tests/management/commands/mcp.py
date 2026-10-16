import asyncio
import logging
import socket
import sys
import threading
import time
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import MagicMock, patch

import httpx
from django.core.management import call_command

from porsche.core.restframework import PorscheAPITestCase
from porsche.management.commands.mcp import Command


class TestMcp(PorscheAPITestCase):
    def test_handle_starts_fastmcp_server(self):
        fastmcp = MagicMock()
        generator = MagicMock()
        generator_instance = MagicMock()
        generator.return_value = generator_instance
        generator_instance.get_schema.return_value = {"openapi": "3.1.0"}

        with (
            patch.dict(sys.modules, {"fastmcp": fastmcp}),
            patch("porsche.management.commands.mcp.logging.config.dictConfig"),
            patch("porsche.management.commands.mcp.spectacular_settings.DEFAULT_GENERATOR_CLASS", generator),
            patch("porsche.management.commands.mcp.spectacular_settings.SERVE_PUBLIC", True),
            patch("porsche.management.commands.mcp.settings.LOG_LEVEL", "INFO"),
            patch("porsche.management.commands.mcp.httpx.AsyncClient") as async_client,
        ):
            Command().handle(base_url="http://example.test", api_version="v1", port=3002)

        generator.assert_called_once_with(api_version="v1")
        generator_instance.get_schema.assert_called_once_with(public=True)
        fastmcp.FastMCP.from_openapi.assert_called_once()
        fastmcp.FastMCP.from_openapi.return_value.run.assert_called_once_with(
            transport="streamable-http",
            host="0.0.0.0",
            port=3002,
        )
        async_client.assert_called_once_with(base_url="http://example.test")

    @staticmethod
    def _is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) != 0

    @staticmethod
    async def _check_process_health(thread):
        return thread.is_alive()

    async def _wait_for_fastmcp_service(self, base_url, process, timeout=20, interval=1.0):
        start_time = time.time()
        endpoints_to_check = ["/"]
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("mcp").setLevel(logging.WARNING)

        while time.time() - start_time < timeout:
            if not await self._check_process_health(process):
                return False, None, "进程已退出"

            for endpoint in endpoints_to_check:
                try:
                    url = f"{base_url}{endpoint}"
                    httpx.get(url, timeout=3.0)
                    return True, endpoint, None
                except (httpx.RequestError, httpx.ConnectError, httpx.TimeoutException) as e:
                    continue

            await asyncio.sleep(interval)

        return False, None, "超时"

    async def test_command_default_settings(self):
        command = Command()
        parser = command.create_parser("manage.py", "mcp")
        args = parser.parse_args([])
        self.assertEqual(args.port, 3002)
        self.assertEqual(args.base_url, "http://localhost:8000")
        args = parser.parse_args(["--port", "3003"])
        self.assertEqual(args.port, 3003)
        args = parser.parse_args(["--base_url", "http://example.com"])
        self.assertEqual(args.base_url, "http://example.com")

        port = 3003
        if not self._is_port_available(port):
            self.skipTest(f"Port {port} is not available")
        base_url = "http://localhost:8000"

        # 使用context manager重定向输出，抑制FastMCP日志
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            thread = threading.Thread(
                target=call_command,
                args=("mcp",),
                kwargs={"port": port, "base_url": base_url, "verbosity": 0},
            )
            thread.daemon = True
            thread.start()

            service_url = f"http://localhost:{port}"
            service_started, working_endpoint, error_msg = await self._wait_for_fastmcp_service(service_url, thread)

            if not service_started:
                if await self._check_process_health(thread):
                    self.fail(f"FastMCP服务启动失败: {error_msg} at {service_url}")

            if thread.is_alive():
                thread.join(timeout=5.0)
