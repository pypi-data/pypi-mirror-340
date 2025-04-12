from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.navigate_browser_body import NavigateBrowserBody
from ...models.navigate_browser_response_200 import NavigateBrowserResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: NavigateBrowserBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/browser/session/{session_id}/navigate".format(session_id=session_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, NavigateBrowserResponse200]]:
    if response.status_code == 200:
        response_200 = NavigateBrowserResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400
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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, NavigateBrowserResponse200]]:
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
    body: NavigateBrowserBody,

) -> Response[Union[Error, NavigateBrowserResponse200]]:
    """ Navigate to URL

     Navigates the browser to a specified URL

    Args:
        session_id (UUID):
        body (NavigateBrowserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, NavigateBrowserResponse200]]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NavigateBrowserBody,

) -> Optional[Union[Error, NavigateBrowserResponse200]]:
    """ Navigate to URL

     Navigates the browser to a specified URL

    Args:
        session_id (UUID):
        body (NavigateBrowserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, NavigateBrowserResponse200]
     """


    return sync_detailed(
        session_id=session_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NavigateBrowserBody,

) -> Response[Union[Error, NavigateBrowserResponse200]]:
    """ Navigate to URL

     Navigates the browser to a specified URL

    Args:
        session_id (UUID):
        body (NavigateBrowserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, NavigateBrowserResponse200]]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NavigateBrowserBody,

) -> Optional[Union[Error, NavigateBrowserResponse200]]:
    """ Navigate to URL

     Navigates the browser to a specified URL

    Args:
        session_id (UUID):
        body (NavigateBrowserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, NavigateBrowserResponse200]
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
