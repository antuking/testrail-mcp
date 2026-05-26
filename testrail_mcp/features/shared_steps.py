"""Shared step tools registration."""
from typing import Dict, Optional, Union, List
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_shared_step", description="Get a shared step by ID")
    def get_shared_step(shared_step_id: int) -> Dict:
        return client.get_shared_step(shared_step_id)

    @mcp.tool("get_shared_step_history", description="Get history for a shared step")
    def get_shared_step_history(
        shared_step_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_shared_step_history(shared_step_id, limit=limit, offset=offset)

    @mcp.tool("get_shared_steps", description="Get shared steps for a project")
    def get_shared_steps(
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_shared_steps(
            project_id,
            created_after=created_after,
            created_before=created_before,
            created_by=created_by,
            updated_after=updated_after,
            updated_before=updated_before,
            updated_by=updated_by,
            limit=limit,
            offset=offset,
        )

    @mcp.tool("add_shared_step", description="Add a shared step")
    def add_shared_step(
        project_id: int,
        title: str,
        custom_shared_step_steps: Optional[str] = None,
        custom_shared_step_expected: Optional[str] = None,
        custom_shared_step_refs: Optional[str] = None,
        custom_shared_step_steps_separated: Optional[list] = None,
    ) -> Dict:
        data = {'title': title}
        if custom_shared_step_steps is not None:
            data['custom_shared_step_steps'] = custom_shared_step_steps
        if custom_shared_step_expected is not None:
            data['custom_shared_step_expected'] = custom_shared_step_expected
        if custom_shared_step_refs is not None:
            data['custom_shared_step_refs'] = custom_shared_step_refs
        if custom_shared_step_steps_separated is not None:
            data['custom_shared_step_steps_separated'] = custom_shared_step_steps_separated
        return client.add_shared_step(project_id, data)

    @mcp.tool("update_shared_step", description="Update a shared step")
    def update_shared_step(
        shared_step_id: int,
        title: Optional[str] = None,
        custom_shared_step_steps: Optional[str] = None,
        custom_shared_step_expected: Optional[str] = None,
        custom_shared_step_refs: Optional[str] = None,
        custom_shared_step_steps_separated: Optional[list] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if title is not None:
            data['title'] = title
        if custom_shared_step_steps is not None:
            data['custom_shared_step_steps'] = custom_shared_step_steps
        if custom_shared_step_expected is not None:
            data['custom_shared_step_expected'] = custom_shared_step_expected
        if custom_shared_step_refs is not None:
            data['custom_shared_step_refs'] = custom_shared_step_refs
        if custom_shared_step_steps_separated is not None:
            data['custom_shared_step_steps_separated'] = custom_shared_step_steps_separated
        return client.update_shared_step(shared_step_id, data)

    @mcp.tool("delete_shared_step", description="Delete a shared step")
    def delete_shared_step(shared_step_id: int) -> Dict:
        return client.delete_shared_step(shared_step_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://shared_step/{shared_step_id}")
    def get_shared_step_resource(shared_step_id: int) -> Dict:
        return client.get_shared_step(shared_step_id)
