"""Attachments API mixin."""
from typing import Dict, Optional, Any
import os


class AttachmentsAPI:
    """Attachments API methods."""

    def _post_attachment(self, uri: str, file_path: str, file_name: Optional[str] = None,
                         content_type: Optional[str] = None) -> Dict:
        """Upload an attachment using multipart/form-data."""
        url = self.base_url + uri
        headers = dict(self.session.headers)
        headers.pop('Content-Type', None)
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as handle:
            if content_type:
                files = {'attachment': (file_name, handle, content_type)}
            else:
                files = {'attachment': (file_name, handle)}
            response = self.session.post(url, files=files, headers=headers)
        if response.status_code >= 300:
            try:
                error = response.json()
            except Exception:
                error = response.text
            raise Exception(f"TestRail API returned HTTP {response.status_code}: {error}")
        return response.json() if response.content else {}

    def add_attachment_to_case(
        self,
        case_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        """Add an attachment to a test case."""
        return self._post_attachment(
            f'add_attachment_to_case/{case_id}',
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    def add_attachment_to_plan(
        self,
        plan_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        """Add an attachment to a test plan."""
        return self._post_attachment(
            f'add_attachment_to_plan/{plan_id}',
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    def add_attachment_to_plan_entry(
        self,
        plan_id: int,
        entry_id: str,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        """Add an attachment to a test plan entry."""
        return self._post_attachment(
            f'add_attachment_to_plan_entry/{plan_id}/{entry_id}',
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    def add_attachment_to_result(
        self,
        result_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        """Add an attachment to a test result."""
        return self._post_attachment(
            f'add_attachment_to_result/{result_id}',
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    def add_attachment_to_run(
        self,
        run_id: int,
        file_path: str,
        file_name: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Dict:
        """Add an attachment to a test run."""
        return self._post_attachment(
            f'add_attachment_to_run/{run_id}',
            file_path=file_path,
            file_name=file_name,
            content_type=content_type,
        )

    def get_attachments_for_case(
        self,
        case_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get attachments for a test case."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_attachments_for_case/{case_id}', params)
        return self._send_request('GET', uri)

    def get_attachments_for_plan(
        self,
        plan_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get attachments for a test plan."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_attachments_for_plan/{plan_id}', params)
        return self._send_request('GET', uri)

    def get_attachments_for_plan_entry(self, plan_id: int, entry_id: str) -> Dict:
        """Get attachments for a test plan entry."""
        return self._send_request('GET', f'get_attachments_for_plan_entry/{plan_id}/{entry_id}')

    def get_attachments_for_run(
        self,
        run_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict:
        """Get attachments for a test run."""
        params = {
            'limit': limit,
            'offset': offset,
        }
        uri = self._append_query_params(f'get_attachments_for_run/{run_id}', params)
        return self._send_request('GET', uri)

    def get_attachments_for_test(self, test_id: int) -> Dict:
        """Get attachments for a test."""
        return self._send_request('GET', f'get_attachments_for_test/{test_id}')

    def get_attachment(self, attachment_id: int) -> bytes:
        """Get a raw attachment by ID."""
        url = self.base_url + f'get_attachment/{attachment_id}'
        response = self.session.get(url)
        if response.status_code >= 300:
            try:
                error = response.json()
            except Exception:
                error = response.text
            raise Exception(f"TestRail API returned HTTP {response.status_code}: {error}")
        return response.content

    def delete_attachment(self, attachment_id: int) -> Dict:
        """Delete an attachment."""
        return self._send_request('POST', f'delete_attachment/{attachment_id}')
