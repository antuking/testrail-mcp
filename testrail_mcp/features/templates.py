"""Template tools registration."""
from typing import Dict, List
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_templates", description="Get all test case templates for a project")
    def get_templates(project_id: int) -> List[Dict]:
        return client.get_templates(project_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    pass
