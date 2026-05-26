"""Milestone tools/resources registration."""
from typing import Dict, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_milestone", description="Get a milestone by ID")
    def get_milestone(milestone_id: int) -> Dict:
        return client.get_milestone(milestone_id)

    @mcp.tool("get_milestones", description="Get milestones for a project")
    def get_milestones(
        project_id: int,
        is_completed: Optional[bool] = None,
        is_started: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_milestones(
            project_id,
            is_completed=is_completed,
            is_started=is_started,
            limit=limit,
            offset=offset,
        )

    @mcp.tool("add_milestone", description="Add a new milestone")
    def add_milestone(
        project_id: int,
        name: str,
        description: Optional[str] = None,
        due_on: Optional[int] = None,
        parent_id: Optional[int] = None,
        refs: Optional[str] = None,
        start_on: Optional[int] = None,
    ) -> Dict:
        data = {'name': name}
        if description is not None:
            data['description'] = description
        if due_on is not None:
            data['due_on'] = due_on
        if parent_id is not None:
            data['parent_id'] = parent_id
        if refs is not None:
            data['refs'] = refs
        if start_on is not None:
            data['start_on'] = start_on
        return client.add_milestone(project_id, data)

    @mcp.tool("update_milestone", description="Update an existing milestone")
    def update_milestone(
        milestone_id: int,
        is_completed: Optional[bool] = None,
        is_started: Optional[bool] = None,
        parent_id: Optional[int] = None,
        start_on: Optional[int] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if is_completed is not None:
            data['is_completed'] = is_completed
        if is_started is not None:
            data['is_started'] = is_started
        if parent_id is not None:
            data['parent_id'] = parent_id
        if start_on is not None:
            data['start_on'] = start_on
        return client.update_milestone(milestone_id, data)

    @mcp.tool("delete_milestone", description="Delete a milestone")
    def delete_milestone(milestone_id: int) -> Dict:
        return client.delete_milestone(milestone_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://milestone/{milestone_id}")
    def get_milestone_resource(milestone_id: int) -> Dict:
        return client.get_milestone(milestone_id)
