"""
Linko MCP - A Model Context Protocol extension for accessing Linko study notes and resources.

This module implements MCP tools to allow LLMs to access the Linko API for retrieving 
study notes, resources, and subject information.
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

# Setup logging with rotation
log_file = os.path.join(LOGS_DIR, "linko_mcp.log")
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3           # Keep 3 backup files
)
logging.basicConfig(
    level=logging.INFO, # Default to INFO, can be overridden by args
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler()] # Also log to console
)
# Set httpx logger level higher to avoid verbose connection logs
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger('linko_mcp') # Main logger

# --- MCP Server Setup ---

# Global API client instance (initialized later)
api_client: Optional[LinkoAPIClient] = None

# Reference to hold command line args
cmd_args = None

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Get arguments from global reference
    global cmd_args
    
    # Initialize on startup
    start_result = await startup(cmd_args)
    try:
        yield start_result
    finally:
        # Clean up on shutdown
        await shutdown()

# Create FastMCP instance with lifespan
mcp = FastMCP("Linko MCP", lifespan=lifespan)

# --- Helper Functions (Type conversion, etc.) ---

def _parse_int(value: Any, default: int) -> int:
    """Safely parse an integer."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def _parse_str(value: Any) -> Optional[str]:
    """Safely parse a string, returning None if empty."""
    return str(value) if value else None

# --- Error Handling Wrapper for Tools ---

async def _handle_api_call(tool_name: str, coro, *args, **kwargs) -> Dict[str, Any]:
    """Wraps API calls in tools to handle common errors."""
    global api_client
    if not api_client:
         logger.error(f"{tool_name}: API client not initialized.")
         return {"error": "Internal Server Error", "message": "API client not available."}
         
    try:
        return await coro(*args, **kwargs)
    except LinkoAuthError as e:
        logger.error(f"{tool_name}: Authentication error: {e}")
        return {"error": "Authentication Failed", "message": str(e) or "Authentication token invalid or expired. Please restart MCP."}
    except LinkoAPIError as e:
        logger.error(f"{tool_name}: API error (Status: {e.status_code}): {e}")
        return {"error": f"API Request Failed (Status: {e.status_code})", "message": str(e)}
    except Exception as e:
        logger.exception(f"{tool_name}: Unexpected error occurred.") # Log full traceback
        return {"error": "Unexpected Error", "message": f"An unexpected error occurred: {str(e)}"}
        
# --- MCP Tool Definitions ---

@mcp.tool()
async def get_notes(
    keyword=None,
    limit=10,
    subject_name=None,
    resource_name=None,
    days_ago=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get user study notes with filters.
    
    Args:
        keyword: Search term for note content 
        limit: Max notes to return (default: 10, max: 10)
        subject_name: Filter by subject
        resource_name: Filter by resource
        days_ago: Filter by days
        offset: Skip for pagination
    
    Returns:
        Dict with notes, counts and search context
    """
    async def core_logic():
        # Type conversions
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        resource_name_str = _parse_str(resource_name)
        days_ago_int = _parse_int(days_ago, default=None)
        limit_int = min(_parse_int(limit, default=10), 10) # Enforce max limit of 10
        offset_int = _parse_int(offset, default=0)
        
        # Fetch IDs if names are provided
        resource_id = await api_client.search_resource_id(resource_name_str) if resource_name_str else None
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
            logger.info(f"Searching notes with keyword: '{keyword_str}'")
        else:
            # Use list endpoint for filtering by ID, date, etc.
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)
            if subject_id:
                params["filter_knowledge"] = subject_id
            if resource_id:
                # Note: Check if the backend /api/note/ supports resource_id filtering directly
                # If not, filtering might need to happen client-side after fetching,
                # or the search endpoint might be better even without a keyword.
                # Assuming it supports `resource_id` for now based on old code structure.
                params["resource_id"] = resource_id 
            # Date filtering needs to be applied *after* fetching if using list endpoint
            
            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {subject_id})")
            if resource_name_str: filter_msg.append(f"resource '{resource_name_str}' (ID: {resource_id})")
            if days_ago_int: filter_msg.append(f"from last {days_ago_int} days")
            logger.info(f"Fetching notes with filters: {', '.join(filter_msg) if filter_msg else 'Recent notes'} (Limit: {limit_int})")

        # --- Make API Call --- 
        try:
            response_data = await api_client.get(endpoint, params=params)
            
            # Add debug logging for API response
            logger.info(f"API Response for notes with offset {offset_int}: params={params}")
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
                    total_count_from_api = 0
                else:
                    notes = response_data
                    total_count_from_api = len(notes)
            else:
                # For list endpoint, response should be a dict with results and count
                if not isinstance(response_data, dict):
                    logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
                    notes = []
                    total_count_from_api = 0
                else:
                    notes = response_data.get("results", [])
                    total_count_from_api = response_data.get("count", len(notes))
            
            # --- Apply client-side filtering if needed ---
            # Filter by days_ago for list endpoint (search handles this via API)
            if days_ago_int is not None and not search_used:
                import datetime
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
                # Adjust total count
                total_count_from_api = len(notes)
            
            # --- Prepare notes for return ---
            # Format each note to include the essential fields
            formatted_notes = process_notes_response(notes)
            
            # --- Build search context description ---
            context_parts = []
            if keyword_str:
                context_parts.append(f"containing keyword '{keyword_str}'")
            if subject_name_str:
                context_parts.append(f"from subject '{subject_name_str}'")
            if resource_name_str:
                context_parts.append(f"from resource '{resource_name_str}'")
            if days_ago_int:
                context_parts.append(f"created in the last {days_ago_int} days")
            
            search_context = "Notes " + (", ".join(context_parts) if context_parts else "from your recent studies")
            if offset_int > 0:
                search_context += f" (skipping first {offset_int} results)"
            
            return {
                "notes": formatted_notes,
                "total_count": total_count_from_api,
                "displayed_count": len(formatted_notes),
                "search_context": search_context
            }
            
        except Exception as e:
            logger.exception(f"Error processing notes response: {e}")
            return {"error": "Processing Error", "message": f"Error processing notes: {str(e)}"}
    
    # Call with error handling wrapper
    return await _handle_api_call("get_notes", core_logic)

def process_notes_response(notes):
    """Process and format note objects from API response."""
    formatted_notes = []
    
    for note in notes:
        note_id = note.get("id")
        title = note.get("title", "")
        
        # Handle content field which could be in 'content' or 'note' field
        content = note.get("note", "")
        
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
        
        # Extract resource data - notes can have at most one resource
        resource_name = ""
        if "resource" in note and isinstance(note["resource"], list) and note["resource"]:
            # For most cases, there should be at most one resource
            # But handle the case if somehow there are multiple
            resource_names = []
            for r in note["resource"]:
                if isinstance(r, dict) and "title" in r:
                    resource_names.append(r["title"])
            resource_name = resource_names[0] if resource_names else ""

        # Include a preview field for compatibility
        if len(content) > 2000:
            content = content[:1997] + "..."
        
        # Prepare a formatted object with consistent structure
        formatted_note = {
            "id": note_id,
            "title": title,
            "content": content,
            "subject": knowledge_name,
            "resource": resource_name,
            "created_at": created_at,
        }
        
        formatted_notes.append(formatted_note)
    
    return formatted_notes

@mcp.tool()
async def get_resources(
    keyword=None,
    limit=10,
    subject_name=None,
    resource_type=None,
    finished=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get learning resources with filters.
    
    Args:
        keyword: Search term
        limit: Max resources (default: 10)
        subject_name: Filter by subject
        resource_type: Filter by type (book, article, video, course, podcast, other)
        finished: Filter by completion (True/False)
        offset: Skip for pagination
    
    Returns:
        Dict with resources, counts and search context
    """
    async def core_logic():
        # Type conversions and validation
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        resource_type_str = _parse_str(resource_type)
        limit_int = _parse_int(limit, default=10)
        offset_int = _parse_int(offset, default=0)
        
        # Parse the finished parameter
        filter_finished = None
        if finished is not None:
            if isinstance(finished, bool):
                filter_finished = "finished" if finished else "not_started"
            elif isinstance(finished, str):
                finished_lower = finished.lower()
                if finished_lower in ('true', 'yes', '1'):
                    filter_finished = "finished"
                elif finished_lower in ('false', 'no', '0'):
                    filter_finished = "not_started"
                else:
                    filter_finished = finished_lower  # Use as-is if it's another string value
        
        # Map resource type to API format
        filter_type = None
        if resource_type_str:
            resource_type_map = {
                "book": "bo", 
                "article": "ar", 
                "video": "vi", 
                "course": "co", 
                "podcast": "po", 
                "other": "or"
            }
            resource_type_lower = resource_type_str.lower()
            if resource_type_lower in resource_type_map:
                filter_type = resource_type_map[resource_type_lower]
            else:
                logger.warning(f"Invalid resource type: '{resource_type_str}'. Valid types are: {', '.join(resource_type_map.keys())}")
        
        # Get subject ID if subject name is provided
        filter_knowledge = None
        if subject_name_str:
            subject_id = await api_client.search_knowledge_id(subject_name_str)
            if subject_id:
                filter_knowledge = subject_id
        
        # Determine endpoint and parameters based on search vs. filter
        params = {}
        endpoint = "/api/resource/"
        search_used = False
        
        if keyword_str:
            # Use search endpoint for keyword search
            endpoint = "/api/search/search_resource/"
            params["keyword"] = keyword_str
            search_used = True
            logger.info(f"Searching resources with keyword: '{keyword_str}'")
        else:
            # Use list endpoint with filters
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)
            
            # Add filters to parameters
            if filter_knowledge:
                params["filter_knowledge"] = filter_knowledge
            if filter_type:
                params["filter_type"] = filter_type
            if filter_finished:
                params["filter_finished"] = filter_finished
                
            # Build log message for active filters
            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {filter_knowledge})")
            if resource_type_str: filter_msg.append(f"type '{resource_type_str}'")
            if filter_finished: filter_msg.append(f"status: '{filter_finished}'")
            logger.info(f"Fetching resources with filters: {', '.join(filter_msg) if filter_msg else 'All resources'} (Limit: {limit_int})")
        
        # Make API Call
        response_data = await api_client.get(endpoint, params=params)
        
        # Process API response
        resources = []
        total_count = 0
        
        if search_used:
            # Process search results (list format)
            if isinstance(response_data, list):
                resources = response_data
                total_count = len(resources)
                # Apply pagination manually for search results
                resources = resources[offset_int:offset_int + limit_int]
            else:
                logger.warning(f"Expected list response from search endpoint, got {type(response_data)}")
        else:
            # Process list results (dict format with pagination)
            if isinstance(response_data, dict):
                resources = response_data.get("results", [])
                total_count = response_data.get("count", len(resources))
            else:
                logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
        
        # Format resources for response
        formatted_resources = []
        for resource in resources:
            formatted_resource = process_resource(resource)
            if formatted_resource:
                formatted_resources.append(formatted_resource)
        
        # Build search context description
        context_parts = []
        if keyword_str:
            context_parts.append(f"matching '{keyword_str}'")
        if subject_name_str:
            context_parts.append(f"in subject '{subject_name_str}'")
        if resource_type_str:
            context_parts.append(f"of type '{resource_type_str}'")
        if filter_finished:
            status_map = {
                "finished": "completed", 
                "not_started": "not started", 
                "in_progress": "in progress"
            }
            status_description = status_map.get(filter_finished, filter_finished)
            context_parts.append(f"marked as {status_description}")
        
        search_context = "Resources " + (", ".join(context_parts) if context_parts else "from your collection")
        if offset_int > 0:
            search_context += f" (skipping first {offset_int} results)"
        
        return {
            "resources": formatted_resources,
            "total_count": total_count,
            "displayed_count": len(formatted_resources),
            "search_context": search_context
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("get_resources", core_logic)

def process_resource(resource: Dict) -> Dict:
    """Extract and format resource data from API response."""
    if not isinstance(resource, dict):
        return None
        
    # Extract basic fields with defaults
    resource_id = resource.get("id")
    title = resource.get("title", "")
    author = resource.get("author", "")
    description = resource.get("description", "")
    
    # Get resource type - try multiple possible field names
    resource_type = resource.get("type", resource.get("resource_type", ""))
    
    # Extract progress information
    try:
        progress = int(resource.get("progress", 0))
    except (TypeError, ValueError):
        progress = 0
        
    try:
        total_length = int(resource.get("total_length", 100))
    except (TypeError, ValueError):
        total_length = 100
    
    # Determine if resource is finished
    is_finished = False
    if "is_finished" in resource:
        is_finished = bool(resource.get("is_finished"))
    elif total_length > 0 and progress > 0 and progress >= total_length:
        is_finished = True
    
    # Handle nested resource object if present
    if "resource" in resource and isinstance(resource["resource"], dict):
        resource_data = resource["resource"]
        resource_id = resource_data.get("id", resource_id)
        title = resource_data.get("title", title)
        author = resource_data.get("author", author)
        
        # Get resource type from nested object if not already set
        if not resource_type:
            resource_type = resource_data.get("type", resource_data.get("resource_type", ""))
        
        # Use the longer description if both are available
        if resource_data.get("description"):
            if not description or len(resource_data.get("description")) > len(description):
                description = resource_data.get("description")
    
    # Process subject information
    subject_names = []
    
    # Check user_knowledge first (common in learn_history)
    knowledge_list = []
    if "user_knowledge" in resource and isinstance(resource["user_knowledge"], list):
        knowledge_list = resource["user_knowledge"]
    # Fall back to resource.knowledge
    elif "knowledge" in resource:
        knowledge_data = resource.get("knowledge")
        if isinstance(knowledge_data, list):
            knowledge_list = knowledge_data
        elif isinstance(knowledge_data, dict) and "results" in knowledge_data:
            knowledge_list = knowledge_data.get("results", [])
    
    # Extract subject names from knowledge list
    for knowledge_item in knowledge_list:
        if isinstance(knowledge_item, dict):
            subject_name = knowledge_item.get("name") or knowledge_item.get("title")
            if subject_name:
                subject_names.append(subject_name)
    
    subject_title = ", ".join(subject_names) if subject_names else ""
    
    # Return formatted resource object
    return {
        "id": resource_id,
        "title": title,
        "author": author,
        "type": resource_type,
        "description": description,
        "subject": subject_title,
        "is_finished": is_finished,
        "progress": progress,
        "total_length": total_length
    }

@mcp.tool()
async def get_subjects(
    subject_name=None,
) -> Dict[str, Any]:
    """
    Get user's knowledge subjects.
    
    Args:
        subject_name: Optional specific subject to search
    
    Returns:
        Dict with subjects, counts and search context
    """
    async def core_logic():
        subject_name_str = _parse_str(subject_name)
        
        # If subject name is provided, search for that specific subject
        if subject_name_str:
            logger.info(f"Searching for subject: '{subject_name_str}'")
            
            # Use search_knowledge_id to find the subject ID
            subject_id = await api_client.search_knowledge_id(subject_name_str)
            
            if subject_id:
                logger.info(f"Found subject ID: {subject_id} for '{subject_name_str}'")
                
                # Get subject details from details endpoint
                details_endpoint = "/api/subject/details/"
                details_params = {"pk": str(subject_id)}
                
                try:
                    details_response = await api_client.get(details_endpoint, details_params)
                    
                    if not isinstance(details_response, dict):
                        logger.warning(f"Expected dict response for subject details, got {type(details_response)}")
                        return {
                            "error": "Invalid Response",
                            "message": "Invalid response format from subject details API",
                            "subjects": [],
                            "total_count": 0,
                            "displayed_count": 0
                        }
                    
                    # Extract data from details response
                    subject_data = details_response.get("data", {})
                    notes_count = details_response.get("notes_count", 0)
                    resource_count = details_response.get("resource_count", 0)
                    
                    # Format subject with additional details
                    subject_item_id = subject_data.get("id")
                    name = subject_data.get("name", "")
                    is_linked = subject_data.get("is_linked", True)
                    description = subject_data.get("description", "")
                    
                    subject_info = {
                        "id": subject_item_id,
                        "title": name.title() if is_linked else name,
                        "is_linked": is_linked,
                        "description": description,
                        "note_count": notes_count,
                        "resource_count": resource_count,
                        "learn_count": notes_count + resource_count
                    }
                    
                    # Add related subjects if available
                    related_subjects = []
                    for relation_type in ["children", "siblings", "father"]:
                        relation_items = subject_data.get(relation_type, [])
                        if isinstance(relation_items, list):
                            for related in relation_items:
                                if not isinstance(related, dict):
                                    continue
                                    
                                related_id = related.get("id")
                                related_name = related.get("name", "")
                                related_is_linked = related.get("is_linked", True)
                                related_note_count = related.get("note_count", 0)
                                related_resource_count = related.get("resource_count", 0)
                                related_learn_count = related.get("learn_count", 0)
                                
                                relation_name = relation_type
                                if relation_type.endswith("s"):
                                    relation_name = relation_type[:-1]
                                    
                                related_subject = {
                                    "id": related_id,
                                    "title": related_name.title() if related_is_linked else related_name,
                                    "is_linked": related_is_linked,
                                    "note_count": related_note_count,
                                    "resource_count": related_resource_count,
                                    "learn_count": related_learn_count,
                                    "relation": relation_name
                                }
                                related_subjects.append(related_subject)
                    
                    return {
                        "subjects": [subject_info],
                        "related_subjects": related_subjects,
                        "total_count": 1,
                        "displayed_count": 1,
                        "search_context": f"Details for subject '{name}'"
                    }
                    
                except Exception as e:
                    logger.exception(f"Error fetching subject details: {e}")
                    return {
                        "error": "Processing Error", 
                        "message": f"Error fetching subject details: {str(e)}",
                        "subjects": [],
                        "total_count": 0,
                        "displayed_count": 0
                    }
            else:
                # No subject found
                return {
                    "error": "Not Found",
                    "message": f"No subjects found matching '{subject_name_str}'",
                    "subjects": [],
                    "total_count": 0,
                    "displayed_count": 0
                }
        
        # If no subject_name provided, get all subjects
        endpoint = "/api/subject/"
        params = {}
        logger.info("Fetching subjects overview")
        
        try:
            response_data = await api_client.get(endpoint, params=params)
            
            if not isinstance(response_data, dict) or "subjects" not in response_data:
                logger.warning(f"Expected dict with 'subjects' key in response, got: {response_data}")
                return {
                    "error": "Invalid Response",
                    "message": "Expected dict with 'subjects' key in response",
                    "subjects": [],
                    "total_count": 0,
                    "displayed_count": 0
                }
            
            # Get subjects and count
            subjects_data = response_data.get("subjects", [])
            total_count = response_data.get("total_count", len(subjects_data))
            
            # Format subjects 
            formatted_subjects = []
            for subject_item in subjects_data:
                if not isinstance(subject_item, dict):
                    continue
                    
                subject_item_id = subject_item.get("id")
                name = subject_item.get("name", "")
                is_linked = subject_item.get("is_linked", True)
                learn_count = subject_item.get("learn_count", 0)
                note_count = subject_item.get("note_count", 0)
                resource_count = subject_item.get("resource_count", 0)
                
                formatted_subject = {
                    "id": subject_item_id,
                    "title": name.title() if is_linked else name,
                    "is_linked": is_linked,
                    "note_count": note_count,
                    "resource_count": resource_count,
                    "learn_count": learn_count
                }
                formatted_subjects.append(formatted_subject)
            
            return {
                "subjects": formatted_subjects,
                "total_count": total_count,
                "displayed_count": len(formatted_subjects),
                "search_context": "Your learning subjects overview"
            }
            
        except Exception as e:
            logger.exception(f"Error processing subjects: {e}")
            return {
                "error": "Processing Error", 
                "message": f"Error processing subjects: {str(e)}",
                "subjects": [],
                "total_count": 0,
                "displayed_count": 0
            }
    
    # Call with error handling wrapper
    return await _handle_api_call("get_subjects", core_logic)

# --- Command Line Arguments ---

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Linko MCP - Access your Linko study notes and resources")
    parser.add_argument("--username", help="Linko email address (overrides environment variable)")
    parser.add_argument("--password", help="Linko password (overrides environment variable)")
    parser.add_argument("--base-url", help="Linko API base URL (default: https://www.linko.study)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def setup_debug_logging():
    """Configure debug logging for all relevant modules."""
    logging.getLogger('linko_mcp').setLevel(logging.DEBUG)
    logging.getLogger('linko_mcp.auth').setLevel(logging.DEBUG)
    logging.getLogger('linko_mcp.api_client').setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled")

async def check_authentication(cmd_args) -> Tuple[bool, Optional[LinkoAPIClient]]:
    """Check authentication status and return auth result and API client."""
    
    # Set logging level based on debug flag
    if cmd_args.debug:
        setup_debug_logging()
    
    # Create API client with specified base URL if provided
    client = LinkoAPIClient(base_url=cmd_args.base_url)
    
    # Check for stored token first
    token_data = auth.get_stored_token()
    if token_data and 'access_token' in token_data:
        token = token_data['access_token']
        logger.info("Found stored access token, verifying...")
        
        if await auth.verify_token(token, base_url=cmd_args.base_url):
            logger.info("Stored token is valid.")
            return True, client
        else:
            logger.warning("Stored token is invalid or expired.")
            
            # Try refreshing token
            logger.info("Attempting to refresh token...")
            new_token = await auth.refresh_access_token(base_url=cmd_args.base_url)
            if new_token:
                logger.info("Token refreshed successfully.")
                return True, client
            else:
                logger.warning("Token refresh failed, need to re-authenticate.")
    else:
        logger.info("No stored token found.")
    
    # If we get here, we need authentication with username/password
    username = cmd_args.username
    password = cmd_args.password
    
    # If not provided via command line, try environment variables
    if not username or not password:
        env_username, env_password, _ = auth.get_credentials_from_env()
        username = username or env_username
        password = password or env_password
    
    # If still not available, prompt user (only works in interactive mode)
    if not username:
        logger.info("Username not provided via arguments or environment variables.")
        try:
            username = input("Linko email: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False, None
    
    if not password:
        logger.info("Password not provided via arguments or environment variables.")
        try:
            password = getpass.getpass("Linko password: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False, None
    
    # Attempt authentication
    if not username or not password:
        logger.error("Username and password are required. Please provide via command line arguments, environment variables, or interactive prompt.")
        return False, None
    
    logger.info(f"Authenticating with username: {username}")
    auth_result = await auth.authenticate(
        username=username,
        password=password,
        base_url=cmd_args.base_url
    )
    
    if auth_result:
        logger.info("Authentication successful.")
        return True, client
    else:
        logger.error("Authentication failed. Please check your credentials.")
        return False, None

# --- Startup/Shutdown Functions ---

async def startup(args): 
    """
    Performs asynchronous setup tasks before starting MCP.
    
    This function initializes the global api_client variable.
    """
    global api_client  # Modifies global API client
    logger.info("Starting Linko MCP setup")
    
    # Perform authentication check and get API client
    authenticated, client = await check_authentication(args)
    
    if not authenticated:
        logger.critical("Authentication failed. MCP cannot start.")
        return False
        
    # Store the authenticated client
    api_client = client
    logger.info("Linko MCP ready to serve requests.")
    return True

async def shutdown():
    """
    Performs asynchronous cleanup tasks.
    
    This function cleans up resources such as the global API client.
    """
    global api_client  # Uses and potentially modifies global API client
    
    if api_client:
        logger.info("Closing API client connection...")
        await api_client.close()
        api_client = None  # Clear reference to allow garbage collection
        
    logger.info("Async shutdown complete.")

# --- Main Entry Point ---

def main():
    """
    Main entry point for starting the MCP server.
    
    This function:
    1. Parses command line arguments
    2. Sets up logging based on debug flag
    3. Authenticates with Linko and initializes the API client
    4. Starts the MCP server if authentication succeeds
    5. Handles proper cleanup on exit
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    global cmd_args
    
    # Parse command-line arguments
    cmd_args = parse_args()
    
    # Configure logging level if specified
    if cmd_args.debug:
        setup_debug_logging()
    
    # Initialize exit code to success
    exit_code = 0
    startup_success = False
    
    try:
        # Run async startup tasks first (this will initialize api_client)
        startup_success = asyncio.run(startup(cmd_args))
        
        if startup_success:
            print("\n✅ Linko MCP Authenticated and Ready. Starting server...")
            logger.info("Authentication successful, starting MCP server loop")
            # Run the blocking MCP server
            mcp.run()
        else:
            print("\n❌ MCP startup failed due to authentication error. Exiting.")
            exit_code = 1
            
    except KeyboardInterrupt:
        print("\n🔌 Shutting down Linko MCP due to KeyboardInterrupt...")
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
                asyncio.run(shutdown())
            except Exception as e:
                logger.error(f"Error during shutdown cleanup: {e}", exc_info=True)
                
        logger.info("Linko MCP process finished.")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 