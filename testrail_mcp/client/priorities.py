"""Priorities API mixin."""
from typing import Dict, List


class PrioritiesAPI:
    """Priorities API methods."""

    def get_priorities(self) -> List[Dict]:
        """Get all available test case priorities."""
        return self._send_request('GET', 'get_priorities')
