from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_browser_context_response_200 import GetBrowserContextResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/browser/session/{session_id}/context".format(session_id=session_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, GetBrowserContextResponse200]]:
    if response.status_code == 200:
        response_200 = GetBrowserContextResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, GetBrowserContextResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetBrowserContextResponse200]]:
    """ Get browser context

     Retrieves the current browser context including cookies, localStorage, etc.

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetBrowserContextResponse200]]
     """


    kwargs = _get_kwargs(
        session_id=session_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[Error, GetBrowserContextResponse200]]:
    """ Get browser context

     Retrieves the current browser context including cookies, localStorage, etc.

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetBrowserContextResponse200]
     """


    return sync_detailed(
        session_id=session_id,
client=client,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetBrowserContextResponse200]]:
    """ Get browser context

     Retrieves the current browser context including cookies, localStorage, etc.

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetBrowserContextResponse200]]
     """


    kwargs = _get_kwargs(
        session_id=session_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[Error, GetBrowserContextResponse200]]:
    """ Get browser context

     Retrieves the current browser context including cookies, localStorage, etc.

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetBrowserContextResponse200]
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,

    )).parsed
