from fastmcp import FastMCP
from elasticsearch import Elasticsearch
import config

# Load config and extract values
cfg = config.load_config()
es_cfg = cfg["elasticsearch"]

# Initialize FastMCP and Elasticsearch client
so_elasticsearch_mcp = FastMCP(name="so_elasticsearch")

es = Elasticsearch(
    [es_cfg["host"]],
    basic_auth=(es_cfg["username"], es_cfg["password"]),
    verify_certs=False,
    ssl_show_warn=False,
    request_timeout=30
)

# Tool: Search Elasticsearch
@so_elasticsearch_mcp.tool()
def search_elasticsearch(index: str, query: dict, size: int = 10, from_: int = 0) -> list:
    """Search documents in Elasticsearch."""
    res = es.search(index=index, query=query, size=size, from_=from_)
    return res["hits"]["hits"]

# Tool: List Indices
@so_elasticsearch_mcp.tool()
def list_indices() -> list:
    """List all indices in Elasticsearch."""
    indices = es.indices.get_alias("*")
    return list(indices.keys())
