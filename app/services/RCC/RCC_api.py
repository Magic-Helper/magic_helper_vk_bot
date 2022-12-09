import asyncio
from typing import TYPE_CHECKING, Union

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from app.core import settings
from app.services.base_api import BaseAPI
from app.services.RCC.models import RCCBaseResponse, RCCPlayer

if TYPE_CHECKING:
    from yarl import URL

    from app.core.typedefs import Steamid


class RustCheatCheckAPI(BaseAPI):

    API_URL = 'https://rustcheatcheck.ru/panel/api/'
    API_KEY = settings.RCC_API_KEY

    def __init__(self) -> None:
        self._session = ClientSession(connector=TCPConnector(limit=5, limit_per_host=5))
        self._session.headers.update({'User-Agent': settings.SERVER_TITLE})

    async def api_request(
        self,
        api_url: Union[str, 'URL'],
        api_action: str,
        http_method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict | None:
        """Make a request to the RCC API.

        If the request is successful, the response will be returned as a dict.
        If the request is unsuccessful, None will be returned.

        Args:
            api_url (Union[str, URL]): API URL.
            api_action (str): API action.
            http_method (str, optional): HTTP method. Defaults to 'GET'.
            params (dict, optional): Request params. Defaults to None.
            data (dict, optional): Request data. Defaults to None.
        """
        if params:
            params.update({'action': api_action})
            params.update({'key': self.API_KEY})

        logger.debug(f'RCC API request: {api_url} {http_method} {params}')
        response = await super().api_request(
            api_url, http_method=http_method, params=params, data=data
        )
        logger.debug(f'RCC API response: {response}')

        if response.get('status', 'error') == 'error':
            return None

        return response

    async def get_rcc_player(self, steamid: 'Steamid') -> RCCPlayer | None:
        """Get player info from RCC."""
        params = {'player': steamid}
        api_action = 'getInfo'
        response = await self.api_request(self.API_URL, api_action, params=params)
        if not response:
            return None
        return RCCPlayer(**response)

    async def get_rcc_players(self, steamids: list['Steamid']) -> list[RCCPlayer] | None:
        """Get players info from RCC."""
        tasks = []
        for steamid in steamids:
            task = asyncio.ensure_future(self.get_rcc_player(steamid))
            tasks.append(task)
        rcc_players = await asyncio.gather(*tasks)
        return rcc_players

    async def give_checker_accesss(
        self, player_steamid: 'Steamid', moder_steamid: 'Steamid' = 0
    ) -> RCCBaseResponse | None:
        """Give checker access to player."""
        params = {
            'player': player_steamid,
            'moder': moder_steamid,
        }
        api_action = 'addPlayer'
        response = await self.api_request(self.API_URL, api_action, params=params)
        if not response:
            return None
        return RCCBaseResponse(**response)
