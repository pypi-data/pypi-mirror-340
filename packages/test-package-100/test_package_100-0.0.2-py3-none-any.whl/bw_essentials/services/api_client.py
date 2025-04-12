"""
Generic API client module for making external HTTP requests with structured logging.

This wrapper provides reusable methods to send GET, POST, and PUT requests with consistent headers,
tracing (via x-request-id), and tenant context for multitenant systems. It logs key request and response
information and handles exceptions with logging.
"""

import logging
import os

import requests
from typing import Optional, Dict, Any

from asgi_correlation_id import correlation_id

from bw_essentials.contexts.contexts import get_request_id, get_tenant_id

logger = logging.getLogger(__name__)


class ApiClient:
    """
    A reusable API client for external service calls with contextual logging.

    Args:
        user (str): The user or system initiating the request.
        headers (Optional[Dict[str, str]]): Initial HTTP headers to be used for requests.
    """

    def __init__(
        self,
        user: str,
        headers: Optional[Dict[str, str]]
    ):
        logger.info(f"Initializing ApiClient with {user=}")
        self.name = "ParentWrapper"
        self.user = user
        self.request_id = get_request_id()
        self.tenant_id = get_tenant_id()
        self.headers = headers
        self.updated_headers = self._update_headers()
        logger.info(f"Initialized ApiClient with request_id={self.request_id}, tenant_id={self.tenant_id}")

    def _get_env_var(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise EnvironmentError(f"Required environment variable `{key}` not set.")
        return value

    def get_base_url(self, service_name: str) -> str:
        """
        Resolves base_url for the service.
        """
        env_key = f"{service_name.upper()}_BASE_URL"
        return self._get_env_var(env_key)

    def _update_headers(self) -> Dict[str, str]:
        """
        Updates the headers with request ID for traceability.

        Returns:
            dict: Updated headers with 'x-request-id' added.
        """
        headers = self.headers or {}
        request_id = correlation_id.get()
        logger.info(f"Request ID in API CLIENT : {request_id =}")
        headers["x-request-id"] = self.request_id
        logger.info("Updated headers with x-request-id")
        return headers

    def _get(self, url: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Sends a GET request to the specified endpoint.

        Args:
            url (str): Base URL of the external service.
            endpoint (str): API endpoint path.
            params (Optional[Dict[str, Any]]): Query parameters to be sent.

        Returns:
            Any: JSON response from the external API.
        """
        try:
            headers = self.updated_headers
            formatted_url = f"{url}/{endpoint}"
            logger.info(f"Sending GET request to {formatted_url} with params={params}, headers={headers}")
            response = requests.get(formatted_url, params=params, headers=headers)
            logger.info(f"GET response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.info(f"Exception during GET {url=}, {endpoint=}, {params=}")
            logger.exception(exc)
            raise exc

    def _post(
        self,
        url: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Sends a POST request to the specified endpoint.

        Args:
            url (str): Base URL of the external service.
            endpoint (str): API endpoint path.
            data (Optional[Dict[str, Any]]): Form data to be sent in the body.
            json (Optional[Dict[str, Any]]): JSON data to be sent in the body.
            params (Optional[Dict[str, Any]]): Query parameters to be sent.

        Returns:
            Any: JSON response from the external API.
        """
        try:
            headers = self.updated_headers
            formatted_url = f"{url}/{endpoint}"
            logger.info(f"Sending POST request to {formatted_url} with data={data}, json={json}, params={params}, headers={headers}")
            response = requests.post(formatted_url, data=data, json=json, headers=headers, params=params)
            logger.info(f"POST response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.info(f"Exception during POST {url=}, {endpoint=}, {data=}, {params=}")
            logger.exception(exc)
            raise exc

    def _put(
        self,
        url: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Sends a PUT request to the specified endpoint.

        Args:
            url (str): Base URL of the external service.
            endpoint (str): API endpoint path.
            data (Optional[Dict[str, Any]]): Form data to be sent in the body.
            json (Optional[Dict[str, Any]]): JSON data to be sent in the body.
            params (Optional[Dict[str, Any]]): Query parameters to be sent.

        Returns:
            Any: JSON response from the external API.
        """
        try:
            headers = self.updated_headers
            formatted_url = f"{url}/{endpoint}"
            logger.info(f"Sending PUT request to {formatted_url} with data={data}, json={json}, params={params}, headers={headers}")
            response = requests.put(formatted_url, data=data, json=json, headers=headers, params=params)
            logger.info(f"PUT response status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.info(f"Exception during PUT {url=}, {endpoint=}, {data=}")
            logger.exception(exc)
            raise exc
