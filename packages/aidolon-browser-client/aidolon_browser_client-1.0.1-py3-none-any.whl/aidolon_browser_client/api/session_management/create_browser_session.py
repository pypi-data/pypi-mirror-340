from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_browser_session_body import CreateBrowserSessionBody
from ...models.create_browser_session_response_200 import CreateBrowserSessionResponse200
from ...models.create_browser_session_response_402 import CreateBrowserSessionResponse402
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: CreateBrowserSessionBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/browser/session",
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    if response.status_code == 200:
        response_200 = CreateBrowserSessionResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401
    if response.status_code == 402:
        response_402 = CreateBrowserSessionResponse402.from_dict(response.json())



        return response_402
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBrowserSessionBody,

) -> Response[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    """ Create a new browser session

     Creates a new browser session that can be controlled via API calls.
    Returns session details including an embed URL for viewing the session in a browser.

    Args:
        body (CreateBrowserSessionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBrowserSessionBody,

) -> Optional[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    """ Create a new browser session

     Creates a new browser session that can be controlled via API calls.
    Returns session details including an embed URL for viewing the session in a browser.

    Args:
        body (CreateBrowserSessionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBrowserSessionBody,

) -> Response[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    """ Create a new browser session

     Creates a new browser session that can be controlled via API calls.
    Returns session details including an embed URL for viewing the session in a browser.

    Args:
        body (CreateBrowserSessionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateBrowserSessionBody,

) -> Optional[Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]]:
    """ Create a new browser session

     Creates a new browser session that can be controlled via API calls.
    Returns session details including an embed URL for viewing the session in a browser.

    Args:
        body (CreateBrowserSessionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateBrowserSessionResponse200, CreateBrowserSessionResponse402, Error]
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
