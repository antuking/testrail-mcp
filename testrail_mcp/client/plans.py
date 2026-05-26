"""Plans API mixin."""
from typing import Dict, Optional, Union, List


class PlansAPI:
    """Plans API methods."""

    def get_plan(self, plan_id: int) -> Dict:
        """Get a test plan by ID."""
        return self._send_request('GET', f'get_plan/{plan_id}')

    def get_plans(
        self,
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        is_completed: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        milestone_id: Optional[Union[int, List[int], str]] = None,
    ) -> Dict:
        """Get test plans for a project."""
        params = {
            'created_after': created_after,
            'created_before': created_before,
            'created_by': created_by,
            'is_completed': 1 if is_completed is True else 0 if is_completed is False else None,
            'limit': limit,
            'offset': offset,
            'milestone_id': milestone_id,
        }
        uri = self._append_query_params(f'get_plans/{project_id}', params)
        return self._send_request('GET', uri)

    def add_plan(self, project_id: int, data: Dict) -> Dict:
        """Add a new test plan."""
        return self._send_request('POST', f'add_plan/{project_id}', data)

    def add_plan_entry(self, plan_id: int, data: Dict) -> Dict:
        """Add a new test plan entry."""
        return self._send_request('POST', f'add_plan_entry/{plan_id}', data)

    def add_run_to_plan_entry(self, plan_id: int, entry_id: str, data: Dict) -> Dict:
        """Add a new run to a plan entry."""
        return self._send_request('POST', f'add_run_to_plan_entry/{plan_id}/{entry_id}', data)

    def update_plan(self, plan_id: int, data: Dict) -> Dict:
        """Update an existing test plan."""
        return self._send_request('POST', f'update_plan/{plan_id}', data)

    def update_run_in_plan_entry(self, run_id: int, data: Dict) -> Dict:
        """Update a run in a plan entry."""
        return self._send_request('POST', f'update_run_in_plan_entry/{run_id}', data)

    def close_plan(self, plan_id: int) -> Dict:
        """Close a test plan."""
        return self._send_request('POST', f'close_plan/{plan_id}')

    def delete_plan(self, plan_id: int) -> Dict:
        """Delete a test plan."""
        return self._send_request('POST', f'delete_plan/{plan_id}')

    def delete_plan_entry(self, plan_id: int, entry_id: str) -> Dict:
        """Delete a plan entry."""
        return self._send_request('POST', f'delete_plan_entry/{plan_id}/{entry_id}')

    def delete_run_from_plan_entry(self, run_id: int) -> Dict:
        """Delete a run from a plan entry."""
        return self._send_request('POST', f'delete_run_from_plan_entry/{run_id}')
