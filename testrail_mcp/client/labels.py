"""Labels API mixin."""
from typing import Dict, Optional


class LabelsAPI:
    """Labels API methods."""

    def get_label(self, label_id: int) -> Dict:
        """Get a label by ID."""
        return self._send_request('GET', f'get_label/{label_id}')

    def get_labels(
        self,
        project_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict:
        """Get labels for a project."""
        params = {
            'offset': offset,
            'limit': limit,
        }
        uri = self._append_query_params(f'get_labels/{project_id}', params)
        return self._send_request('GET', uri)

    def update_label(self, label_id: int, project_id: int, title: str) -> Dict:
        """Update an existing label."""
        data = {
            'project_id': project_id,
            'title': title,
        }
        return self._send_request('POST', f'update_label/{label_id}', data)
