"""Results API mixin."""
from typing import Dict, List, Optional, Union


class ResultsAPI:
    """Results API methods."""

    def get_result_fields(self) -> List[Dict]:
        """Get all available test result custom fields."""
        return self._send_request('GET', 'get_result_fields')

    def get_results(
        self,
        test_id: int,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get all results for a test."""
        params = {
            'defects_filter': defects_filter,
            'status_id': status_id,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_results/{test_id}', params)
        return self._send_request('GET', uri)

    def get_results_for_case(
        self,
        run_id: int,
        case_id: int,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get all results for a run + case combination."""
        params = {
            'defects_filter': defects_filter,
            'status_id': status_id,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_results_for_case/{run_id}/{case_id}', params)
        return self._send_request('GET', uri)

    def get_results_for_run(
        self,
        run_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        defects_filter: Optional[str] = None,
        status_id: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get all results for a run."""
        params = {
            'created_after': created_after,
            'created_before': created_before,
            'created_by': created_by,
            'defects_filter': defects_filter,
            'status_id': status_id,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_results_for_run/{run_id}', params)
        return self._send_request('GET', uri)

    def add_result(self, test_id: int, data: Dict) -> Dict:
        """Add a new result for a test."""
        return self._send_request('POST', f'add_result/{test_id}', data)

    def add_result_for_case(self, run_id: int, case_id: int, data: Dict) -> Dict:
        """Add a new result for a run + case combination."""
        return self._send_request('POST', f'add_result_for_case/{run_id}/{case_id}', data)

    def add_results(self, run_id: int, data: Dict) -> List[Dict]:
        """Add multiple results for a run."""
        return self._send_request('POST', f'add_results/{run_id}', data)

    def add_results_for_cases(self, run_id: int, data: Dict) -> List[Dict]:
        """Add results for specific cases in a run."""
        return self._send_request('POST', f'add_results_for_cases/{run_id}', data)
