"""Suites API mixin."""
from typing import Dict, Optional


class SuitesAPI:
    """Suites API methods."""

    def get_suite(self, suite_id: int) -> Dict:
        """Get a test suite by ID."""
        return self._send_request('GET', f'get_suite/{suite_id}')

    def get_suites(
        self,
        project_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get test suites for a project."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_suites/{project_id}', params)
        return self._send_request('GET', uri)

    def add_suite(self, project_id: int, data: Dict) -> Dict:
        """Add a new test suite."""
        return self._send_request('POST', f'add_suite/{project_id}', data)

    def update_suite(self, suite_id: int, data: Dict) -> Dict:
        """Update an existing test suite."""
        return self._send_request('POST', f'update_suite/{suite_id}', data)

    def delete_suite(self, suite_id: int, soft: Optional[bool] = None) -> Dict:
        """Delete a test suite."""
        params = {'soft': 1 if soft else None}
        uri = self._append_query_params(f'delete_suite/{suite_id}', params)
        return self._send_request('POST', uri)
