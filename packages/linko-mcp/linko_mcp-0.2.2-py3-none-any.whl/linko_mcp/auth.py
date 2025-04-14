"""
Authentication module for Linko API.
Handles token storage, retrieval, and authentication flows.
"""

import httpx
import json
import os
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger('linko_mcp.auth')

# Default to Linko production URL (can be overridden)
BASE_URL = "https://www.linko.study"
# Default Token storage path (for user)
DEFAULT_TOKEN_PATH = os.path.expanduser("~/.linko/auth.json")
# Default Token storage path for AI
AI_TOKEN_PATH = os.path.expanduser("~/.linko/auth_ai.json")

# Environment variable names for user
ENV_USERNAME = "LINKO_USERNAME"
ENV_PASSWORD = "LINKO_PASSWORD"
ENV_BASE_URL = "LINKO_BASE_URL"

# Environment variable names for AI
ENV_AI_USERNAME = "LINKO_AI_USERNAME"
ENV_AI_PASSWORD = "LINKO_AI_PASSWORD"

# Ensure default token directory exists (can be created multiple times, safe)
os.makedirs(os.path.dirname(DEFAULT_TOKEN_PATH), exist_ok=True)

def get_credentials_from_env() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Get Linko credentials from environment variables.
    
    Returns:
        Tuple of (username, password, base_url)
    """
    username = os.environ.get(ENV_USERNAME)
    password = os.environ.get(ENV_PASSWORD)
    base_url = os.environ.get(ENV_BASE_URL, BASE_URL)
    
    if username and password:
        logger.info(f"Using credentials from environment variables")
    else:
        logger.debug("Credentials not found in environment variables")
        
    return username, password, base_url

def get_ai_credentials_from_env() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Get AI Linko credentials from environment variables.
    
    Returns:
        Tuple of (ai_username, ai_password, base_url)
    """
    ai_username = os.environ.get(ENV_AI_USERNAME)
    ai_password = os.environ.get(ENV_AI_PASSWORD)
    base_url = os.environ.get(ENV_BASE_URL, BASE_URL)
    
    if ai_username and ai_password:
        logger.info(f"Using AI credentials from environment variables")
    else:
        logger.debug("AI credentials not found in environment variables")
        
    return ai_username, ai_password, base_url

def get_stored_token(token_path: str = DEFAULT_TOKEN_PATH) -> Optional[Dict[str, str]]:
    """Get stored tokens (access and refresh) from a specific path."""
    if not os.path.exists(token_path):
        return None
    try:
        with open(token_path, 'r') as f:
            data = json.load(f)
            if 'access_token' in data and 'refresh_token' in data:
                return data
    except Exception as e:
        logger.error(f"Error reading token file {token_path}: {e}")
    return None

def store_token(access_token: str, refresh_token: str, token_path: str = DEFAULT_TOKEN_PATH) -> None:
    """Store access and refresh tokens to a specific path."""
    try:
        # Ensure directory exists before writing
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'w') as f:
            json.dump({'access_token': access_token, 'refresh_token': refresh_token}, f)
        logger.debug(f"Tokens stored successfully in {token_path}")
    except Exception as e:
        logger.error(f"Error storing token to {token_path}: {e}")

def clear_token(token_path: str = DEFAULT_TOKEN_PATH) -> None:
    """Remove the stored token file at a specific path."""
    try:
        if os.path.exists(token_path):
            os.remove(token_path)
            logger.warning(f"Removed stored token file: {token_path}")
    except Exception as e:
        logger.error(f"Failed to remove token file {token_path}: {e}")


async def authenticate(username: str = None, password: str = None, base_url: Optional[str] = None, token_path: str = DEFAULT_TOKEN_PATH) -> Optional[Dict[str, str]]:
    """
    Authenticate with Linko using email and password, storing token at specified path.
    
    Args:
        username: Linko email address (defaults to env var if None)
        password: Linko password (defaults to env var if None)
        base_url: Optional API base URL (defaults to env var or constant)
        token_path: Path to store the tokens
        
    Returns:
        Dictionary with access and refresh tokens if successful, None otherwise
    """
    # If credentials not provided, try getting from environment variables
    if username is None or password is None:
        env_username, env_password, env_base_url = get_credentials_from_env()
        username = username or env_username
        password = password or env_password
        base_url = base_url or env_base_url
    
    if not username or not password:
        logger.error("Email and password are required for authentication. Set LINKO_USERNAME and LINKO_PASSWORD environment variables or provide them directly.")
        return None
    
    api_base = (base_url or BASE_URL).rstrip('/')
    login_url = f"{api_base}/api/auth/login/"
    
    logger.info(f"Attempting login for user {username} at {api_base}")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(
                login_url,
                json={"email": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access")
                refresh_token = data.get("refresh")
                if access_token and refresh_token:
                    # Store token using the provided path
                    store_token(access_token, refresh_token, token_path=token_path)
                    logger.info(f"Login successful, tokens stored at {token_path}.")
                    return {"access": access_token, "refresh": refresh_token}
                else:
                    logger.error("Login response did not contain required tokens (access/refresh).")
            elif response.status_code == 403:
                logger.error("Login failed: Email not verified.")
                return None # Specific error handled by caller maybe
            elif response.status_code == 401:
                logger.error("Login failed: Invalid credentials.")
                return None # Specific error handled by caller
            else:
                logger.error(f"Login failed with status {response.status_code}: {response.text}")
        
    except httpx.RequestError as e:
        logger.error(f"Network error during login request to {login_url}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
    
    return None


async def verify_token(token: str, base_url: Optional[str] = None) -> bool:
    """Verify if an access token is valid by making a test API call"""
    if not token:
        return False
        
    api_base = (base_url or BASE_URL).rstrip('/')
    # Using a lightweight endpoint like user profile is common for verification
    verify_url = f"{api_base}/api/user/profile/" 
    
    logger.debug(f"Verifying token via {verify_url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                verify_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            is_valid = response.status_code == 200
            logger.debug(f"Token verification status: {response.status_code} (Valid: {is_valid})")
            return is_valid
    except httpx.RequestError as e:
         logger.error(f"Network error during token verification: {e}")
         return False
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {str(e)}")
        return False

async def refresh_access_token(base_url: Optional[str] = None, token_path: str = DEFAULT_TOKEN_PATH) -> Optional[str]:
    """Refresh the access token using the refresh token from a specific path."""
    token_data = get_stored_token(token_path=token_path)
    if not token_data or 'refresh_token' not in token_data:
        logger.error(f"Refresh token not found in {token_path} for refreshing access token.")
        return None

    refresh_token = token_data['refresh_token']
    api_base = (base_url or BASE_URL).rstrip('/')
    refresh_url = f"{api_base}/api/auth/refresh/"
    
    logger.info(f"Attempting to refresh access token using {refresh_url}.")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                refresh_url,
                json={"refresh": refresh_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get("access")
                # Check if the response also includes a new refresh token
                new_refresh_token = data.get("refresh", refresh_token)
                
                if new_access_token:
                    # Update the token file with new tokens
                    store_token(new_access_token, new_refresh_token, token_path=token_path)
                    logger.info("Access token refreshed successfully.")
                    return new_access_token
                else:
                    logger.error("Refresh response did not contain a new access token.")
            else:
                logger.error(f"Token refresh failed with status {response.status_code}: {response.text}")
                
    except httpx.RequestError as e:
        logger.error(f"Network error during token refresh: {e}")
    except Exception as e:
        logger.error(f"Unexpected error refreshing token: {str(e)}")
    
    return None 