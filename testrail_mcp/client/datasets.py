"""Datasets API mixin."""
from typing import Dict, List


class DatasetsAPI:
    """Datasets API methods."""

    def get_datasets(self, project_id: int) -> List[Dict]:
        """Get all datasets for a project."""
        return self._send_request('GET', f'get_datasets/{project_id}')

    def get_dataset(self, dataset_id: int) -> Dict:
        """Get a dataset by ID."""
        return self._send_request('GET', f'get_dataset/{dataset_id}')

    def add_dataset(self, project_id: int, data: Dict) -> Dict:
        """Add a new dataset."""
        return self._send_request('POST', f'add_dataset/{project_id}', data)

    def update_dataset(self, dataset_id: int, data: Dict) -> Dict:
        """Update an existing dataset."""
        return self._send_request('POST', f'update_dataset/{dataset_id}', data)

    def delete_dataset(self, dataset_id: int) -> Dict:
        """Delete a dataset."""
        return self._send_request('POST', f'delete_dataset/{dataset_id}')
