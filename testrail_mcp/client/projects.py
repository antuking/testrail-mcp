"""Projects API mixin."""
from typing import Dict, List


class ProjectsAPI:
    """Projects API methods."""

    def get_project(self, project_id: int) -> Dict:
        """Get a project by ID."""
        return self._send_request('GET', f'get_project/{project_id}')

    def get_projects(self) -> List[Dict]:
        """Get all projects."""
        return self._send_request('GET', 'get_projects')

    def add_project(self, data: Dict) -> Dict:
        """Add a new project."""
        return self._send_request('POST', 'add_project', data)

    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update an existing project."""
        return self._send_request('POST', f'update_project/{project_id}', data)

    def delete_project(self, project_id: int) -> Dict:
        """Delete a project."""
        return self._send_request('POST', f'delete_project/{project_id}')
