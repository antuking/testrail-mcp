"""Dataset tools/resources registration."""
from typing import Dict, List, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_dataset", description="Get a dataset by ID")
    def get_dataset(dataset_id: int) -> Dict:
        return client.get_dataset(dataset_id)

    @mcp.tool("get_datasets", description="Get all datasets for a project")
    def get_datasets(project_id: int) -> List[Dict]:
        return client.get_datasets(project_id)

    @mcp.tool("add_dataset", description="Add a new dataset")
    def add_dataset(
        project_id: int,
        name: str,
        description: Optional[str] = None,
    ) -> Dict:
        data = {'name': name}
        if description is not None:
            data['description'] = description
        return client.add_dataset(project_id, data)

    @mcp.tool("update_dataset", description="Update an existing dataset")
    def update_dataset(
        dataset_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict:
        data: Dict[str, object] = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        return client.update_dataset(dataset_id, data)

    @mcp.tool("delete_dataset", description="Delete a dataset")
    def delete_dataset(dataset_id: int) -> Dict:
        return client.delete_dataset(dataset_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://dataset/{dataset_id}")
    def get_dataset_resource(dataset_id: int) -> Dict:
        return client.get_dataset(dataset_id)
