from mcp.server.fastmcp import FastMCP

from escloud_mcp_server.tools import instance_info, resource_info


class ESCloudMCPServer:
    def __init__(self):
        self.name = "ESCloudMCPServer"
        self.mcp = FastMCP(self.name)
        self._register_tools()

    def _register_tools(self):
        """Register tools to the mcp server."""
        resource_info.register_tools(self.mcp)
        instance_info.register_tools(self.mcp)

    def run(self):
        """Run the mcp server."""
        self.mcp.run(transport="stdio")


def main():
    server = ESCloudMCPServer()
    server.run()


if __name__ == "__main__":
    print("Start ESCloud MCP Server")
    main()
