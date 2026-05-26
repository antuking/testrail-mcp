"""Result tools/resources registration."""
from typing import Dict, List, Any, Optional, Union
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_result_fields", description="Get all available test result custom fields")
    def get_result_fields() -> List[Dict]:
        return client.get_result_fields()

    @mcp.tool("get_results", description="Get all test results for a test")
    def get_results(
        test_id: int,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        return client.get_results(
            test_id,
            defects_filter=defects_filter,
            status_id=status_id,
            limit=limit,
            offset=offset,
        )

    @mcp.tool("get_results_for_case", description="Get all test results for a run + case")
    def get_results_for_case(
        run_id: int,
        case_id: int,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        return client.get_results_for_case(
            run_id,
            case_id,
            defects_filter=defects_filter,
            status_id=status_id,
            limit=limit,
            offset=offset,
        )

    @mcp.tool("get_results_for_run", description="Get all test results for a run")
    def get_results_for_run(
        run_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        return client.get_results_for_run(
            run_id,
            created_after=created_after,
            created_before=created_before,
            created_by=created_by,
            defects_filter=defects_filter,
            status_id=status_id,
            limit=limit,
            offset=offset,
        )

    @mcp.tool("add_result", description="Add a new test result")
    def add_result(
        test_id: int,
        status_id: int,
        comment: Optional[str] = None,
        version: Optional[str] = None,
        elapsed: Optional[str] = None,
        defects: Optional[str] = None,
        assignedto_id: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        data = {
            'status_id': status_id,
        }
        if comment is not None:
            data['comment'] = comment
        if version is not None:
            data['version'] = version
        if elapsed is not None:
            data['elapsed'] = elapsed
        if defects is not None:
            data['defects'] = defects
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if custom_fields:
            data.update(custom_fields)
        return client.add_result(test_id, data)

    @mcp.tool("add_result_for_case", description="Add a new test result for a case in a run")
    def add_result_for_case(
        run_id: int,
        case_id: int,
        status_id: int,
        comment: Optional[str] = None,
        version: Optional[str] = None,
        elapsed: Optional[str] = None,
        defects: Optional[str] = None,
        assignedto_id: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        data = {
            'status_id': status_id,
        }
        if comment is not None:
            data['comment'] = comment
        if version is not None:
            data['version'] = version
        if elapsed is not None:
            data['elapsed'] = elapsed
        if defects is not None:
            data['defects'] = defects
        if assignedto_id is not None:
            data['assignedto_id'] = assignedto_id
        if custom_fields:
            data.update(custom_fields)
        return client.add_result_for_case(run_id, case_id, data)

    @mcp.tool("add_results", description="Add multiple test results for a run")
    def add_results(run_id: int, results: List[Dict[str, Any]]) -> List[Dict]:
        return client.add_results(run_id, {'results': results})

    @mcp.tool("add_results_for_cases", description="Add multiple test results for cases in a run")
    def add_results_for_cases(run_id: int, results: List[Dict[str, Any]]) -> List[Dict]:
        return client.add_results_for_cases(run_id, {'results': results})


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://results/{test_id}")
    def get_results_resource(test_id: int) -> List[Dict]:
        return client.get_results(test_id)
