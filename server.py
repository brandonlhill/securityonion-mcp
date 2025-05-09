#!/usr/bin/env python3

import asyncio
import importlib.util
import os
import signal
import sys

import config
from fastmcp import FastMCP

# Fallbacks in case dynamic import fails
from tools import so_elasticsearch_mcp, so_filesearch_mcp

main_mcp = FastMCP(name="securityonion")
TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

def load_mcp_modules(tools_dir):
    """Dynamically load all FastMCP servers from Python files in tools/."""
    loaded = {}
    for filename in os.listdir(tools_dir):
        if not filename.endswith(".py") or filename.startswith("__"):
            continue

        module_name = filename[:-3]
        full_path = os.path.join(tools_dir, filename)

        spec = importlib.util.spec_from_file_location(f"tools.{module_name}", full_path)
        if not spec or not spec.loader:
            continue

        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            # Look for the first variable ending in _mcp and being a FastMCP instance
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if attr_name.endswith("_mcp") and isinstance(attr, FastMCP):
                    loaded[module_name] = attr
                    break
        except Exception as e:
            print(f"[!] Error loading {module_name}: {e}")
    return loaded

async def main():
    try:
        config.load_config()
    except SystemExit:
        sys.exit(1)

    # Dynamically load MCPs
    loaded_mcps = load_mcp_modules(TOOLS_DIR)

    # Import all unique FastMCP subservers
    for name, mcp in loaded_mcps.items():
        prefix = name.replace("so_", "").replace("_mcp", "")
        try:
            await main_mcp.import_server(prefix, mcp)
        except Exception as e:
            print(f"[!] Failed to import server '{name}': {e}")


   

    shutdown_event = asyncio.Event()

    def signal_handler(*_):
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run server
    server_task = asyncio.create_task(
        main_mcp.run_async(transport="sse", host="0.0.0.0", port=5001, log_level="debug")
    )

    await shutdown_event.wait()

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        print("Server task cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
