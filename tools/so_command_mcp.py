from fastmcp import FastMCP, Context
import subprocess

so_command_mcp = FastMCP(name="so_command")

# Note that this server is NOT SECURE, and could have command injection from the mcp server. Hence why this server isn't enabled on default.

def run_command(cmd: str) -> str:
    """Executes a shell command and returns output or raises an error."""
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {cmd}\n{e.stderr}")


@so_command_mcp.resource(uri="admin://host/{host_cmd}", mime_type="text/plain")
def get_host_ip(host_cmd: str, ctx: Context) -> str:
    if host_cmd == "ip":
        return run_safe_command("hostname", "-I")
    if host_cmd == "hostname":
        return run_safe_command("hostname")
    raise ValueError(f"Unsupported host_cmd: {host_cmd}")


# SecurityOnion Commands
@so_command_mcp.resource(uri="admin://status/{s}", mime_type="text/plain")
def get_system_status(s: str, ctx: Context, quiet: bool = False, json_output: bool = False, install_check: bool = False) -> str:
    cmd = "so-status"
    if quiet:
        cmd += " -q"
    if json_output:
        cmd += " -j"
    if install_check:
        cmd += " -i"
    return run_command(cmd)



# TODO: These still need to be implemented
# @so_command_mcp.resource(uri="admin://rule-update", mime_type="text/plain")
# def update_rules(ctx: Context) -> str:
#     return run_command("so-rule-update")

# @so_command_mcp.resource(uri="admin://redis-count", mime_type="text/plain")
# def redis_queue_length(ctx: Context) -> str:
#     return run_command("so-redis-count")

# @so_command_mcp.resource(uri="admin://firewall-allow", mime_type="text/plain")
# def firewall_allow(ctx: Context, role: str = "analyst", ip_address: str = "") -> str:
#     if not ip_address:
#         raise ValueError("IP address is required for firewall allow.")
#     cmd = f"so-firewall includehost {role} {ip_address}"
#     return run_command(cmd)

# @so_command_mcp.resource(uri="admin://firewall-control", mime_type="text/plain")
# def firewall_control(ctx: Context, action: str, group: str = "", ip_address: str = "") -> str:
#     if action not in ["includehost", "excludehost", "includedhosts", "excludedhosts"]:
#         raise ValueError("Invalid firewall action.")
#     cmd = f"so-firewall {action}"
#     if group:
#         cmd += f" {group}"
#     if ip_address:
#         cmd += f" {ip_address}"
#     return run_command(cmd)

# @so_command_mcp.resource(uri="admin://update", mime_type="text/plain")
# def update_securityonion(ctx: Context) -> str:
#     return run_command("soup")

# @so_command_mcp.resource(uri="salt://ping", mime_type="text/plain")
# def salt_ping(ctx: Context) -> str:
#     return run_command("salt '*' test.ping")

# @so_command_mcp.resource(uri="salt://run/{cmd}", mime_type="text/plain")
# def salt_run_command(cmd: str, ctx: Context) -> str:
#     return run_command(f"salt '*' cmd.run \"{cmd}\"")

# @so_command_mcp.resource(uri="salt://sync", mime_type="text/plain")
# def salt_sync(ctx: Context) -> str:
#     return run_command("salt '*' state.highstate")

# @so_command_mcp.resource(uri="salt://status", mime_type="text/plain")
# def salt_check_status(ctx: Context) -> str:
#     return run_command("salt '*' so.status")
