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
def search(index: str, query: dict, size: int = 10, from_: int = 0) -> dict:
    """Search documents in Elasticsearch."""
    #search(*, index=None, aggregations=None, aggs=None, allow_no_indices=None, allow_partial_search_results=None, analyze_wildcard=None, analyzer=None, batched_reduce_size=None, ccs_minimize_roundtrips=None, collapse=None, default_operator=None, df=None, docvalue_fields=None, error_trace=None, expand_wildcards=None, explain=None, ext=None, fields=None, filter_path=None, force_synthetic_source=None, from_=None, highlight=None, human=None, ignore_throttled=None, ignore_unavailable=None, include_named_queries_score=None, indices_boost=None, knn=None, lenient=None, max_concurrent_shard_requests=None, min_compatible_shard_node=None, min_score=None, pit=None, post_filter=None, pre_filter_shard_size=None, preference=None, pretty=None, profile=None, q=None, query=None, rank=None, request_cache=None, rescore=None, rest_total_hits_as_int=None, retriever=None, routing=None, runtime_mappings=None, script_fields=None, scroll=None, search_after=None, search_type=None, seq_no_primary_term=None, size=None, slice=None, sort=None, source=None, source_excludes=None, source_includes=None, stats=None, stored_fields=None, suggest=None, suggest_field=None, suggest_mode=None, suggest_size=None, suggest_text=None, terminate_after=None, timeout=None, track_scores=None, track_total_hits=None, typed_keys=None, version=None, body=None)
    return dict(es.search(index=index, query=query, size=size, from_=from_))

# Tool: List Indices
@so_elasticsearch_mcp.tool()
def list_indices() -> list:
    """List all indices in Elasticsearch."""
    index = es.indices.get_alias()
    return [index]
