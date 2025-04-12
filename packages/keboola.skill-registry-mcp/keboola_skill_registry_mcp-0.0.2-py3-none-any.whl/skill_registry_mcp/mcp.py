""""""

import logging
from typing import Any

from mcp import stdio_server
from mcp.server import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.types import Tool as MCPTool

from keboola.skill_registry_mcp.sr_tools import SRToolManager

logger = logging.getLogger(__name__)


class KeboolaSkillRegistryMcpServer(FastMCP):

    def __init__(
        self,
        name: str | None = None,
        instructions: str | None = None,
        *,
        sr_manager: SRToolManager = None,
        **settings: Any,
    ) -> None:
        super().__init__(name, instructions, **settings)
        self._tool_manager = sr_manager

    async def list_tools(self) -> list[MCPTool]:
        """List all available tools."""
        return self._tool_manager.list_tools()

    async def run_stdio_async(self) -> None:
        """Run the server using stdio transport."""
        async with stdio_server() as (read_stream, write_stream):
            await self._mcp_server.run(
                read_stream,
                write_stream,
                initialization_options=self._mcp_server.create_initialization_options(),
                raise_exceptions=True,
            )

    async def run_sse_async(self) -> None:
        """Run the server using SSE transport."""
        import uvicorn
        from starlette.applications import Starlette
        from starlette.requests import Request
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request: Request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await self._mcp_server.run(
                    streams[0],
                    streams[1],
                    initialization_options=self._mcp_server.create_initialization_options(),
                )

        starlette_app = Starlette(
            debug=self.settings.debug,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
                # TODO: add endpoints for health-check and info
            ],
        )

        config = uvicorn.Config(
            starlette_app,
            host=self.settings.host,
            port=self.settings.port,
            log_level=self.settings.log_level.lower(),
        )
        server = uvicorn.Server(config)
        await server.serve()
