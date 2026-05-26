"""Group tools/resources registration."""
from typing import Dict, List, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_group", description="Get a group by ID")
    def get_group(group_id: int) -> Dict:
        return client.get_group(group_id)

    @mcp.tool("get_groups", description="Get all groups")
    def get_groups() -> List[Dict]:
        return client.get_groups()

    @mcp.tool("add_group", description="Add a new group")
    def add_group(
        name: str,
        user_ids: Optional[List[int]] = None,
    ) -> Dict:
        data = {'name': name}
        if user_ids is not None:
            data['user_ids'] = user_ids
        return client.add_group(data)

    @mcp.tool("update_group", description="Update an existing group")
    def update_group(
        group_id: int,
        name: Optional[str] = None,
        user_ids: Optional[List[int]] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if user_ids is not None:
            data['user_ids'] = user_ids
        return client.update_group(group_id, data)

    @mcp.tool("delete_group", description="Delete a group")
    def delete_group(group_id: int) -> Dict:
        return client.delete_group(group_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://group/{group_id}")
    def get_group_resource(group_id: int) -> Dict:
        return client.get_group(group_id)
