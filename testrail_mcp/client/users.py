"""Users API mixin."""
from typing import Dict, List, Optional


class UsersAPI:
    """Users API methods."""

    def get_user(self, user_id: int) -> Dict:
        """Get a user by ID."""
        return self._send_request('GET', f'get_user/{user_id}')

    def get_current_user(self, user_id: int) -> Dict:
        """Get the current user by ID."""
        return self._send_request('GET', f'get_current_user/{user_id}')

    def get_user_by_email(self, email: str) -> Dict:
        """Get a user by email address."""
        uri = self._append_query_params('get_user_by_email', {'email': email})
        return self._send_request('GET', uri)

    def get_users(self, project_id: Optional[int] = None) -> List[Dict]:
        """Get users (optionally for a project)."""
        if project_id is None:
            return self._send_request('GET', 'get_users')
        return self._send_request('GET', f'get_users/{project_id}')

    def add_user(self, data: Dict) -> Dict:
        """Add a new user."""
        return self._send_request('POST', 'add_user', data)

    def update_user(self, user_id: int, data: Dict) -> Dict:
        """Update an existing user."""
        return self._send_request('POST', f'update_user/{user_id}', data)
