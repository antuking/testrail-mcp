"""Project tools/resources registration."""
from typing import Dict, List, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_project", description="Get a project by ID")
    def get_project(project_id: int) -> Dict:
        """Get a project by ID."""
        return client.get_project(project_id)

    @mcp.tool("get_projects", description="Get all projects")
    def get_projects() -> List[Dict]:
        """Get all projects."""
        return client.get_projects()

    @mcp.tool("add_project", description="Add a new project")
    def add_project(
        name: str,
        announcement: Optional[str] = None,
        show_announcement: Optional[bool] = None,
        suite_mode: Optional[int] = None,
    ) -> Dict:
        data = {'name': name}
        if announcement is not None:
            data['announcement'] = announcement
        if show_announcement is not None:
            data['show_announcement'] = show_announcement
        if suite_mode is not None:
            data['suite_mode'] = suite_mode
        return client.add_project(data)

    @mcp.tool("update_project", description="Update an existing project")
    def update_project(
        project_id: int,
        name: Optional[str] = None,
        announcement: Optional[str] = None,
        show_announcement: Optional[bool] = None,
        is_completed: Optional[bool] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if announcement is not None:
            data['announcement'] = announcement
        if show_announcement is not None:
            data['show_announcement'] = show_announcement
        if is_completed is not None:
            data['is_completed'] = is_completed
        return client.update_project(project_id, data)

    @mcp.tool("delete_project", description="Delete a project")
    def delete_project(project_id: int) -> Dict:
        return client.delete_project(project_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://project/{project_id}")
    def get_project_resource(project_id: int) -> Dict:
        return client.get_project(project_id)
