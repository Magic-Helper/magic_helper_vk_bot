from typing import TypeVar, Union

import aiohttp
from pydantic import parse_obj_as

from app.services.http_client import HTTPClient

RT = TypeVar('RT')


class APIClient:
    def __init__(self, authorization_token: str, base_url: None = None) -> None:
        self.http_client = HTTPClient(base_url, authorization_token)

    async def api_GET_request(
        self,
        url: str,
        query: dict | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.request_get(url, query=query)
        return await self._parse_response(response, response_model)

    async def api_POST_request(
        self,
        url: str,
        query: str | None = None,
        payload: dict | None = None,
        body: str | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.request_post(url, query=query, payload=payload, body=body)
        return await self._parse_response(response, response_model)

    async def api_PUT_request(
        self,
        url: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: str | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.requets_put(url, query=query, payload=payload, body=body)
        return await self._parse_response(response, response_model)

    async def api_DELETE_request(
        self,
        url: str,
        query: dict | None = None,
        response_model: RT | None = None,
    ) -> RT:
        response = await self.http_client.request_delete(url, query=query)
        return await self._parse_response(response, response_model)

    async def _parse_response(
        self,
        response: aiohttp.ClientResponse,
        response_model: RT | None = None,
    ) -> Union[RT, list[RT], None]:
        if response_model is None:
            return

        response_json = await response.json()
        if isinstance(response_json, dict):
            return response_model.parse_obj(response_json)
        elif isinstance(response_json, list):
            return parse_obj_as(list[response_model], response_json)
        else:
            raise TypeError('Not supported response_json type')
