"""Attachment tools registration."""
from typing import Dict, Optional
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("add_attachment_to_case", description="Add an attachment to a test case")
    def add_attachment_to_case(
        case_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        return client.add_attachment_to_case(
            case_id,
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    @mcp.tool("add_attachment_to_plan", description="Add an attachment to a test plan")
    def add_attachment_to_plan(
        plan_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        return client.add_attachment_to_plan(
            plan_id,
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    @mcp.tool("add_attachment_to_plan_entry", description="Add an attachment to a test plan entry")
    def add_attachment_to_plan_entry(
        plan_id: int,
        entry_id: str,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        return client.add_attachment_to_plan_entry(
            plan_id,
            entry_id,
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    @mcp.tool("add_attachment_to_result", description="Add an attachment to a test result")
    def add_attachment_to_result(
        result_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        return client.add_attachment_to_result(
            result_id,
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    @mcp.tool("add_attachment_to_run", description="Add an attachment to a test run")
    def add_attachment_to_run(
        run_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        return client.add_attachment_to_run(
            run_id,
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    @mcp.tool("get_attachments_for_case", description="Get attachments for a test case")
    def get_attachments_for_case(
        case_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_attachments_for_case(case_id, limit=limit, offset=offset)

    @mcp.tool("get_attachments_for_plan", description="Get attachments for a test plan")
    def get_attachments_for_plan(
        plan_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_attachments_for_plan(plan_id, limit=limit, offset=offset)

    @mcp.tool("get_attachments_for_plan_entry", description="Get attachments for a test plan entry")
    def get_attachments_for_plan_entry(plan_id: int, entry_id: str) -> Dict:
        return client.get_attachments_for_plan_entry(plan_id, entry_id)

    @mcp.tool("get_attachments_for_run", description="Get attachments for a test run")
    def get_attachments_for_run(
        run_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        return client.get_attachments_for_run(run_id, limit=limit, offset=offset)

    @mcp.tool("get_attachments_for_test", description="Get attachments for a test")
    def get_attachments_for_test(test_id: int) -> Dict:
        return client.get_attachments_for_test(test_id)

    @mcp.tool("get_attachment", description="Get a raw attachment by ID")
    def get_attachment(attachment_id: int) -> bytes:
        return client.get_attachment(attachment_id)

    @mcp.tool("delete_attachment", description="Delete an attachment")
    def delete_attachment(attachment_id: int) -> Dict:
        return client.delete_attachment(attachment_id)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    pass
