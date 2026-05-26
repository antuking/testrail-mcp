"""Milestones API mixin."""
from typing import Dict, Optional


class MilestonesAPI:
    """Milestones API methods."""

    def get_milestone(self, milestone_id: int) -> Dict:
        """Get a milestone by ID."""
        return self._send_request('GET', f'get_milestone/{milestone_id}')

    def get_milestones(
        self,
        project_id: int,
        is_completed: Optional[bool] = None,
        is_started: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get milestones for a project."""
        params = {
            'is_completed': 1 if is_completed is True else 0 if is_completed is False else None,
            'is_started': 1 if is_started is True else 0 if is_started is False else None,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_milestones/{project_id}', params)
        return self._send_request('GET', uri)

    def add_milestone(self, project_id: int, data: Dict) -> Dict:
        """Add a new milestone."""
        return self._send_request('POST', f'add_milestone/{project_id}', data)

    def update_milestone(self, milestone_id: int, data: Dict) -> Dict:
        """Update an existing milestone."""
        return self._send_request('POST', f'update_milestone/{milestone_id}', data)

    def delete_milestone(self, milestone_id: int) -> Dict:
        """Delete a milestone."""
        return self._send_request('POST', f'delete_milestone/{milestone_id}')
