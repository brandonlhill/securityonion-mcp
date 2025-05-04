#!/usr/bin/env python3

import asyncio
import os
import signal
import sys

import config

from fastmcp import FastMCP
from tools.so_elasticsearch_mcp import so_elasticsearch_mcp
from tools.so_files_mcp import so_files_mcp

# Define mcp class globally
main_mcp = FastMCP(name="securityonion")

async def setup():
    """Import subservers with prefixes here."""
    await main_mcp.import_server("so_elasticsearch", so_elasticsearch_mcp)
    await main_mcp.import_server("so_files", so_files_mcp)

async def main():
    # Check if the config file has been created
    try:
        cfg = config.load_config()
    except SystemExit:
        sys.exit(1)

    # Setup servers
    await setup()

    # Create a shutdown event
    shutdown_event = asyncio.Event()

    # Define signal handlers
    def shutdown_signal_handler():
        print("Shutdown signal received. Cleaning up...")
        shutdown_event.set()

    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown_signal_handler)

    # Run the MCP server in a background task
    server_task = asyncio.create_task(main_mcp.run_async(transport="sse", host="0.0.0.0", port=5001))

    # Wait for shutdown signal
    await shutdown_event.wait()

    # Perform any necessary cleanup here
    # For example, cancel tasks, close connections, etc.
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        print("Server task cancelled.")

if __name__ == "__main__":
    asyncio.run(main())