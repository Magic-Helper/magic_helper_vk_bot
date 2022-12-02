from typing import TYPE_CHECKING, Union, Callable, Any

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from app.core import settings

if TYPE_CHECKING:
    from yarl import URL


class BaseAPI:
    """Represents a base API."""

    def __init__(self) -> None:
        self._session = ClientSession(connector=TCPConnector(limit=14))
        self._session.headers.update({'User-Agent': settings.SERVER_TITLE})

    async def request_json(
        self,
        url: Union[str, 'URL'],
        http_method: str,
        params: dict | None = None,
        data: dict | None = None,
        encoding: str = 'utf-8',
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
        response = await self._session.request(http_method, url, params=params, data=data)
        try:
            return await response.json(content_type=None)
        except Exception as e:
            message = str(e) + str(params)
            logger.error(message)
            return None

    async def api_request(
        self,
        api_url: Union[str, 'URL'],
        api_method: str | None = None,
        http_method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict:
        """Make a request to API and return JSON response.

        Args:
            api_method (str): API method.
            http_method (str, optional): HTTP method. Defaults to 'GET'.
            params (dict, optional): Parameters. Defaults to None.
            data (dict, optional): Data. Defaults to None.

        Returns:
            dict: JSON response.
        """
        if api_method:
            api_url = api_url + api_method
        return await self.request_json(api_url, http_method, params, data)

    def __del__(self):
        if self._session and not self._session.closed:
            if self._session._connector is not None and self._session._connector_owner:
                self._session._connector.close()
            self._session._connector = None
