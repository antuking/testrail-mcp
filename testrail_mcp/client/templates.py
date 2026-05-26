"""Templates API mixin."""
from typing import Dict, List


class TemplatesAPI:
    """Templates API methods."""

    def get_templates(self, project_id: int) -> List[Dict]:
        """Get all test case templates for a project."""
        return self._send_request('GET', f'get_templates/{project_id}')
