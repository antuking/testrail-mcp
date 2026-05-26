"""User tools registration."""
from typing import Dict, List, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_user", description="Get a user by ID")
    def get_user(user_id: int) -> Dict:
        return client.get_user(user_id)

    @mcp.tool("get_current_user", description="Get the current user by ID")
    def get_current_user(user_id: int) -> Dict:
        return client.get_current_user(user_id)

    @mcp.tool("get_user_by_email", description="Get a user by email")
    def get_user_by_email(email: str) -> Dict:
        return client.get_user_by_email(email)

    @mcp.tool("get_users", description="Get users (optionally for a project)")
    def get_users(project_id: Optional[int] = None) -> List[Dict]:
        return client.get_users(project_id=project_id)

    @mcp.tool("add_user", description="Add a new user")
    def add_user(
        name: str,
        email: str,
        role_id: int,
        is_active: Optional[bool] = None,
        group_id: Optional[int] = None,
    ) -> Dict:
        data = {
            'name': name,
            'email': email,
            'role_id': role_id,
        }
        if is_active is not None:
            data['is_active'] = is_active
        if group_id is not None:
            data['group_id'] = group_id
        return client.add_user(data)

    @mcp.tool("update_user", description="Update an existing user")
    def update_user(
        user_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        group_id: Optional[int] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if email is not None:
            data['email'] = email
        if role_id is not None:
            data['role_id'] = role_id
        if is_active is not None:
            data['is_active'] = is_active
        if group_id is not None:
            data['group_id'] = group_id
        return client.update_user(user_id, data)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://user/{user_id}")
    def get_user_resource(user_id: int) -> Dict:
        return client.get_user(user_id)
