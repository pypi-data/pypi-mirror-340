# (C) Continuous AI, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from __future__ import annotations

import json
import logging
import sys
import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

import requests
from oauthlib import oauth1
from requests_oauthlib import OAuth1
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout
from urllib3.util.retry import Retry

# Configure default logger
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)

class NetSuiteClient:
    """A client for interacting with NetSuite's REST and SuiteQL APIs.

    This client provides methods to interact with NetSuite's REST API and execute SuiteQL queries.
    It handles OAuth 1.0 authentication and provides a simple interface for making requests.

    Args:
        realm: The NetSuite realm ID
        account: The NetSuite account ID (the xxxxx part of xxxxx.app.netsuite.com)
        consumer_key: OAuth consumer key from your integration record
        consumer_secret: OAuth consumer secret from your integration record
        token_id: OAuth token ID from your access token
        token_secret: OAuth token secret from your access token
        timeout: Request timeout in seconds (default: 60)
        logger: Custom logger instance (default: standard logging)
        max_retries: Maximum number of retries for failed requests (default: 3)
    """

    def __init__(
        self,
        realm: str,
        account: str,
        consumer_key: str,
        consumer_secret: str,
        token_id: str,
        token_secret: str,
        timeout: int = 60,
        logger: Optional[logging.Logger] = None,
        max_retries: int = 3,
    ) -> None:
        self.realm = realm
        self.account = account
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_id = token_id
        self.token_secret = token_secret
        self.timeout = timeout
        self.max_retries = max_retries
        self.log = logger or logging.getLogger(__name__)
        
        # Configure OAuth
        self.oauth = oauth1.Client(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.token_id,
            resource_owner_secret=self.token_secret,
            realm=self.realm,
            signature_method="HMAC-SHA256"
        )
        
        self.auth = OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.token_id,
            resource_owner_secret=self.token_secret,
            realm=self.realm,
            signature_method="HMAC-SHA256",
        )

        # Configure session
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """Get the default headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Prefer": "transient"
        }

    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: The URL to make the request to
            **kwargs: Additional arguments to pass to requests

        Returns:
            The JSON response from the API

        Raises:
            NetSuiteError: If the request fails after all retries
        """
        retries = 0
        last_error = None

        while retries <= self.max_retries:
            try:
                response = self.session.request(method, url, **kwargs)
                if response.status_code < 400:
                    return response.json()
                elif response.status_code >= 500:
                    last_error = RequestException(f"HTTP {response.status_code}: {response.text}")
                    retries += 1
                    if retries <= self.max_retries:
                        time.sleep(2 ** retries)  # Exponential backoff
                        continue
                else:
                    raise RequestException(f"HTTP {response.status_code}: {response.text}")
            except Timeout as e:
                self.log.error("Request timed out: %s", str(e))
                raise NetSuiteError(f"Request timed out: {str(e)}") from e
            except RequestException as e:
                last_error = e
                retries += 1
                if retries <= self.max_retries:
                    time.sleep(2 ** retries)  # Exponential backoff
                    continue
                break

        if last_error:
            raise NetSuiteError(f"Failed after {retries} retries: {str(last_error)}") from last_error
        raise NetSuiteError("Failed to make request")

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the NetSuite API.

        Args:
            url: The URL to make the request to
            params: Optional query parameters

        Returns:
            The JSON response from the API

        Raises:
            NetSuiteError: If the request fails
        """
        self.log.debug("Making GET request to %s with params: %s", url, params)
        
        params = params or {}
        params_str = urlencode(params)
        full_url = f"{url}?{params_str}" if params else url
        
        headers = self._get_headers()
        url, headers, _body = self.oauth.sign(full_url, headers=headers)
        
        return self._make_request('GET', url, headers=headers, timeout=self.timeout)

    def post(self, url: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request to the NetSuite API.

        Args:
            url: The URL to make the request to
            data: The data to send in the request body
            params: Optional query parameters

        Returns:
            The JSON response from the API

        Raises:
            NetSuiteError: If the request fails
        """
        self.log.debug("Making POST request to %s with data: %s", url, data)
        
        headers = self._get_headers()
        if params:
            headers.update(params)
        
        return self._make_request('POST', url, json=data, headers=headers, auth=self.auth, timeout=self.timeout)

    def get_suiteql_query(self, query: str) -> Dict[str, Any]:
        """Execute a SuiteQL query.

        Args:
            query: The SuiteQL query to execute

        Returns:
            The query results

        Raises:
            NetSuiteError: If the query fails
        """
        self.log.debug("Executing SuiteQL query: %s", query)
        
        data = {"q": query}
        url = f"https://{self.account}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"
        
        try:
            return self.post(url, data)
        except NetSuiteError as e:
            self.log.error("Failed to execute SuiteQL query: %s", str(e))
            raise

    def get_scriptlet(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a custom scriptlet.

        Args:
            params: Parameters for the scriptlet execution

        Returns:
            The scriptlet results

        Raises:
            NetSuiteError: If the scriptlet execution fails
        """
        self.log.debug("Executing scriptlet with params: %s", params)
        
        url = f"https://{self.account}.app.netsuite.com/app/site/hosting/scriptlet.nl"
        
        try:
            return self.get(url, params)
        except NetSuiteError as e:
            self.log.error("Failed to execute scriptlet: %s", str(e))
            raise

class NetSuiteError(Exception):
    """Base exception for NetSuite client errors."""
    pass