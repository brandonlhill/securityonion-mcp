import os

from fastmcp import FastMCP
from config import ZEEK_DIR, SURICATA_DIR, STRELKA_DIR

so_files_mcp = FastMCP(name="so_files")

# Helper function
def safe_get_file(directory: str, filename: str) -> str:
    safe_name = os.path.basename(filename)
    full_path = os.path.join(directory, safe_name)
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"File {safe_name} not found in {directory}")
    return full_path

@so_files_mcp.tool()
def get_zeek_file(filename: str) -> str:
    """
    Retrieve a file from the Zeek directory.
    """
    return safe_get_file(ZEEK_DIR, filename)

@so_files_mcp.tool()
def get_suricata_pcap(filename: str) -> str:
    """
    Retrieve a pcap file from the Suricata directory.
    """
    return safe_get_file(SURICATA_DIR, filename)

@so_files_mcp.tool()
def get_strelka_file(filename: str) -> str:
    """
    Retrieve a file from the Strelka directory.
    """
    return safe_get_file(STRELKA_DIR, filename)
