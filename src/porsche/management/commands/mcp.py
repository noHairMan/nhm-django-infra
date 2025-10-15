import pathlib
import tempfile

import httpx
import ujson
from django.core.management import call_command
from django.core.management.base import BaseCommand
from fastmcp import FastMCP


class Command(BaseCommand):
    # can user `npx @modelcontextprotocol/inspector uv run` for test
    help = "Run MCP server"

    def add_arguments(self, parser):
        parser.add_argument(
            "--base_url",
            dest="base_url",
            default="http://localhost:8000",
            type=str,
            help="backend server url",
        )

    def handle(self, *args, **options):
        with tempfile.TemporaryDirectory() as tmpdir:
            schema_file = pathlib.Path(tmpdir) / "schema.json"
            call_command("generateschema", format="openapi-json", file=schema_file)
            openapi_spec = ujson.load(open(schema_file))
        client = httpx.AsyncClient(base_url=options["base_url"])
        mcp = FastMCP.from_openapi(openapi_spec=openapi_spec, client=client, name="MCP Server")
        mcp.run(transport="streamable-http", host="0.0.0.0", port=3002)
