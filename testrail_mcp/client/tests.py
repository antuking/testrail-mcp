"""Tests API mixin."""
from typing import Dict, List, Optional, Union, Any


class TestsAPI:
    """Tests API methods."""

    def get_test(self, test_id: int, with_data: Optional[str] = None) -> Dict:
        """Get a test by ID."""
        params = {'with_data': with_data}
        uri = self._append_query_params(f'get_test/{test_id}', params)
        return self._send_request('GET', uri)

    def get_tests(
        self,
        run_id: int,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        label_id: Optional[Union[int, List[int], str]] = None,
    ) -> Dict:
        """Get tests for a run."""
        params = {
            'status_id': status_id,
            'limit': limit,
            'offset': offset,
            'label_id': label_id,
        }
        uri = self._append_query_params(f'get_tests/{run_id}', params)
        return self._send_request('GET', uri)

    def update_test(self, test_id: int, labels: List[Union[int, str]]) -> Dict:
        """Update labels assigned to a test."""
        data: Dict[str, Any] = {'labels': labels}
        return self._send_request('POST', f'update_test/{test_id}', data)

    def update_tests(self, test_ids: List[int], labels: List[Union[int, str]]) -> Dict:
        """Update labels assigned to multiple tests."""
        data: Dict[str, Any] = {
            'test_ids': test_ids,
            'labels': labels,
        }
        return self._send_request('POST', 'update_tests', data)
