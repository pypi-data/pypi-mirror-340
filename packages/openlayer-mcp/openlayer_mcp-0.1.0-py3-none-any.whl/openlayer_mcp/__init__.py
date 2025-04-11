from .openlayer_platform import mcp


def main():
    """Run the Openlayer MCP server."""
    mcp.run(transport="stdio")
