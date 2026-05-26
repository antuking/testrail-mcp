"""Statuses API mixin."""
from typing import Dict, List


class StatusesAPI:
    """Statuses API methods."""

    def get_statuses(self) -> List[Dict]:
        """Get all test statuses."""
        return self._send_request('GET', 'get_statuses')

    def get_case_statuses(self) -> List[Dict]:
        """Get all case statuses."""
        return self._send_request('GET', 'get_case_statuses')

    def get_status_id_by_name(self, name: str) -> int:
        """Get the ID of a test status by its name (label).

        Args:
            name: The name of the status (e.g., 'Passed', 'Retest').

        Returns:
            The status ID.

        Raises:
            ValueError: If the status name is not found.
        """
        statuses = self.get_statuses()
        for status in statuses:
            if status['label'].lower() == name.lower() or status['name'].lower() == name.lower():
                return status['id']
        raise ValueError(f"Status '{name}' not found. Available: {[s['label'] for s in statuses]}")
