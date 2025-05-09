from fastmcp import FastMCP, Context
import os

so_filesearch_mcp = FastMCP(name="so_filesearch")

# Individual diagnostic log paths
LOG_PATHS = {
    "suricata": "/opt/so/log/suricata/suricata.log",
    "stenographer": "/opt/so/log/stenographer/stenographer.log",
    "zeek_current": "/nsm/zeek/logs/current/",  # Directory
    "zeek_stderr": "/opt/so/log/zeek/stderr.log",
    "zeek_reporter": "/opt/so/log/zeek/reporter.log",
    "zeek_loaded_scripts": "/opt/so/log/zeek/loaded_scripts.log",
    "strelka": "/opt/so/log/strelka/",
    "logstash": "/opt/so/log/logstash/logstash.log",
    "elasticsearch": "/opt/so/log/elasticsearch/elasticsearch.log",  # Simplified
    "elastalert": "/opt/so/log/elastalert/elastalert.log",
    "kibana": "/opt/so/log/kibana/kibana.log",
    "influxdb": "/opt/so/log/influxdb/",
    "other": "/opt/so/log/",
}


def safe_get(path: str, is_dir: bool = False) -> str:
    """Ensure a file or directory exists."""
    if is_dir:
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory not found: {path}")
    else:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
    return path


def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


# === Individual log file resources ===

@so_filesearch_mcp.resource(uri="log://suricata", mime_type="text/plain")
def get_suricata_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["suricata"])
    ctx.debug("Serving suricata.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://stenographer", mime_type="text/plain")
def get_stenographer_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["stenographer"])
    ctx.debug("Serving stenographer.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://zeek_reporter", mime_type="text/plain")
def get_zeek_reporter_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["zeek_reporter"])
    ctx.debug("Serving reporter.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://zeek_stderr", mime_type="text/plain")
def get_zeek_stderr_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["zeek_stderr"])
    ctx.debug("Serving stderr.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://zeek_loaded_scripts", mime_type="text/plain")
def get_zeek_loaded_scripts(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["zeek_loaded_scripts"])
    ctx.debug("Serving loaded_scripts.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://logstash", mime_type="text/plain")
def get_logstash_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["logstash"])
    ctx.debug("Serving logstash.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://elasticsearch", mime_type="text/plain")
def get_elasticsearch_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["elasticsearch"])
    ctx.debug("Serving elasticsearch.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://elastalert", mime_type="text/plain")
def get_elastalert_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["elastalert"])
    ctx.debug("Serving elastalert.log")
    return read_file(path)


@so_filesearch_mcp.resource(uri="log://kibana", mime_type="text/plain")
def get_kibana_log(ctx: Context) -> bytes:
    path = safe_get(LOG_PATHS["kibana"])
    ctx.debug("Serving kibana.log")
    return read_file(path)


# === Directory listings or dynamic file access could be added as needed ===

@so_filesearch_mcp.resource(uri="logdir://{component}/{filename}", mime_type="text/plain")
def get_dynamic_log(component: str, filename: str, ctx: Context) -> bytes:
    """Generic access to files within known diagnostic directories."""
    base = LOG_PATHS.get(component)
    if not base:
        raise FileNotFoundError(f"Unknown log component: {component}")
    full_path = os.path.join(base, os.path.basename(filename))
    safe_get(full_path)
    ctx.debug(f"Serving {component} log file: {filename}")
    return read_file(full_path)
