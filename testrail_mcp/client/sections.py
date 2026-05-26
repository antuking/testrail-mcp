"""Sections API mixin."""
from typing import Dict, Optional


class SectionsAPI:
    """Sections API methods."""

    def get_section(self, section_id: int) -> Dict:
        """Get a specific section."""
        return self._send_request('GET', f'get_section/{section_id}')

    def get_sections(
        self,
        project_id: int,
        suite_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get all sections for a project."""
        params = {
            'suite_id': suite_id,
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_sections/{project_id}', params)
        return self._send_request('GET', uri)

    def add_section(self, project_id: int, data: Dict) -> Dict:
        """Add a new section."""
        return self._send_request('POST', f'add_section/{project_id}', data)

    def update_section(self, section_id: int, data: Dict) -> Dict:
        """Update an existing section."""
        return self._send_request('POST', f'update_section/{section_id}', data)

    def delete_section(self, section_id: int, soft: bool) -> Dict:
        """Delete an existing section."""
        url = f'delete_section/{section_id}'
        if soft:
            url = f'delete_section/{section_id}?soft=1'
        return self._send_request('POST', url)

    def move_section(self, section_id: int, data: Dict) -> Dict:
        """Move a section to a different parent or position."""
        return self._send_request('POST', f'move_section/{section_id}', data)
