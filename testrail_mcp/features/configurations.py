"""Configuration tools/resources registration."""
from typing import Dict, List
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_configs", description="Get all configuration groups and configurations for a project")
    def get_configs(project_id: int) -> List[Dict]:
        return client.get_configs(project_id)

    @mcp.tool("add_config_group", description="Add a new configuration group")
    def add_config_group(project_id: int, name: str) -> Dict:
        return client.add_config_group(project_id, name)

    @mcp.tool("add_config", description="Add a new configuration to a group")
    def add_config(config_group_id: int, name: str) -> Dict:
        return client.add_config(config_group_id, name)

    @mcp.tool("update_config_group", description="Update an existing configuration group")
    def update_config_group(config_group_id: int, name: str) -> Dict:
        return client.update_config_group(config_group_id, name)

    @mcp.tool("update_config", description="Update an existing configuration")
    def update_config(config_id: int, name: str) -> Dict:
        return client.update_config(config_id, name)

    @mcp.tool("delete_config_group", description="Delete a configuration group")
    def delete_config_group(config_group_id: int) -> Dict:
        return client.delete_config_group(config_group_id)

    @mcp.tool("delete_config", description="Delete a configuration")
    def delete_config(config_id: int) -> Dict:
        return client.delete_config(config_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://configurations/{project_id}")
    def get_configs_resource(project_id: int) -> List[Dict]:
        return client.get_configs(project_id)
