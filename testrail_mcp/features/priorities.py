"""Priority tools registration."""
from typing import Dict, List
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_priorities", description="Get all available test case priorities")
    def get_priorities() -> List[Dict]:
        return client.get_priorities()


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    pass
