"""Shared Steps API mixin."""
from typing import Dict, Optional, Union, List


class SharedStepsAPI:
    """Shared Steps API methods."""

    def get_shared_step(self, shared_step_id: int) -> Dict:
        """Get a shared step by ID."""
        return self._send_request('GET', f'get_shared_step/{shared_step_id}')

    def get_shared_step_history(
        self,
        shared_step_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get history for a shared step."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(
            f'get_shared_step_history/{shared_step_id}',
            params,
        )
        return self._send_request('GET', uri)

    def get_shared_steps(
        self,
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[Union[int, List[int], str]] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[Union[int, List[int], str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get shared steps for a project."""
        params = {
            'created_after': created_after,
            'created_before': created_before,
            'created_by': created_by,
            'updated_after': updated_after,
            'updated_before': updated_before,
            'updated_by': updated_by,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_shared_steps/{project_id}', params)
        return self._send_request('GET', uri)

    def add_shared_step(self, project_id: int, data: Dict) -> Dict:
        """Add a shared step."""
        return self._send_request('POST', f'add_shared_step/{project_id}', data)

    def update_shared_step(self, shared_step_id: int, data: Dict) -> Dict:
        """Update a shared step."""
        return self._send_request('POST', f'update_shared_step/{shared_step_id}', data)

    def delete_shared_step(self, shared_step_id: int) -> Dict:
        """Delete a shared step."""
        return self._send_request('POST', f'delete_shared_step/{shared_step_id}')
