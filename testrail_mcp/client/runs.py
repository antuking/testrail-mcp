"""Runs API mixin."""
from typing import Dict, List


class RunsAPI:
    """Runs API methods."""

    def get_run(self, run_id: int) -> Dict:
        """Get a test run by ID."""
        return self._send_request('GET', f'get_run/{run_id}')

    def get_runs(self, project_id: int) -> List[Dict]:
        """Get all test runs for a project."""
        return self._send_request('GET', f'get_runs/{project_id}')

    def add_run(self, project_id: int, data: Dict) -> Dict:
        """Add a new test run.

        Supported data fields: suite_id, name, description, milestone_id,
        assignedto_id, include_all, case_ids, refs.
        """
        return self._send_request('POST', f'add_run/{project_id}', data)

    def update_run(self, run_id: int, data: Dict) -> Dict:
        """Update an existing test run.

        Supported data fields: name, description, milestone_id,
        assignedto_id, include_all, case_ids, refs.
        """
        return self._send_request('POST', f'update_run/{run_id}', data)

    def close_run(self, run_id: int) -> Dict:
        """Close a test run."""
        return self._send_request('POST', f'close_run/{run_id}')

    def delete_run(self, run_id: int) -> Dict:
        """Delete a test run."""
        return self._send_request('POST', f'delete_run/{run_id}')
