"""Test tools/resources registration."""
from typing import Dict, List, Optional, Union
from fastmcp import FastMCP

from testrail_mcp.testrail_client import TestRailClient


def register_tools(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.tool("get_test", description="Get a test by ID")
    def get_test(test_id: int, with_data: Optional[str] = None) -> Dict:
        return client.get_test(test_id, with_data=with_data)

    @mcp.tool("get_tests", description="Get tests for a run")
    def get_tests(
        run_id: int,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        label_id: Optional[Union[int, List[int], str]] = None,
        section_id: Optional[int] = None,
    ) -> List[Dict]:
        """Get tests for a run with optional section filtering."""
        tests_data = client.get_tests(
            run_id,
            status_id=status_id,
            limit=limit,
            offset=offset,
            label_id=label_id,
        )
        
        # TestRail API returns a dictionary with 'tests' list and pagination info
        # if 'limit' or 'offset' is used, otherwise it returns a list of tests directly
        # depending on the client implementation. 
        # Checking how client.get_tests is implemented...
        
        # Looking back at testrail_mcp/client/tests.py:
        # def get_tests(self, run_id: int, ...) -> Dict:
        #     ...
        #     return self._send_request('GET', uri)
        
        # Most TestRail GET list endpoints return a list of objects directly 
        # unless they are paginated with 'limit'/'offset' in which case they return {'tests': [...], 'size': ..., ...}
        
        tests_list = tests_data.get('tests', []) if isinstance(tests_data, dict) else tests_data
        
        if section_id is not None:
            # 1. Get run info to know project and suite
            run = client.get_run(run_id)
            project_id = run['project_id']
            suite_id = run.get('suite_id')
            
            # 2. Get cases in that section
            cases_data = client.get_cases(project_id, suite_id=suite_id, section_id=section_id)
            cases_list = cases_data.get('cases', []) if isinstance(cases_data, dict) else cases_data
            case_ids = {case['id'] for case in cases_list}
            
            # 3. Filter tests by case_ids
            tests_list = [t for t in tests_list if t['case_id'] in case_ids]
            
        return tests_list

    @mcp.tool("update_test", description="Update labels assigned to a test")
    def update_test(test_id: int, labels: List[Union[int, str]]) -> Dict:
        return client.update_test(test_id, labels)

    @mcp.tool("update_tests", description="Update labels assigned to multiple tests")
    def update_tests(test_ids: List[int], labels: List[Union[int, str]]) -> Dict:
        return client.update_tests(test_ids, labels)


def register_resources(mcp: FastMCP, client: TestRailClient) -> None:
    @mcp.resource("testrail://test/{test_id}")
    def get_test_resource(test_id: int) -> Dict:
        return client.get_test(test_id)
