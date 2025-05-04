#!/usr/bin/env python3

import asyncio
import os
import signal
import sys

from fastmcp import FastMCP
from tools.so_elasticsearch_mcp import so_elasticsearch_mcp
from tools.so_files_mcp import so_files_mcp

# Define mcp class globally
main_mcp = FastMCP(name="securityonion")

def shutdown_signal_handler(signal_received, frame):
    """Function to handle shutdown signals"""
    print("Shutdown signal received. Cleaning up...")
    # Perform any necessary cleanup here
    sys.exit(0)

async def setup():
    """Import subservers with prefixes here: (note that you can build servers and import them here)"""
    await main_mcp.import_server("so_elasticsearch", so_elasticsearch_mcp)
    await main_mcp.import_server("so_files", so_files_mcp)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, shutdown_signal_handler)
    signal.signal(signal.SIGTERM, shutdown_signal_handler)

    # Start subservers
    asyncio.run(setup())
    main_mcp.run(transport="sse", host="0.0.0.0", port=5001)