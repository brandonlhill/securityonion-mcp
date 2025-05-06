from fastmcp import FastMCP
from fastmcp import Context
import os

from config import ZEEK_DIR, SURICATA_DIR, STRELKA_DIR

so_filesearch_mcp = FastMCP(name="so_filesearch_mcp")

def safe_get_file(directory: str, filename: str) -> str:
    safe_name = os.path.basename(filename)
    full_path = os.path.join(directory, safe_name)
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"File {safe_name} not found in {directory}")
    return full_path

@so_filesearch_mcp.resource(uri="zeek://{filename}", mime_type="application/octet-stream")
def get_zeek_file(filename: str) -> bytes:
    """Retrieve a file from the Zeek directory."""
    path = safe_get_file(ZEEK_DIR, filename)
    with open(path, "rb") as f:
        return f.read()

@so_filesearch_mcp.resource(uri="suricata://{filename}", mime_type="application/octet-stream")
def get_suricata_pcap(filename: str) -> bytes:
    """Retrieve a PCAP from the Suricata directory."""
    path = safe_get_file(SURICATA_DIR, filename)
    with open(path, "rb") as f:
        return f.read()

@so_filesearch_mcp.resource(uri="strelka://{filename}")
def get_strelka_file(filename: str) -> bytes:
    """Retrieve a file from the Strelka directory."""
    return filename
    #path = safe_get_file(STRELKA_DIR, filename)
    ##await ctx.info(f"Hello world")
    #with open(path, "rb") as f:
    #    return f.read()