import volcenginesdkescloud
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from escloud_mcp_server.client import create_escloud_client


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def escloud_describe_zones(region_id: str):
        """
        查询云搜索服务在指定区域下的可用区列表，包括可用区 id、名称、状态等信息。

        :param region_id: 区域 id
        :return: 可用区列表
        """
        try:
            client = create_escloud_client(region_id)
            response = client.describe_zones(
                volcenginesdkescloud.DescribeZonesRequest()
            )
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")