import asyncio

from fastmcp import FastMCP
from tools.so_elasticsearch_mcp import so_elasticsearch_mcp
from tools.so_files_mcp import so_files_mcp

main_mcp = FastMCP(name="securityonion")

async def setup():
    # Import subservers with prefixes
    await main_mcp.import_server("so_elasticsearch", so_elasticsearch_mcp)
    await main_mcp.import_server("so_files", so_files_mcp)

if __name__ == "__main__":
    asyncio.run(setup())
    main_mcp.run(transport="sse", host="0.0.0.0", port=5001)