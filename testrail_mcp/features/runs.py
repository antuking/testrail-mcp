"""Run tools/resources registration."""
from typing import Dict, List, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_run", description="Get a test run by ID")
    def get_run(run_id: int) -> Dict:
        return client.get_run(run_id)

    @mcp.tool("get_runs", description="Get all test runs for a project")
    def get_runs(project_id: int) -> List[Dict]:
        return client.get_runs(project_id)

    @mcp.tool("add_run", description="Add a new test run")
    def add_run(
        project_id: int,
        suite_id: int,
        name: str,
        description: Optional[str] = None,
        milestone_id: Optional[int] = None,
        assignedto_id: Optional[int] = None,
        include_all: Optional[bool] = None,
        case_ids: Optional[List[int]] = None,
        refs: Optional[str] = None,
    ) -> Dict:
        data = {
            'suite_id': suite_id,
            'name': name,
        }
        if description is not None:
            data['description'] = description
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if include_all is not None:
            data['include_all'] = include_all
        if case_ids is not None:
            data['case_ids'] = case_ids
        if refs is not None:
            data['refs'] = refs
        return client.add_run(project_id, data)

    @mcp.tool("update_run", description="Update an existing test run")
    def update_run(
        run_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        milestone_id: Optional[int] = None,
        assignedto_id: Optional[int] = None,
        include_all: Optional[bool] = None,
        case_ids: Optional[List[int]] = None,
        refs: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if include_all is not None:
            data['include_all'] = include_all
        if case_ids is not None:
            data['case_ids'] = case_ids
        if refs is not None:
            data['refs'] = refs
        return client.update_run(run_id, data)

    @mcp.tool("close_run", description="Close an existing test run")
    def close_run(run_id: int) -> Dict:
        return client.close_run(run_id)

    @mcp.tool("delete_run", description="Delete a test run")
    def delete_run(run_id: int) -> Dict:
        return client.delete_run(run_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://run/{run_id}")
    def get_run_resource(run_id: int) -> Dict:
        return client.get_run(run_id)
