"""Label tools/resources registration."""
from typing import Dict, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_label", description="Get a label by ID")
    def get_label(label_id: int) -> Dict:
        return client.get_label(label_id)

    @mcp.tool("get_labels", description="Get labels for a project")
    def get_labels(
        project_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict:
        return client.get_labels(project_id, offset=offset, limit=limit)

    @mcp.tool("update_label", description="Update an existing label")
    def update_label(
        label_id: int,
        project_id: int,
        title: str,
    ) -> Dict:
        return client.update_label(label_id, project_id, title)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://label/{label_id}")
    def get_label_resource(label_id: int) -> Dict:
        return client.get_label(label_id)
