import json
import anyio

import logging
from collections.abc import Sequence
from functools import lru_cache
from typing import Any, Dict
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

load_dotenv()

# Import the specific classes needed
from .obsidian import Obsidian
from . import tools
# Load environment variables

# Configure logging
# TODO: Consider more advanced logging configuration (e.g., JSON formatter) if needed for production monitoring.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-obsidian")

# --- Obsidian Client Configuration & Instantiation ---

# Environment variable names
OBSIDIAN_API_KEY_ENV = "OBSIDIAN_API_KEY"
OBSIDIAN_PROTOCOL_ENV = "OBSIDIAN_PROTOCOL"
OBSIDIAN_HOST_ENV = "OBSIDIAN_HOST"
OBSIDIAN_PORT_ENV = "OBSIDIAN_PORT"
OBSIDIAN_VERIFY_SSL_ENV = "OBSIDIAN_VERIFY_SSL"

api_key = os.getenv(OBSIDIAN_API_KEY_ENV)
if not api_key:
    raise ValueError(f"{OBSIDIAN_API_KEY_ENV} environment variable required. Working directory: {os.getcwd()}")

obsidian_protocol = os.getenv(OBSIDIAN_PROTOCOL_ENV, "http")
obsidian_host = os.getenv(OBSIDIAN_HOST_ENV, "127.0.0.1")
obsidian_port = int(os.getenv(OBSIDIAN_PORT_ENV, "27124")) # Default Obsidian local REST API port
obsidian_verify_ssl = os.getenv(OBSIDIAN_VERIFY_SSL_ENV, "false").lower() == "true"

@lru_cache(maxsize=1)
def get_obsidian_client() -> Obsidian:
    """Initializes and returns a singleton Obsidian client instance."""
    logger.info(f"Initializing Obsidian client for {obsidian_protocol}://{obsidian_host}:{obsidian_port}")
    return Obsidian(
        api_key=api_key,
        protocol=obsidian_protocol,
        host=obsidian_host,
        port=obsidian_port,
        verify_ssl=obsidian_verify_ssl
    )

# --- MCP Server Setup ---

app = Server("mcp-obsidian-remote")

tool_handlers = {}
def add_tool_handler(tool_handler_instance: tools.ToolHandler):
    """Adds an initialized tool handler instance to the registry."""
    global tool_handlers
    if tool_handler_instance.name in tool_handlers:
        logger.warning(f"Overwriting tool handler for {tool_handler_instance.name}")
    tool_handlers[tool_handler_instance.name] = tool_handler_instance

def get_tool_handler(name: str) -> tools.ToolHandler | None:
    if name not in tool_handlers:
        return None

    return tool_handlers[name]

# Instantiate handlers, passing the client instance
obsidian_client = get_obsidian_client()
add_tool_handler(tools.ListFilesInDirToolHandler(obsidian_client))
add_tool_handler(tools.ListFilesInVaultToolHandler(obsidian_client))
add_tool_handler(tools.GetFileContentsToolHandler(obsidian_client))
add_tool_handler(tools.SearchToolHandler(obsidian_client))
add_tool_handler(tools.PatchContentToolHandler(obsidian_client))
add_tool_handler(tools.AppendContentToolHandler(obsidian_client))
add_tool_handler(tools.DeleteFileToolHandler(obsidian_client))
add_tool_handler(tools.ComplexSearchToolHandler(obsidian_client))
add_tool_handler(tools.BatchGetFileContentsToolHandler(obsidian_client))
add_tool_handler(tools.PeriodicNotesToolHandler(obsidian_client))
add_tool_handler(tools.RecentPeriodicNotesToolHandler(obsidian_client))
add_tool_handler(tools.RecentChangesToolHandler(obsidian_client))

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""

    return [th.get_tool_description() for th in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for command line run."""

    if not isinstance(arguments, dict):
        raise RuntimeError("arguments must be dictionary")


    tool_handler = get_tool_handler(name)
    if not tool_handler:
        raise ValueError(f"Unknown tool: {name}")

    try:
        # The handler already has the client instance
        return await tool_handler.run_tool(arguments)
    except Exception as e:
        logger.exception(f"Error executing tool '{name}' with args {arguments}") # Log full traceback
        raise e # Re-raise the original exception


def main(port: int=3031, transport: str='sse'):
    """MCP Obsidian Remote Server entry point."""
    # Import here to avoid issues with event loops

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)

    else:

        from mcp.server.stdio import stdio_server
        options = app.create_initialization_options()

        async def arun():

            async with stdio_server() as (read_stream, write_stream):
                await app.run(
                    read_stream,
                    write_stream,
                    options,
                    raise_exceptions=True
                )

        anyio.run(arun)
