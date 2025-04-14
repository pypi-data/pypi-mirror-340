from mcp.server.fastmcp import FastMCP
try:
    from ..base.models import GlobalVar
except ImportError:
    from aivk.base.models import GlobalVar

port = GlobalVar.get_port()
host = GlobalVar.get_host()

# 创建 FastMCP 实例
mcp = FastMCP(
    name="aivk", 
    instructions="aivk mcp server", 
    port=port,
    host=host
)

@mcp.resource("aivk://status")
def status():
    """返回 AIVK 状态信息"""
    return {
        "status": "running",
        "host": host,
        "port": port,
        "server_name": "aivk-mcp"
    }






