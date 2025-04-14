"""
API client for Linko web service.
Handles authentication, rate limiting, and request management.
"""

import httpx
import logging
import json
import time
import asyncio
import requests
from typing import Optional, Dict, Any, Tuple

# Import auth module
from . import auth

logger = logging.getLogger('linko_mcp.api_client')

class LinkoAPIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class LinkoAuthError(LinkoAPIError):
    """Custom exception for authentication errors after refresh attempt."""
    def __init__(self, message: str = "Authentication failed after refresh attempt."):
        super().__init__(message, status_code=401)

class RateLimiter:
    """Token bucket rate limiter with support for async usage"""
    
    def __init__(self, tokens_per_second=2, max_tokens=10):
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.last_refill = time.time()
        self.lock = asyncio.Lock()
        
    def acquire(self):
        """Synchronous acquire a token, blocking if necessary"""
        self._refill()
        
        # If we don't have tokens, wait until we do
        while self.tokens < 1:
            time.sleep(0.1)
            self._refill()
            
        self.tokens -= 1
        return True
        
    async def acquire_async(self):
        """Asynchronously acquire a token, awaiting if necessary"""
        async with self.lock:
            self._refill()
            
            # If we don't have tokens, wait until we do
            while self.tokens < 1:
                # Release the lock while waiting
                self.lock.release()
                await asyncio.sleep(0.1)
                await self.lock.acquire()
                self._refill()
                
            self.tokens -= 1
            return True
        
    def _refill(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        
        # Calculate new tokens to add
        new_tokens = elapsed * self.tokens_per_second
        if new_tokens > 0:
            self.tokens = min(self.tokens + new_tokens, self.max_tokens)
            self.last_refill = now

# Create a global rate limiter instance
rate_limiter = RateLimiter(tokens_per_second=2, max_tokens=10)

class LinkoAPIClient:
    """Client for interacting with the Linko API, handling auth and refresh."""
    
    def __init__(self, base_url: Optional[str] = None, token_path: str = auth.DEFAULT_TOKEN_PATH):
        self.base_url = (base_url or auth.BASE_URL).rstrip('/')
        self.token_path = token_path # Store the token path for this client instance
        self._client = httpx.AsyncClient(follow_redirects=True, timeout=30.0) # Increased timeout
        logger.info(f"Linko API Client initialized for base URL: {self.base_url} using token path: {self.token_path}")

    async def _get_headers(self) -> Optional[Dict[str, str]]:
        """Get headers with the current access token."""
        token_data = auth.get_stored_token(token_path=self.token_path)
        if not token_data or 'access_token' not in token_data:
            logger.error(f"Access token not found in {self.token_path} for API request.")
            return None
        
        return {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Content-Type": "application/json"
        }

    async def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None, attempt: int = 1) -> Dict[str, Any]:
        """Internal method to make API requests with refresh handling."""
        # Apply rate limiting before making the request
        await rate_limiter.acquire_async()
        
        url = f"{self.base_url}{endpoint}"
        headers = await self._get_headers()

        if headers is None and endpoint != '/api/auth/refresh/': # Allow refresh without initial token
             logger.error("Cannot make request without authorization headers.")
             # Raise a specific error indicating auth is needed
             raise LinkoAuthError("Authentication token not available.")

        try:
            logger.debug(f"Request Attempt {attempt}: {method} {url} Params: {params} Data: {json_data}")
            response = await self._client.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_data
            )
            logger.debug(f"Response Status: {response.status_code}")

            # --- Refresh Logic --- 
            if response.status_code == 401 and attempt == 1:
                logger.warning("Received 401 Unauthorized. Attempting token refresh.")
                new_token = await auth.refresh_access_token(self.base_url, token_path=self.token_path)
                if new_token:
                    logger.info("Token refreshed successfully. Retrying original request.")
                    # Retry the request (attempt=2)
                    return await self._request(method, endpoint, params=params, json_data=json_data, attempt=2)
                else:
                    logger.warning("Token refresh failed. Attempting re-authentication with credentials.")
                    # Try to get credentials from environment
                    username, password, base_url = auth.get_credentials_from_env()
                    if username and password:
                        logger.info(f"Re-authenticating with username: {username}")
                        auth_result = await auth.authenticate(
                            username=username,
                            password=password,
                            base_url=self.base_url,
                            token_path=self.token_path
                        )
                        if auth_result:
                            logger.info("Re-authentication successful. Retrying original request.")
                            # Retry the request after re-authentication (attempt=2)
                            return await self._request(method, endpoint, params=params, json_data=json_data, attempt=2)
                    
                    # If we get here, both refresh and re-auth failed
                    logger.error("Both token refresh and re-authentication failed.")
                    raise LinkoAuthError("Authentication failed after both refresh and re-authentication attempts.")
            
            # Check for other errors after potential retry
            response.raise_for_status() # Raises HTTPStatusError for 4xx/5xx
            
            # Handle potential empty response body for certain successful status codes (e.g., 204 No Content)
            if response.status_code == 204:
                return {}
                
            # Try to parse JSON, handle potential errors
            try:
                # Log the response text for better debugging
                response_text = response.text
                logger.debug(f"Response from {url}: {response_text[:500]}")
                
                if not response_text or response_text.isspace():
                    logger.warning(f"Empty response from {method} {url}")
                    return {}
                    
                return response.json()
            except json.JSONDecodeError as e:
                # Log the specific error and response text for debugging
                logger.error(f"JSON decode error: {e}, Response: {response.text[:1000]}")
                
                # Try to extract more information for better debugging
                error_info = {
                    "error_type": "JSONDecodeError", 
                    "error_msg": str(e),
                    "response_status": response.status_code,
                    "response_text": response.text[:500] if response.text else "",
                    "doc": "API returned invalid JSON"
                }
                
                # Log to help with debugging
                logger.error(f"JSON Decode Error Details: {error_info}")
                
                # Return something usable rather than raising an exception
                return error_info

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text[:500]} for {e.request.method} {e.request.url}")
            # Specific handling for auth error on second attempt
            if e.response.status_code == 401 and attempt == 2:
                 logger.error("Authentication failed even after token refresh and re-authentication attempts.")
                 raise LinkoAuthError("Authentication failed after both refresh and re-authentication attempts.")
            raise LinkoAPIError(f"API request failed: {e.response.text[:500]}", status_code=e.response.status_code)
            
        except httpx.RequestError as e:
            logger.error(f"Network error connecting to API: {e} for {method} {url}")
            raise LinkoAPIError(f"Network error: {e}")
            
        except LinkoAuthError: # Re-raise specific auth errors
            raise
            
        except Exception as e:
            logger.exception(f"An unexpected error occurred during API request: {e}") # Use exception for traceback
            raise LinkoAPIError(f"An unexpected error occurred: {str(e)}")

    # --- Public API Methods --- 

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a GET request."""
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a POST request."""
        return await self._request("POST", endpoint, json_data=json_data, params=params)
        
    async def put(self, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a PUT request."""
        return await self._request("PUT", endpoint, json_data=json_data, params=params)

    async def delete(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a DELETE request."""
        return await self._request("DELETE", endpoint, params=params)

    # --- Helper Methods for Common Lookups --- 
    
    async def search_resource_id(self, resource_name: str) -> Optional[int]:
        """Search for a resource by name and return its ID."""
        if not resource_name:
            return None
        try:
            logger.info(f"Searching for resource ID for name: '{resource_name}'")
            results = await self.get("/api/search/search_resource/", params={"keyword": resource_name})
            if results and isinstance(results, list) and len(results) > 0:
                resource_id = results[0].get("id")
                logger.info(f"Found resource ID {resource_id} for name '{resource_name}'")
                return resource_id
            else:
                logger.warning(f"No resources found matching name '{resource_name}'")
                return None
        except Exception as e:
            logger.error(f"Error searching for resource ID: {e}")
            return None
    
    async def search_knowledge_id(self, subject_name: str) -> Optional[int]:
        """Search for a knowledge (subject) by name and return its ID."""
        if not subject_name:
            return None
            
        try:
            logger.info(f"Searching for knowledge ID for name: '{subject_name}'")
            results = await self.get("/api/search/search_knowledge/", params={"keyword": subject_name})
            
            if results and isinstance(results, list) and len(results) > 0:
                knowledge_id = results[0].get("id")
                logger.info(f"Found knowledge ID {knowledge_id} for name '{subject_name}'")
                return knowledge_id
            else:
                logger.warning(f"No knowledge found matching name '{subject_name}'")
                return None
        except Exception as e:
            logger.error(f"Error searching for knowledge ID: {e}")
            return None

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
        
    # --- Non-async method for backward compatibility if needed ---
    def make_request(self, endpoint, method="GET", params=None, data=None, json=None):
        """
        Make a synchronous request. This is a convenience method when async is not needed.
        Note: This doesn't use the rate limiter and doesn't refresh tokens.
        """
        url = f"{self.base_url}{endpoint}"
        
        token_data = auth.get_stored_token(token_path=self.token_path)
        if not token_data or 'access_token' not in token_data:
            logger.error(f"Access token not found in {self.token_path} for sync API request.")
            raise LinkoAuthError("Authentication token not available.")
            
        headers = {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Content-Type": "application/json"
        }
        
        # Apply rate limiting (synchronous)
        rate_limiter.acquire()
        
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json,
            data=data
        )
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return {}
            
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON response from sync {method} {url}")
            raise LinkoAPIError(f"Invalid JSON response from server.", status_code=response.status_code) 