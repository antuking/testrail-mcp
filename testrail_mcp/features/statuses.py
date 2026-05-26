"""Status tools registration."""
from typing import Dict, List
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_statuses", description="Get all test statuses")
    def get_statuses() -> List[Dict]:
        return client.get_statuses()

    @mcp.tool("get_case_statuses", description="Get all case statuses")
    def get_case_statuses() -> List[Dict]:
        return client.get_case_statuses()

    @mcp.tool("get_status_id_by_name", description="Get the ID of a test status by its name")
    def get_status_id_by_name(name: str) -> int:
        return client.get_status_id_by_name(name)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    pass
