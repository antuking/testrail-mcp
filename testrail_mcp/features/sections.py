"""Section tools registration."""
from typing import Dict, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_section", description="Retrieves details of a specific section by ID")
    def get_section(section_id: int) -> Dict:
        return client.get_section(section_id)

    @mcp.tool("get_sections", description="Retrieves all sections for a specified project and or suite")
    def get_sections(
        project_id: int,
        suite_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_sections(project_id, suite_id=suite_id, limit=limit, offset=offset)

    @mcp.tool("add_section", description="Creates a new section in a TestRail project")
    def add_section(
        project_id: int,
        name: str,
        description: str,
        suite_id: Optional[int] = None,
        parent_id: Optional[int] = None,
    ) -> Dict:
        data = {
            'name': name,
            'description': description,
        }
        if suite_id is not None:
            data['suite_id'] = suite_id
        if parent_id is not None:
            data['parent_id'] = parent_id
        return client.add_section(project_id, data)

    @mcp.tool("update_section", description="Updates an existing section")
    def update_section(
        section_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        return client.update_section(section_id, data)

    @mcp.tool("delete_section", description="Deletes a section")
    def delete_section(section_id: int, soft: bool) -> Dict:
        return client.delete_section(section_id, soft)

    @mcp.tool("move_section", description="Moves a section to a new position in the test hierarchy")
    def move_section(
        section_id: int,
        parent_id: Optional[int],
        after_id: Optional[int],
    ) -> Dict:
        data: Dict[str, object] = {}
        if parent_id is not None:
            data['parent_id'] = parent_id
        if after_id is not None:
            data['after_id'] = after_id
        return client.move_section(section_id, data)
