"""Shared base client for TestRail API calls."""
import base64
import json
from typing import Dict, List, Any, Optional, Union

import requests


class BaseClient:
    """Base TestRail API client with auth and request helpers."""

    def __init__(self, base_url: str, username: str, api_key: str):
        """
        Initialize the TestRail API client.

        Args:
            base_url: The URL of your TestRail instance (e.g., https://example.testrail.io/)
            username: Your TestRail username/email
            api_key: Your TestRail API key
        """
        self.username = username
        self.api_key = api_key

        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url + 'index.php?/api/v2/'

        self.session = requests.Session()
        auth = str(
            base64.b64encode(bytes(f'{username}:{api_key}', 'utf-8')),
            'ascii',
        ).strip()
        self.session.headers.update({
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
        })

    def _send_request(self, method: str, uri: str, data: Optional[Dict] = None) -> Any:
        """
        Send a request to the TestRail API.

        Args:
            method: HTTP method (GET, POST, etc.)
            uri: API endpoint URI
            data: Request data for POST/PUT requests

        Returns:
            Response data from TestRail

        Raises:
            Exception: If the request fails
        """
        url = self.base_url + uri

        if method.upper() == 'GET':
            response = self.session.get(url)
        elif method.upper() == 'POST':
            response = self.session.post(url, data=json.dumps(data) if data else None)
        elif method.upper() == 'PUT':
            response = self.session.put(url, data=json.dumps(data) if data else None)
        elif method.upper() == 'DELETE':
            response = self.session.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code >= 300:
            try:
                error = response.json()
            except Exception:
                error = response.text
            raise Exception(f"TestRail API returned HTTP {response.status_code}: {error}")

        return response.json() if response.content else {}

    def _append_query_params(self, uri: str, params: Optional[Dict[str, Any]]) -> str:
        """Append query params to a TestRail API URI using TestRail's '&' style."""
        if not params:
            return uri
        parts: List[str] = []
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                value = ','.join(str(v) for v in value)
            parts.append(f"{key}={value}")
        if not parts:
            return uri
        return f"{uri}&{'&'.join(parts)}"
