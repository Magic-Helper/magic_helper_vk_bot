import aiohttp
from loguru import logger


class HTTPClient:
    def __init__(self, base_url: str | None = None, authorization_token: str | None = None) -> None:
        self.client = aiohttp.ClientSession(base_url=base_url)
        if authorization_token:
            self.client.headers.update(
                {
                    'Authorization': 'Bearer ' + authorization_token,
                    'Content-Type': 'application/json',
                    'accept': 'application/json',
                }
            )

    async def raw_request(
        self,
        url: str,
        http_method: str,
        query: dict | None = None,
        payload: dict | None = None,
        body: str | None = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        logger.debug(f'Make request: {http_method}: {url} | Query: {query} | Payload: {payload} | Body: {body}')
        response = await self.client.request(
            http_method, url, params=query, data=payload, json=body, ssl=False, **kwargs
        )
        await response.read()
        logger.debug(
            f'Receive response {response.request_info.method} {response.request_info.real_url}: {await response.text()}'
        )
        response.raise_for_status()
        return response

    async def request_get(self, url: str, query: dict | None = None, **kwargs) -> aiohttp.ClientResponse:
        return await self.raw_request(url, 'GET', query=query, **kwargs)

    async def request_post(
        self, url: str, query: dict | None = None, payload: dict | None = None, body: dict | None = None, **kwargs
    ) -> aiohttp.ClientResponse:
        return await self.raw_request(url, 'POST', query=query, payload=payload, body=body, **kwargs)

    async def requets_put(
        self, url: str, query: dict | None = None, payload: dict | None = None, body: dict | None = None, **kwargs
    ) -> aiohttp.ClientResponse:
        return await self.raw_request(url, 'PUT', query=query, payload=payload, body=body, **kwargs)

    async def request_delete(self, url: str, query: dict | None = None, **kwargs) -> aiohttp.ClientResponse:
        return await self.raw_request(url, 'DELETE', query=query, **kwargs)

    def __del__(self):
        if self.client and not self.client.closed:
            if self.client._connector is not None and self.client._connector_owner:
                self.client._connector._close()
            self.client._connector = None
