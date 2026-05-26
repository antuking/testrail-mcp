"""Configurations API mixin."""
from typing import Dict, List


class ConfigurationsAPI:
    """Configurations API methods."""

    def get_configs(self, project_id: int) -> List[Dict]:
        """Get all configuration groups and configurations for a project."""
        return self._send_request('GET', f'get_configs/{project_id}')

    def add_config_group(self, project_id: int, name: str) -> Dict:
        """Add a new configuration group."""
        return self._send_request('POST', f'add_config_group/{project_id}', {'name': name})

    def add_config(self, config_group_id: int, name: str) -> Dict:
        """Add a new configuration to a group."""
        return self._send_request('POST', f'add_config/{config_group_id}', {'name': name})

    def update_config_group(self, config_group_id: int, name: str) -> Dict:
        """Update an existing configuration group."""
        return self._send_request('POST', f'update_config_group/{config_group_id}', {'name': name})

    def update_config(self, config_id: int, name: str) -> Dict:
        """Update an existing configuration."""
        return self._send_request('POST', f'update_config/{config_id}', {'name': name})

    def delete_config_group(self, config_group_id: int) -> Dict:
        """Delete a configuration group."""
        return self._send_request('POST', f'delete_config_group/{config_group_id}')

    def delete_config(self, config_id: int) -> Dict:
        """Delete a configuration."""
        return self._send_request('POST', f'delete_config/{config_id}')
