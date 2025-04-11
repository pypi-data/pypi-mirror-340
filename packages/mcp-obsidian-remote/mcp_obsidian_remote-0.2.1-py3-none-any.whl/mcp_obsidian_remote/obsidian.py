import logging
import os
import requests
import urllib.parse
import json # Added for error handling
from typing import Any, Dict, List, Optional

# Custom Exceptions
class ObsidianError(Exception):
    """Base exception for Obsidian client errors."""
    pass

class ObsidianAPIError(ObsidianError):
    """Raised for errors reported by the Obsidian API."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Obsidian API Error {code}: {message}")

class ObsidianConnectionError(ObsidianError):
    """Raised for network or connection issues."""
    pass

logger = logging.getLogger(__name__) # Use module logger
class Obsidian():
    def __init__(
            self,
            api_key: str,
            protocol: Optional[str] = "http",
            host: Optional[str] = "127.0.0.1",
            port: Optional[int] = 27124,
            verify_ssl: bool = False,
            timeout: tuple[int, int] = (5, 10) # Increased connect timeout slightly
        ):

        self.protocol = protocol
        self.host = host
        self.port = port
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self._base_url = f'{self.protocol}://{self.host}:{self.port}'

        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})
        self.session.verify = self.verify_ssl

        logger.info(f"Obsidian client initialized for {self._base_url}")

    def get_base_url(self) -> str:
        # Kept for potential external use, but internally use self._base_url
        return self._base_url

    # _get_headers is no longer needed as headers are set on the session

    def _safe_call(self, make_request_func) -> Any:
        """Wraps request calls with error handling and logging."""
        try:
            # The function passed here should prepare and execute the request using self.session
            response = make_request_func()
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            # Successfully completed request
            # Check if response has content before trying to parse JSON or text
            if response.status_code == 204: # No Content
                 return None
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                # Assume text for other types like text/markdown, text/plain
                return response.text

        except requests.HTTPError as e:
            # Log details from the request if available
            request_details = f"{e.request.method} {e.request.url}" if e.request else "Unknown Request"
            status_code = e.response.status_code if e.response is not None else "N/A"
            logging.error(f"HTTP Error calling Obsidian API: {request_details} - Status: {status_code}")
            try:
                # Try to get specific error details from response body
                error_data = e.response.json() if e.response and e.response.content else {}
                code = error_data.get('errorCode', status_code) # Use HTTP status if no specific code
                message = error_data.get('message', e.response.reason if e.response is not None else 'Unknown API error')
                raise ObsidianAPIError(code, message) from e
            except (json.JSONDecodeError, AttributeError):
                # Fallback if response is not JSON or response object is weird
                 error_message = str(e)
                 if e.response is not None:
                     error_message = f"{e.response.status_code} {e.response.reason}"
                 raise ObsidianAPIError(status_code, error_message) from e

        except requests.exceptions.RequestException as e:
            # Catches connection errors, timeouts, etc.
            request_details = f"{e.request.method} {e.request.url}" if e.request else "Unknown Request"
            logging.error(f"Request Exception calling Obsidian API: {request_details} - Error: {e}")
            raise ObsidianConnectionError(f"Connection failed for {request_details}: {str(e)}") from e
        except Exception as e:
            # Catch unexpected errors during request processing
            logging.exception(f"Unexpected error during Obsidian API call: {e}")
            raise ObsidianError(f"An unexpected error occurred: {e}") from e


    def list_files_in_vault(self) -> List[str]:
        url = f"{self._base_url}/vault/"
        def call_fn():
            return self.session.get(url, timeout=self.timeout)
        # The API returns {'files': [...]}
        result = self._safe_call(call_fn)
        return result.get('files', []) if isinstance(result, dict) else []

    def list_files_in_dir(self, dirpath: str) -> List[str]:
        encoded_dirpath = urllib.parse.quote(dirpath.strip('/'))
        url = f"{self._base_url}/vault/{encoded_dirpath}/"
        def call_fn():
            return self.session.get(url, timeout=self.timeout)
        result = self._safe_call(call_fn)
        return result.get('files', []) if isinstance(result, dict) else []

    def get_file_contents(self, filepath: str) -> str:
        encoded_filepath = urllib.parse.quote(filepath)
        url = f"{self._base_url}/vault/{encoded_filepath}"
        def call_fn():
            # Expecting text/markdown or text/plain
            return self.session.get(url, timeout=self.timeout)
        content = self._safe_call(call_fn)
        return content if isinstance(content, str) else "" # Ensure string return

    def get_batch_file_contents(self, filepaths: list[str]) -> str:
        """Get contents of multiple files and concatenate them with headers."""
        result = []
        for filepath in filepaths:
            try:
                content = self.get_file_contents(filepath)
                result.append(f"# {filepath}\n\n{content}\n\n---\n\n")
            except ObsidianError as e: # Catch specific Obsidian errors
                logging.warning(f"Failed to get content for file '{filepath}': {e}")
                result.append(f"# {filepath}\n\nError reading file: {str(e)}\n\n---\n\n")
            except Exception as e: # Catch other unexpected errors
                logging.exception(f"Unexpected error getting content for file '{filepath}': {e}")
                result.append(f"# {filepath}\n\nUnexpected error reading file: {str(e)}\n\n---\n\n")

    def search(self, query: str, context_length: int = 100) -> List[Dict[str, Any]]:
        url = f"{self._base_url}/search/simple/"
        params = {'query': query, 'contextLength': context_length}
        def call_fn():
            # This endpoint uses POST according to original code
            return self.session.post(url, params=params, timeout=self.timeout)
        return self._safe_call(call_fn) or [] # Return empty list on failure/no content

    def append_content(self, filepath: str, content: str) -> None:
        encoded_filepath = urllib.parse.quote(filepath)
        url = f"{self._base_url}/vault/{encoded_filepath}"
        headers = {'Content-Type': 'text/markdown'}
        def call_fn():
            return self.session.post(url, headers=headers, data=content.encode('utf-8'), timeout=self.timeout)
        self._safe_call(call_fn) # Returns None on success (204)

    def patch_content(self, filepath: str, operation: str, target_type: str, target: str, content: str) -> None:
        encoded_filepath = urllib.parse.quote(filepath)
        url = f"{self._base_url}/vault/{encoded_filepath}"
        headers = {
            'Content-Type': 'text/markdown',
            'Operation': operation,
            'Target-Type': target_type,
            'Target': urllib.parse.quote(target) # Target also needs encoding
        }
        def call_fn():
            return self.session.patch(url, headers=headers, data=content.encode('utf-8'), timeout=self.timeout)
        self._safe_call(call_fn) # Returns None on success (204)

    def delete_file(self, filepath: str) -> None:
        encoded_filepath = urllib.parse.quote(filepath)
        url = f"{self._base_url}/vault/{encoded_filepath}"
        def call_fn():
            return self.session.delete(url, timeout=self.timeout)
        self._safe_call(call_fn) # Returns None on success (204)

    def search_json(self, query: dict) -> Any: # Return type depends heavily on query
        url = f"{self._base_url}/search/"
        headers = {'Content-Type': 'application/vnd.olrapi.jsonlogic+json'}
        def call_fn():
            return self.session.post(url, headers=headers, json=query, timeout=self.timeout)
        return self._safe_call(call_fn) # Return raw JSON response
    def get_periodic_note(self, period: str) -> str:
        url = f"{self._base_url}/periodic/{period}/"
        def call_fn():
             # Expecting text/markdown or text/plain
            return self.session.get(url, timeout=self.timeout)
        content = self._safe_call(call_fn)
        return content if isinstance(content, str) else "" # Ensure string return

    def get_recent_periodic_notes(self, period: str, limit: int = 5, include_content: bool = False) -> List[Dict[str, Any]]:
        url = f"{self._base_url}/periodic/{period}/recent"
        params = {"limit": limit, "includeContent": include_content}
        def call_fn():
            return self.session.get(url, params=params, timeout=self.timeout)
        return self._safe_call(call_fn) or [] # Return empty list on failure/no content

    def get_recent_changes(self, limit: int = 10, days: int = 90) -> List[Dict[str, Any]]:
        url = f"{self._base_url}/search/"
        headers = {'Content-Type': 'application/vnd.olrapi.dataview.dql+txt'}
        query_lines = [
            "TABLE file.mtime",
            f"WHERE file.mtime >= date(today) - dur({days} days)",
            "SORT file.mtime DESC",
            f"LIMIT {limit}"
        ]
        dql_query = "\n".join(query_lines)
        def call_fn():
            return self.session.post(url, headers=headers, data=dql_query.encode('utf-8'), timeout=self.timeout)
        return self._safe_call(call_fn) or [] # Return empty list on failure/no content

