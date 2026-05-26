"""Plan tools/resources registration."""
from typing import Dict, List, Any, Optional, Union
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_plan", description="Get a test plan by ID")
    def get_plan(plan_id: int) -> Dict:
        return client.get_plan(plan_id)

    @mcp.tool("get_plans", description="Get test plans for a project")
    def get_plans(
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        is_completed: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        milestone_id: Optional[Union[int, List[int], str]] = None,
    ) -> Dict:
        return client.get_plans(
            project_id,
            created_after=created_after,
            created_before=created_before,
            created_by=created_by,
            is_completed=is_completed,
            limit=limit,
            offset=offset,
            milestone_id=milestone_id,
        )

    @mcp.tool("add_plan", description="Add a new test plan")
    def add_plan(
        project_id: int,
        name: str,
        description: Optional[str] = None,
        milestone_id: Optional[int] = None,
        start_on: Optional[int] = None,
        due_on: Optional[int] = None,
        refs: Optional[str] = None,
        entries: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict:
        data: Dict[str, Any] = {'name': name}
        if description is not None:
            data['description'] = description
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if start_on is not None:
            data['start_on'] = start_on
        if due_on is not None:
            data['due_on'] = due_on
        if refs is not None:
            data['refs'] = refs
        if entries is not None:
            data['entries'] = entries
        return client.add_plan(project_id, data)

    @mcp.tool("add_plan_entry", description="Add a new plan entry")
    def add_plan_entry(
        plan_id: int,
        suite_id: int,
        name: str,
        description: Optional[str] = None,
        assignedto_id: Optional[int] = None,
        include_all: Optional[bool] = None,
        case_ids: Optional[List[int]] = None,
        config_ids: Optional[List[int]] = None,
        refs: Optional[str] = None,
        runs: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict:
        data: Dict[str, Any] = {
            'suite_id': suite_id,
            'name': name,
        }
        if description is not None:
            data['description'] = description
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if include_all is not None:
            data['include_all'] = include_all
        if case_ids is not None:
            data['case_ids'] = case_ids
        if config_ids is not None:
            data['config_ids'] = config_ids
        if refs is not None:
            data['refs'] = refs
        if runs is not None:
            data['runs'] = runs
        return client.add_plan_entry(plan_id, data)

    @mcp.tool("add_run_to_plan_entry", description="Add a new run to a plan entry")
    def add_run_to_plan_entry(
        plan_id: int,
        entry_id: str,
        config_ids: List[int],
        description: Optional[str] = None,
        assignedto_id: Optional[int] = None,
        include_all: Optional[bool] = None,
        case_ids: Optional[List[int]] = None,
        refs: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, Any] = {'config_ids': config_ids}
        if description is not None:
            data['description'] = description
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if include_all is not None:
            data['include_all'] = include_all
        if case_ids is not None:
            data['case_ids'] = case_ids
        if refs is not None:
            data['refs'] = refs
        return client.add_run_to_plan_entry(plan_id, entry_id, data)

    @mcp.tool("update_plan", description="Update an existing test plan")
    def update_plan(
        plan_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        milestone_id: Optional[int] = None,
        start_on: Optional[int] = None,
        due_on: Optional[int] = None,
        refs: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, Any] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        if milestone_id is not None:
            data['milestone_id'] = milestone_id
        if start_on is not None:
            data['start_on'] = start_on
        if due_on is not None:
            data['due_on'] = due_on
        if refs is not None:
            data['refs'] = refs
        return client.update_plan(plan_id, data)

    @mcp.tool("update_run_in_plan_entry", description="Update a run in a plan entry")
    def update_run_in_plan_entry(
        run_id: int,
        description: Optional[str] = None,
        assignedto_id: Optional[int] = None,
        include_all: Optional[bool] = None,
        case_ids: Optional[List[int]] = None,
        refs: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, Any] = {}
        if description is not None:
            data['description'] = description
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if include_all is not None:
            data['include_all'] = include_all
        if case_ids is not None:
            data['case_ids'] = case_ids
        if refs is not None:
            data['refs'] = refs
        return client.update_run_in_plan_entry(run_id, data)

    @mcp.tool("close_plan", description="Close a test plan")
    def close_plan(plan_id: int) -> Dict:
        return client.close_plan(plan_id)

    @mcp.tool("delete_plan", description="Delete a test plan")
    def delete_plan(plan_id: int) -> Dict:
        return client.delete_plan(plan_id)

    @mcp.tool("delete_plan_entry", description="Delete a plan entry")
    def delete_plan_entry(plan_id: int, entry_id: str) -> Dict:
        return client.delete_plan_entry(plan_id, entry_id)

    @mcp.tool("delete_run_from_plan_entry", description="Delete a run from a plan entry")
    def delete_run_from_plan_entry(run_id: int) -> Dict:
        return client.delete_run_from_plan_entry(run_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://plan/{plan_id}")
    def get_plan_resource(plan_id: int) -> Dict:
        return client.get_plan(plan_id)
