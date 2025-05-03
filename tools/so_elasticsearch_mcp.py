from fastmcp import FastMCP
from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_HOST, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD

so_elasticsearch_mcp = FastMCP(name="so_elasticsearch")

es = Elasticsearch(
    [ELASTICSEARCH_HOST],
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=False,
    ssl_show_warn=False,
    request_timeout=30
)

# TODO: Define more tool calls (for now these are just enough)
@so_elasticsearch_mcp.tool()
def search_elasticsearch(index: str, query: dict, size: int = 10, from_: int = 0) -> list:
    """Search documents in Elasticsearch."""
    res = es.search(index=index, query=query, size=size, from_=from_)
    return res["hits"]["hits"]

@so_elasticsearch_mcp.tool()
def list_indices() -> list:
    """List all indices in Elasticsearch."""
    indices = es.indices.get_alias("*")
    return list(indices.keys())