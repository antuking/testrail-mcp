"""Groups API mixin."""
from typing import Dict, List


class GroupsAPI:
    """Groups API methods."""

    def get_group(self, group_id: int) -> Dict:
        """Get a group by ID."""
        return self._send_request('GET', f'get_group/{group_id}')

    def get_groups(self) -> List[Dict]:
        """Get all groups."""
        return self._send_request('GET', 'get_groups')

    def add_group(self, data: Dict) -> Dict:
        """Add a new group."""
        return self._send_request('POST', 'add_group', data)

    def update_group(self, group_id: int, data: Dict) -> Dict:
        """Update an existing group."""
        return self._send_request('POST', f'update_group/{group_id}', data)

    def delete_group(self, group_id: int) -> Dict:
        """Delete a group."""
        return self._send_request('POST', f'delete_group/{group_id}')
