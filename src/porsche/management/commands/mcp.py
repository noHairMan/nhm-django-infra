import httpx
from django.conf import settings
from django.core.management.base import BaseCommand
from drf_spectacular.settings import spectacular_settings
from fastmcp import FastMCP


class Command(BaseCommand):
    # can use `npx @modelcontextprotocol/inspector uv run` for test
    help = "Run MCP server"

    def add_arguments(self, parser):
        parser.add_argument(
            "--base_url",
            dest="base_url",
            default="http://localhost:8000",
            type=str,
            help="backend server url",
        )
        parser.add_argument(
            "--port",
            dest="port",
            default=3002,
            type=int,
            help="mcp server port",
        )
        parser.add_argument(
            "--api_version",
            dest="api_version",
            default=settings.REST_FRAMEWORK["DEFAULT_VERSION"],
            type=str,
            help="mcp server api version",
        )

    def handle(self, *args, **options):
        generator = spectacular_settings.DEFAULT_GENERATOR_CLASS(api_version=options["api_version"])
        openapi_spec = generator.get_schema(public=spectacular_settings.SERVE_PUBLIC)
        client = httpx.AsyncClient(base_url=options["base_url"])
        mcp = FastMCP.from_openapi(openapi_spec=openapi_spec, client=client, name="MCP Server")
        mcp.run(transport="streamable-http", host="0.0.0.0", port=options["port"])
