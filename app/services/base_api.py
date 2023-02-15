from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from aiohttp import ClientResponse, ClientSession, TCPConnector
from loguru import logger

from app.core import settings

if TYPE_CHECKING:
    from yarl import URL


class BaseAPI(ABC):
    """Represents a base API."""

    def __init__(self) -> None:
        self._session = ClientSession(connector=TCPConnector(limit=10))
        self._session.headers.update({'User-Agent': settings.SERVER_TITLE})

    async def request_json(
        self,
        url: Union[str, 'URL'],
        http_method: str,
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
    ) -> dict | None:
        """Make a request to API and return JSON response.

        Args:
            url (Union[str, URL]): URL.
            http_method (str): HTTP method.
            params (dict, optional): Parameters. Defaults to None.
            data (dict, optional): Data. Defaults to None.

        Returns:
            dict: JSON response.
        """
        response = await self.raw_request(http_method=http_method, url=url, params=params, data=data, json=json)
        try:
            return await response.json(content_type=None)
        except Exception as e:
            message = str(e) + str(params) + str(response) + await response.text()
            logger.error(message)
            return None

    async def raw_request(
        self,
        url: Union[str, 'URL'],
        http_method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
    ) -> ClientResponse:
        async with self._session.request(http_method, url, params=params, data=data, json=json) as response:
            await response.read()
        return response

    @abstractmethod
    async def api_request(
        self,
        http_method: str = 'GET',
        api_method: str | None = None,
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
    ) -> dict | None:
        ...

    def __del__(self):
        self._session._connector._close()
