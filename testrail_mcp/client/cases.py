"""Cases API mixin."""
from typing import Dict, List, Any, Optional, Union


class CasesAPI:
    """Cases API methods."""
    def get_case_types(self) -> List[Dict]:
        """Get all available case types."""
        return self._send_request('GET', 'get_case_types')

    def get_case_fields(self) -> List[Dict]:
        """Get all available test case custom fields."""
        return self._send_request('GET', 'get_case_fields')

    def add_case_field(self, data: Dict) -> Dict:
        """Add a new test case custom field."""
        return self._send_request('POST', 'add_case_field', data)

    def get_case(self, case_id: int) -> Dict:
        """Get a test case by ID."""
        return self._send_request('GET', f'get_case/{case_id}')

    def get_cases(
        self,
        project_id: int,
        suite_id: Optional[int] = None,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        filter: Optional[str] = None,
        limit: Optional[int] = None,
        milestone_id: Optional[Union[int, List[int], str]] = None,
        offset: Optional[int] = None,
        priority_id: Optional[Union[int, List[int], str]] = None,
        refs: Optional[str] = None,
        section_id: Optional[int] = None,
        template_id: Optional[Union[int, List[int], str]] = None,
        type_id: Optional[Union[int, List[int], str]] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[Union[int, List[int], str]] = None,
        label_id: Optional[Union[int, List[int], str]] = None,
    ) -> Dict:
        """Get test cases for a project/suite with optional filters."""
        params = {
            'suite_id': suite_id,
            'created_after': created_after,
            'created_before': created_before,
            'created_by': created_by,
            'filter': filter,
            'limit': limit,
            'milestone_id': milestone_id,
            'offset': offset,
            'priority_id': priority_id,
            'refs': refs,
            'section_id': section_id,
            'template_id': template_id,
            'type_id': type_id,
            'updated_after': updated_after,
            'updated_before': updated_before,
            'updated_by': updated_by,
            'label_id': label_id,
        }
        uri = self._append_query_params(f'get_cases/{project_id}', params)
        return self._send_request('GET', uri)

    def add_case(self, section_id: int, data: Dict) -> Dict:
        """Add a new test case."""
        return self._send_request('POST', f'add_case/{section_id}', data)

    def update_case(self, case_id: int, data: Dict) -> Dict:
        """Update an existing test case."""
        return self._send_request('POST', f'update_case/{case_id}', data)

    def delete_case(self, case_id: int, soft: Optional[bool] = None) -> Dict:
        """Delete a test case."""
        params = {'soft': 1 if soft else None}
        uri = self._append_query_params(f'delete_case/{case_id}', params)
        return self._send_request('POST', uri)

    def get_history_for_case(
        self,
        case_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get edit history for a test case."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_history_for_case/{case_id}', params)
        return self._send_request('GET', uri)

    def copy_cases_to_section(
        self,
        section_id: int,
        case_ids: Optional[List[int]] = None,
    ) -> Dict:
        """Copy cases to another section."""
        data: Dict[str, Any] = {}
        if case_ids is not None:
            data['case_ids'] = case_ids
        return self._send_request('POST', f'copy_cases_to_section/{section_id}', data)

    def update_cases(self, suite_id: int, data: Dict) -> Dict:
        """Update multiple test cases with the same values."""
        return self._send_request('POST', f'update_cases/{suite_id}', data)

    def move_cases_to_section(
        self,
        section_id: int,
        suite_id: int,
        case_ids: List[int],
    ) -> Dict:
        """Move cases to another suite/section."""
        data = {
            'suite_id': suite_id,
            'case_ids': case_ids,
        }
        return self._send_request('POST', f'move_cases_to_section/{section_id}', data)

    def delete_cases(
        self,
        suite_id: int,
        project_id: int,
        case_ids: List[int],
        soft: Optional[bool] = None,
    ) -> Dict:
        """Delete multiple test cases from a project/suite."""
        params = {'soft': 1 if soft else None}
        uri = self._append_query_params(f'delete_cases/{suite_id}', params)
        data = {
            'project_id': project_id,
            'case_ids': case_ids,
        }
        return self._send_request('POST', uri, data)
