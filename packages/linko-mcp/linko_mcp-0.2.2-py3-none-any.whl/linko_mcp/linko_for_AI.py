"""
Linko MCP for AI - A Model Context Protocol extension for AI assistants to manage their own notes in Linko.

This module implements MCP tools to allow AI assistants to create, retrieve, update, and delete
their own notes in Linko, supporting cognitive continuity between sessions.
"""

from mcp.server.fastmcp import FastMCP
import sys
import logging
import os
import getpass
import asyncio
import argparse
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional, List, Tuple
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# Import local modules
from . import auth
from . import api_client
from .api_client import LinkoAPIClient, LinkoAPIError, LinkoAuthError

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define logs directory
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Setup logging with rotation (specific file for AI)
log_file = os.path.join(LOGS_DIR, "linko_for_AI.log")
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3           # Keep 3 backup files
)
# Configure root logger - level will be set by args later
logging.basicConfig(
    level=logging.INFO, # Default level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler()] # Also log to console for AI MCP
)
# Set httpx logger level higher to avoid verbose connection logs
logging.getLogger("httpx").setLevel(logging.WARNING)
# Use specific logger for this module
logger = logging.getLogger('linko_for_AI')

# --- MCP Server Setup ---

# Global API client instance (initialized later)
api_client: Optional[LinkoAPIClient] = None

# Specific token path for AI
AI_TOKEN_PATH = os.path.expanduser("~/.linko/auth_ai.json")

# Reference to hold command line args
cmd_args = None

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Get arguments from global reference
    global cmd_args
    
    # Initialize on startup
    start_result = await startup_ai(cmd_args)
    try:
        yield start_result
    finally:
        # Clean up on shutdown
        await shutdown_ai()

# Create FastMCP instance with lifespan
mcp = FastMCP("Linko MCP for AI", lifespan=lifespan)

# --- Helper Functions (Shared with main module) ---

def _parse_int(value: Any, default: int) -> int:
    """Safely parse an integer."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def _parse_str(value: Any) -> Optional[str]:
    """Safely parse a string, returning None if empty."""
    return str(value) if value else None

# --- Error Handling Wrapper (Adapted for AI tools) ---

async def _handle_api_call(tool_name: str, coro, *args, **kwargs) -> Dict[str, Any]:
    """Wraps API calls in AI tools to handle common errors."""
    global api_client
    if not api_client:
         logger.error(f"{tool_name}: API client not initialized.")
         # Provide a more specific error message for the AI context
         return {"error": "Internal Server Error", "message": "API client not available. Cannot interact with Linko."}

    try:
        return await coro(*args, **kwargs)
    except LinkoAuthError as e:
        logger.error(f"{tool_name}: Authentication error: {e}")
        # More specific message for AI context
        return {"error": "Authentication Failed", "message": str(e) or "Authentication token invalid or expired. Please restart AI MCP."}
    except LinkoAPIError as e:
        logger.error(f"{tool_name}: API error (Status: {e.status_code}): {e}")
        return {"error": f"API Request Failed (Status: {e.status_code})", "message": str(e)}
    except Exception as e:
        logger.exception(f"{tool_name}: Unexpected error occurred.") # Log full traceback
        return {"error": "Unexpected Error", "message": f"An unexpected error occurred: {str(e)}"}

# --- MCP Tool Definitions ---

@mcp.tool()
async def get_notes_for_AI(
    keyword=None,
    limit=10,
    subject_name=None,
    days_ago=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get AI's notes with filters.
    
    Args:
        keyword: Search term
        limit: Max notes (default: 10)
        subject_name: Filter by subject
        days_ago: Filter by days
        offset: Skip for pagination
    
    Returns:
        Dict with notes, counts and search context
    """
    async def core_logic():
        # Type conversions
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        days_ago_int = _parse_int(days_ago, default=None)
        limit_int = _parse_int(limit, default=10)
        offset_int = _parse_int(offset, default=0)

        # Fetch subject ID using the shared client helper
        subject_id = await api_client.search_knowledge_id(subject_name_str) if subject_name_str else None

        # --- Build API request parameters ---
        params = {}
        endpoint = "/api/note/" # Default endpoint for filtering
        search_used = False

        if keyword_str:
            # Use search endpoint if keyword is provided
            endpoint = "/api/search/search_notes/"
            params["keyword"] = keyword_str
            search_used = True
            logger.info(f"AI Searching notes with keyword: '{keyword_str}'")
        else:
            # Use list endpoint for filtering by ID, date, etc.
            # Note: API might not paginate search results, pagination primarily for list view
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)  # Use the offset parameter instead of hardcoded "0"
            if subject_id:
                params["filter_knowledge"] = subject_id
            # Date filtering needs client-side processing for list endpoint

            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {subject_id})")
            if days_ago_int: filter_msg.append(f"from last {days_ago_int} days")
            if offset_int > 0: filter_msg.append(f"offset {offset_int}")
            logger.info(f"AI Fetching notes with filters: {', '.join(filter_msg) if filter_msg else 'Recent notes'} (Limit: {limit_int})")

        # --- Make API Call using shared client ---
        response_data = await api_client.get(endpoint, params=params)
        
        # Add debug logging for API response
        logger.info(f"API Response for AI notes with offset {offset_int}: params={params}")
        if isinstance(response_data, dict):
            if "results" in response_data:
                logger.info(f"Response contains 'results' field with {len(response_data['results'])} notes")
                if "count" in response_data:
                    logger.info(f"Response 'count' field reports {response_data['count']} total notes")
            else:
                logger.info(f"Response structure: {list(response_data.keys())}")
        elif isinstance(response_data, list):
            logger.info(f"Response is a list with {len(response_data)} notes")
        else:
            logger.info(f"Response is of type {type(response_data)}")

        # --- Process Response ---
        if search_used:
            # For search endpoint, response is a list of notes
            if not isinstance(response_data, list):
                logger.warning(f"Expected list response from search endpoint, got {type(response_data)}")
                notes = []
                total_count = 0
            else:
                notes = response_data
                total_count = len(notes)
        else:
            # For list endpoint, response should be a dict with results and count
            if not isinstance(response_data, dict):
                logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
                notes = []
                total_count = 0
            else:
                notes = response_data.get("results", [])
                total_count = response_data.get("count", len(notes))

        # --- Apply client-side filtering if needed ---
        # Filter by days_ago for list endpoint (search handles this via API)
        if days_ago_int is not None and not search_used:
            from datetime import datetime, timedelta, timezone
            
            cutoff_dt = datetime.now(timezone.utc) - timedelta(days=days_ago_int)
            
            # Original count for logging
            original_count = len(notes)
            filtered_notes = []
            
            for note in notes:
                # Check both possible date field names
                create_time_str = note.get("created_at") or note.get("create_time")
                
                if create_time_str:
                    try:
                        # Ensure the create_time is offset-aware for comparison
                        create_dt = datetime.fromisoformat(create_time_str.replace('Z', '+00:00'))
                        if create_dt.tzinfo is None:
                            create_dt = create_dt.replace(tzinfo=timezone.utc) # Assume UTC if no timezone
                            
                        if create_dt >= cutoff_dt:
                            filtered_notes.append(note)
                    except ValueError:
                        logger.warning(f"Could not parse create_time '{create_time_str}' for note ID {note.get('id')}")
            
            notes = filtered_notes
            logger.info(f"Client-side date filtering applied: {original_count} -> {len(notes)}")
            # Adjust total_count
            total_count = len(notes)

        # --- Format notes for return ---
        formatted_notes = []
        for note in notes:
            note_id = note.get("id")
            title = note.get("title", "")
            
            # 从笔记中直接获取内容字段
            content = note.get("note")
            
            # 记录笔记内容状态
            if content is None:
                logger.warning(f"Note {note_id} - Content field is null")
                content = ""  # 使用空字符串作为默认值
            
            # Extract dates - handle both naming conventions
            created_at = note.get("created_at", note.get("create_time", ""))
            
            # Extract knowledge/subject data - notes can have multiple knowledge entries
            knowledge_name = ""
            if "knowledge" in note and isinstance(note["knowledge"], list):
                # Join multiple knowledge names if available
                knowledge_names = []
                for k in note["knowledge"]:
                    if isinstance(k, dict) and "name" in k:
                        knowledge_names.append(k["name"])
                knowledge_name = ", ".join(knowledge_names) if knowledge_names else ""
            
            # Format for response
            formatted_note = {
                "id": note_id,
                "title": title,
                "content": content,
                "subject": knowledge_name,
                "created_at": created_at,
            }
            
            formatted_notes.append(formatted_note)

        # --- Build search context description ---
        context_parts = []
        if keyword_str:
            context_parts.append(f"containing keyword '{keyword_str}'")
        if subject_name_str:
            context_parts.append(f"from subject '{subject_name_str}'")
        if days_ago_int:
            context_parts.append(f"created in the last {days_ago_int} days")
        
        search_context = "Your notes " + (", ".join(context_parts) if context_parts else "from recent sessions")
        if offset_int > 0:
            search_context += f" (skipping first {offset_int} results)"
        
        return {
            "notes": formatted_notes,
            "total_count": total_count,
            "displayed_count": len(formatted_notes),
            "search_context": search_context
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("get_notes_for_AI", core_logic)

@mcp.tool()
async def create_note_for_AI(
    title: str,
    content: str
) -> Dict[str, Any]:
    """
    Create a new note for AI.
    
    Args:
        title: Note title
        content: Note content
    
    Returns:
        Dict with created note and status
    """
    async def core_logic():
        # Validate required parameters
        if not title:
            return {"error": "Missing Title", "message": "Note title is required"}
        if not content:
            return {"error": "Missing Content", "message": "Note content is required"}
            
        # Prepare data for API
        note_data = {
            "title": title,
            "note": content
        }
        
        logger.info(f"AI Creating new note with title: '{title}'")
        
        # Make API call
        response = await api_client.post("/api/note/", json_data=note_data)
        
        # Log the full response for debugging
        logger.info(f"Note creation response: {response}")
        
        # Check if response contains expected data
        # Even if the ID is missing, we'll still consider it a success
        # as the tests showed notes are actually created despite API response issues
        note_id = response.get("id")
        if not note_id:
            logger.warning(f"Note creation response missing ID, but note may have been created anyway")
            # Try to search for the note we just created to confirm it exists
            try:
                # Allow some time for the note to be indexed
                await asyncio.sleep(1)
                search_response = await api_client.get("/api/search/search_notes/", params={"keyword": title})
                
                if isinstance(search_response, list) and len(search_response) > 0:
                    # Find a note with matching title that was recently created
                    for note in search_response:
                        if note.get("title") == title:
                            logger.info(f"Found newly created note with title '{title}' via search")
                            note_id = note.get("id")
                            break
            except Exception as search_err:
                logger.warning(f"Failed to verify note creation via search: {search_err}")
        
        # Return simplified response with just ID and status
        return {
            "note_id": note_id,
            "detail": "Note creation appears successful" if note_id else "Note may have been created despite incomplete API response"
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("create_note_for_AI", core_logic)

@mcp.tool()
async def update_note_for_AI(
    note_id: str,
    title=None,
    content=None
) -> Dict[str, Any]:
    """
    Update an AI note.
    
    Args:
        note_id: ID of note to update
        title: New title (optional)
        content: New content (optional)
    
    Returns:
        Dict with updated note and status
    """
    async def core_logic():
        # Validate required parameters
        if not note_id:
            return {"error": "Missing Note ID", "message": "Note ID is required for updates"}
            
        # Must have at least one field to update
        if title is None and content is None:
            return {"error": "No Update Fields", "message": "At least one field (title or content) must be provided for update"}
            
        # Prepare data for API - only include fields that are provided
        note_data = {}
        if title is not None:
            note_data["title"] = title
        if content is not None:
            note_data["note"] = content
        
        # Wrap the data in a 'note' object as expected by the API
        wrapped_data = {"note": note_data}
        
        logger.info(f"AI Updating note with ID: {note_id}")
        
        # First try to fetch the current note to verify it exists
        current_note = None
        try:
            current_note = await api_client.get(f"/api/note/{note_id}/")
            if not current_note or "id" not in current_note:
                logger.warning(f"Direct note retrieval failed for ID {note_id}")
                # If direct retrieval fails, we'll try to search for it
                current_note = None
            else:
                logger.info(f"Successfully retrieved note with ID {note_id}")
        except LinkoAPIError as e:
            if e.status_code == 404:
                logger.warning(f"Note with ID {note_id} not found via direct retrieval, trying search...")
            else:
                # For other errors, log but continue with the fallback approach
                logger.warning(f"Error retrieving note with ID {note_id}: {e}")
        
        # If direct retrieval fails, try to use search to find the note
        if current_note is None:
            try:
                # Get all recent notes and look for the ID
                search_response = await api_client.get("/api/note/", params={"limit": "50"})
                if isinstance(search_response, dict) and "results" in search_response:
                    # Look through results for matching ID
                    for note in search_response.get("results", []):
                        if str(note.get("id")) == str(note_id):
                            current_note = note
                            logger.info(f"Found note with ID {note_id} via search")
                            break
                
                # If still not found, try keyword search with empty query to get all notes
                if current_note is None:
                    logger.info(f"Trying keyword search to find note {note_id}")
                    search_response = await api_client.get("/api/search/search_notes/", params={"keyword": ""})
                    if isinstance(search_response, list):
                        for note in search_response:
                            if str(note.get("id")) == str(note_id):
                                current_note = note
                                logger.info(f"Found note with ID {note_id} via keyword search")
                                break
            except Exception as search_err:
                logger.warning(f"Failed to find note via search: {search_err}")
        
        # If we still couldn't find the note, return an error
        if current_note is None:
            return {"error": "Note Not Found", "message": f"Note with ID {note_id} not found after multiple retrieval attempts"}
        
        # Make update API call with the note ID we've confirmed exists
        try:
            response = await api_client.put(f"/api/note/{note_id}/", json_data=wrapped_data)
            
            # Format the response
            return {
                "note": {
                    "id": response.get("id", note_id),
                    "title": response.get("title", title if title is not None else current_note.get("title", "")),
                    "note": response.get("note", content if content is not None else current_note.get("note", "")),
                    "updated_at": response.get("updated_at", "")
                },
                "detail": "Note updated successfully"
            }
        except LinkoAPIError as e:
            logger.error(f"Failed to update note despite finding it: {e}")
            if e.status_code == 404:
                return {"error": "API Inconsistency", "message": f"Note with ID {note_id} was found but couldn't be updated (404)"}
            raise  # Re-raise other errors to be caught by error handler
    
    # Call with error handling wrapper
    return await _handle_api_call("update_note_for_AI", core_logic)

@mcp.tool()
async def delete_note_for_AI(
    note_id: str
) -> Dict[str, Any]:
    """
    Delete an AI note.
    
    Args:
        note_id: ID of note to delete
    
    Returns:
        Dict with deletion status
    """
    async def core_logic():
        # Validate required parameters
        if not note_id:
            return {"error": "Missing Note ID", "message": "Note ID is required for deletion"}
            
        logger.info(f"AI Deleting note with ID: {note_id}")
        
        # Make delete API call
        try:
            await api_client.delete(f"/api/note/{note_id}/")
            return {"detail": f"Note {note_id} deleted successfully"}
        except LinkoAPIError as e:
            if e.status_code == 404:
                return {"error": "Note Not Found", "message": f"Note with ID {note_id} not found or already deleted"}
            raise  # Re-raise other errors to be caught by error handler
    
    # Call with error handling wrapper
    return await _handle_api_call("delete_note_for_AI", core_logic)

# --- Command Line Arguments ---

def parse_args():
    """Parse command line arguments for AI MCP."""
    parser = argparse.ArgumentParser(description="Linko MCP for AI - Allow AI assistants to manage their notes")
    parser.add_argument("--username", help="AI's Linko email address (overrides environment variable)")
    parser.add_argument("--password", help="AI's Linko password (overrides environment variable)")
    parser.add_argument("--base-url", help="Linko API base URL (default: https://www.linko.study)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    return parser.parse_args()

# --- Authentication Check for AI ---

def setup_debug_logging():
    """Configure debug logging for all relevant modules."""
    logging.getLogger('linko_for_AI').setLevel(logging.DEBUG)
    logging.getLogger('linko_mcp.auth').setLevel(logging.DEBUG)
    logging.getLogger('linko_mcp.api_client').setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled for AI")

async def check_authentication_ai(cmd_args) -> Tuple[bool, Optional[LinkoAPIClient]]:
    """Check authentication status and return auth result and API client for AI user."""
    
    # Set logging level based on debug flag
    if cmd_args.debug:
        setup_debug_logging()
    
    # Create API client with specified base URL if provided, using AI-specific token path
    client = LinkoAPIClient(
        base_url=cmd_args.base_url,
        token_path=AI_TOKEN_PATH
    )
    
    # Check for stored AI token first
    token_data = auth.get_stored_token(token_path=AI_TOKEN_PATH)
    if token_data and 'access_token' in token_data:
        token = token_data['access_token']
        logger.info("Found stored AI access token, verifying...")
        
        if await auth.verify_token(token, base_url=cmd_args.base_url):
            logger.info("Stored AI token is valid.")
            return True, client
        else:
            logger.warning("Stored AI token is invalid or expired.")
            
            # Try refreshing token
            logger.info("Attempting to refresh AI token...")
            new_token = await auth.refresh_access_token(base_url=cmd_args.base_url, token_path=AI_TOKEN_PATH)
            if new_token:
                logger.info("AI token refreshed successfully.")
                return True, client
            else:
                logger.warning("AI token refresh failed, need to re-authenticate.")
    else:
        logger.info("No stored AI token found.")
    
    # If we get here, we need authentication with username/password
    username = cmd_args.username
    password = cmd_args.password
    
    # If not provided via command line, try environment variables (AI-specific ones)
    if not username or not password:
        env_username, env_password, _ = auth.get_ai_credentials_from_env()
        username = username or env_username
        password = password or env_password
    
    # If still not available, prompt user (only works in interactive mode)
    if not username:
        logger.info("AI username not provided via arguments or environment variables.")
        try:
            username = input("AI Linko email: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False, None
    
    if not password:
        logger.info("AI password not provided via arguments or environment variables.")
        try:
            password = getpass.getpass("AI Linko password: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False, None
    
    # Attempt authentication
    if not username or not password:
        logger.error("AI username and password are required. Please provide via command line arguments, environment variables, or interactive prompt.")
        return False, None
    
    logger.info(f"Authenticating with AI username: {username}")
    auth_result = await auth.authenticate(
        username=username,
        password=password,
        base_url=cmd_args.base_url,
        token_path=AI_TOKEN_PATH  # Use AI-specific token path
    )
    
    if auth_result:
        logger.info("AI authentication successful.")
        return True, client
    else:
        logger.error("AI authentication failed. Please check your credentials.")
        return False, None

# --- Startup/Shutdown Functions ---

async def startup_ai(args):
    """
    Performs asynchronous setup tasks before starting MCP for AI.
    
    This function initializes the global api_client variable.
    """
    global api_client  # Modifies global API client
    logger.info("Starting Linko MCP for AI...")
    
    # Check authentication and get API client for AI
    authenticated, client = await check_authentication_ai(args)
    if not authenticated:
        logger.error("AI authentication failed. MCP cannot start.")
        return False
    
    # Store the authenticated client
    api_client = client
    logger.info("Linko MCP for AI ready to serve requests.")
    return True

async def shutdown_ai():
    """
    Performs asynchronous cleanup tasks for AI MCP.
    
    This function cleans up resources such as the global API client.
    """
    global api_client  # Uses and potentially modifies global API client
    
    if api_client:
        logger.info("Closing AI API client connection...")
        await api_client.close()
        api_client = None  # Clear reference to allow garbage collection
        
    logger.info("Async shutdown for AI complete.")

# --- Main Entry Point ---

def main():
    """
    Main entry point for the Linko MCP for AI service.
    
    This function:
    1. Parses command line arguments
    2. Sets up logging based on debug flag
    3. Authenticates with Linko and initializes the API client for AI use
    4. Starts the MCP server if authentication succeeds
    5. Handles proper cleanup on exit
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Parse command line arguments
    args = parse_args()
    
    # Configure logging level if specified
    if args.debug:
        setup_debug_logging()
    
    # Set args in global reference for lifespan to access
    global cmd_args
    cmd_args = args
    
    # Initialize exit code to success
    exit_code = 0
    startup_success = False
    
    try:
        # Run async startup tasks first (this will initialize api_client)
        startup_success = asyncio.run(startup_ai(args))
        
        if startup_success:
            print("\n✅ Linko MCP for AI Authenticated and Ready. Starting server...")
            logger.info("Authentication successful, starting MCP server loop")
            # Run the blocking MCP server
            mcp.run()
        else:
            print("\n❌ MCP startup failed due to authentication error. Exiting.")
            exit_code = 1
            
    except KeyboardInterrupt:
        print("\n🔌 Shutting down Linko MCP for AI due to KeyboardInterrupt...")
        # Normal exit on Ctrl+C
        
    except Exception as e:
        logger.critical(f"Critical error during MCP execution: {e}", exc_info=True)
        print(f"❌ Critical Error: {str(e)}")
        exit_code = 1
        
    finally:
        # Ensure cleanup runs regardless of how mcp.run() exits
        if startup_success:
            logger.info("Initiating shutdown cleanup...")
            try:
                # Run async shutdown tasks
                asyncio.run(shutdown_ai())
            except Exception as e:
                logger.error(f"Error during shutdown cleanup: {e}", exc_info=True)
                
        logger.info("Linko MCP for AI process finished.")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 