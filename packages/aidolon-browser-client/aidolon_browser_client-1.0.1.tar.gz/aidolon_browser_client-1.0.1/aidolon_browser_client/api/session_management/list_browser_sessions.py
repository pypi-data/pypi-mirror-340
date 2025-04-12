from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.list_browser_sessions_response_200 import ListBrowserSessionsResponse200
from ...models.list_browser_sessions_status import ListBrowserSessionsStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    status: Union[Unset, ListBrowserSessionsStatus] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_status: Union[Unset, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/browser/sessions",
        "params": params,
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, ListBrowserSessionsResponse200]]:
    if response.status_code == 200:
        response_200 = ListBrowserSessionsResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, ListBrowserSessionsResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    status: Union[Unset, ListBrowserSessionsStatus] = UNSET,

) -> Response[Union[Error, ListBrowserSessionsResponse200]]:
    """ List browser sessions

     Gets all browser sessions for the authenticated user with optional status filtering

    Args:
        status (Union[Unset, ListBrowserSessionsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListBrowserSessionsResponse200]]
     """


    kwargs = _get_kwargs(
        status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    status: Union[Unset, ListBrowserSessionsStatus] = UNSET,

) -> Optional[Union[Error, ListBrowserSessionsResponse200]]:
    """ List browser sessions

     Gets all browser sessions for the authenticated user with optional status filtering

    Args:
        status (Union[Unset, ListBrowserSessionsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListBrowserSessionsResponse200]
     """


    return sync_detailed(
        client=client,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    status: Union[Unset, ListBrowserSessionsStatus] = UNSET,

) -> Response[Union[Error, ListBrowserSessionsResponse200]]:
    """ List browser sessions

     Gets all browser sessions for the authenticated user with optional status filtering

    Args:
        status (Union[Unset, ListBrowserSessionsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, ListBrowserSessionsResponse200]]
     """


    kwargs = _get_kwargs(
        status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    status: Union[Unset, ListBrowserSessionsStatus] = UNSET,

) -> Optional[Union[Error, ListBrowserSessionsResponse200]]:
    """ List browser sessions

     Gets all browser sessions for the authenticated user with optional status filtering

    Args:
        status (Union[Unset, ListBrowserSessionsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, ListBrowserSessionsResponse200]
     """


    return (await asyncio_detailed(
        client=client,
status=status,

    )).parsed
