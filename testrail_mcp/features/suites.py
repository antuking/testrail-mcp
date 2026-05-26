"""Suites tools/resources registration."""
from typing import Dict, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_suite", description="Get a test suite by ID")
    def get_suite(suite_id: int) -> Dict:
        return client.get_suite(suite_id)

    @mcp.tool("get_suites", description="Get test suites for a project")
    def get_suites(
        project_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_suites(project_id, limit=limit, offset=offset)

    @mcp.tool("add_suite", description="Add a new test suite")
    def add_suite(
        project_id: int,
        name: str,
        description: Optional[str] = None,
    ) -> Dict:
        data = {'name': name}
        if description is not None:
            data['description'] = description
        return client.add_suite(project_id, data)

    @mcp.tool("update_suite", description="Update an existing test suite")
    def update_suite(
        suite_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        return client.update_suite(suite_id, data)

    @mcp.tool("delete_suite", description="Delete a test suite")
    def delete_suite(suite_id: int, soft: Optional[bool] = None) -> Dict:
        return client.delete_suite(suite_id, soft=soft)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://suite/{suite_id}")
    def get_suite_resource(suite_id: int) -> Dict:
        return client.get_suite(suite_id)
