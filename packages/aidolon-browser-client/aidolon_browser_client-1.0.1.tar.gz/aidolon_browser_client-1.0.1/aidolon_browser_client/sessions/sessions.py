import os
from typing import Optional, Union

from aidolon_browser_client.client import AuthenticatedClient, Client
from aidolon_browser_client.api.session_management.list_browser_sessions import sync as list_sync
from aidolon_browser_client.api.session_management.close_all_browser_sessions import sync as close_all_sync
from aidolon_browser_client.models.error import Error
from aidolon_browser_client.models.list_browser_sessions_response_200 import ListBrowserSessionsResponse200
from aidolon_browser_client.models.close_all_browser_sessions_response_200 import CloseAllBrowserSessionsResponse200
from aidolon_browser_client.models.list_browser_sessions_status import ListBrowserSessionsStatus
from aidolon_browser_client.types import UNSET, Unset


def _get_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> AuthenticatedClient:
    """Create and return an authenticated client using the provided API key or from environment variables.
    
    Args:
        api_key: Optional API key to use. If None, will try to get from environment variable.
        base_url: Optional base URL to use. If None, will try to get from environment variable.
    
    Returns:
        An authenticated client instance
        
    Raises:
        ValueError: If no API key is provided and AIDOLONS_API_KEY environment variable is not set
    """
    if not api_key:
        api_key = os.getenv("AIDOLONS_API_KEY")
        if not api_key:
            raise ValueError(
                "AIDOLONS_API_KEY environment variable is not set and no API key was provided. "
                "Please provide an API key or set the environment variable."
            )
    
    if not base_url:
        base_url = os.getenv("AIDOLONS_API_BASE_URL", "https://api.aidolons.com/api/v1")
    
    return AuthenticatedClient(base_url=base_url, token=api_key)


def list_all_sessions(
    *,
    status: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Optional[Union[Error, ListBrowserSessionsResponse200]]:
    """List all browser sessions

    Gets all browser sessions for the authenticated user with optional status filtering

    Args:
        status: Optional string to filter sessions by status. Supported values: "active", "closed".
               If None or not provided, all sessions will be returned.
        api_key: Optional API key to use. If None, will try to get from environment variable.
        base_url: Optional base URL to use. If None, will try to get from environment variable.

    Returns:
        The response model containing session information or an error
        
    Raises:
        ValueError: If no API key is provided and AIDOLONS_API_KEY environment variable is not set
                   or if an invalid status is provided
    """
    client = _get_client(api_key=api_key, base_url=base_url)
    
    # Convert string status to enum if provided
    status_enum = UNSET
    if status is not None:
        if status.lower() == "active":
            status_enum = ListBrowserSessionsStatus.ACTIVE
        elif status.lower() == "closed":
            status_enum = ListBrowserSessionsStatus.CLOSED
        else:
            raise ValueError(f"Invalid status: {status}. Supported values are 'active' and 'closed'")
    
    return list_sync(client=client, status=status_enum)


def close_all_sessions(
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Optional[Union[CloseAllBrowserSessionsResponse200, Error]]:
    """Close all browser sessions

    Closes all active browser sessions for the authenticated user

    Args:
        api_key: Optional API key to use. If None, will try to get from environment variable.
        base_url: Optional base URL to use. If None, will try to get from environment variable.

    Returns:
        The response model confirming sessions were closed or an error
        
    Raises:
        ValueError: If no API key is provided and AIDOLONS_API_KEY environment variable is not set
    """
    client = _get_client(api_key=api_key, base_url=base_url)
    return close_all_sync(client=client)
