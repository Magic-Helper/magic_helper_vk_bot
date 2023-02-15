import asyncio
from typing import TYPE_CHECKING, Optional, Union

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from loguru import logger

from app.core import settings
from app.core.utils import clear_none_from_list
from app.services.base_api import BaseAPI
from app.services.RCC.models import RCCBaseResponse, RCCErrorMessages, RCCPlayer, RCCResponseStatus
from app.services.storage.memory_storage import RCCDataMemoryStorage

if TYPE_CHECKING:
    from yarl import URL

    from app.core.typedefs import Steamid


class RustCheatCheckAPI(BaseAPI):

    API_URL = 'https://rustcheatcheck.ru/panel/api/'
    API_KEY = settings.RCC_API_KEY

    def __init__(self) -> None:
        self._session = ClientSession(
            connector=TCPConnector(limit=5, limit_per_host=5), timeout=ClientTimeout(total=60 * 60)
        )
        self._rcc_cache = RCCDataMemoryStorage()

    async def api_request(
        self,
        api_url: Union[str, 'URL'],
        api_action: str,
        http_method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict | RCCBaseResponse | None:
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
        response = await self.request_json(url=api_url, http_method=http_method, params=params, data=data)
        logger.debug(f'RCC API response: {response}')

        if not response:
            return None

        if response.get('status', 'error') == 'error':
            return RCCBaseResponse(**response)

        return response

    async def get_rcc_player(self, steamid: 'Steamid') -> RCCPlayer | None:
        """Get player info from RCC."""
        if self._rcc_cache.is_steamid_cached(steamid):
            cache_data = self._rcc_cache.get_player(steamid)
            logger.debug(f'Cache data for {steamid}: {cache_data}')
            return cache_data

        params = {'player': steamid}
        api_action = 'getInfo'
        response = await self.api_request(self.API_URL, api_action, params=params)
        if response is None:
            return None

        if self._is_no_rcc_data(response):
            self._cache_no_rcc_data_player(steamid)
            return None

        rcc_player = RCCPlayer(**response)  # type: ignore[arg-type]
        self._cache_with_rcc_data_player(rcc_player)
        return rcc_player

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

    async def get_rcc_players(self, steamids: list['Steamid']) -> list['RCCPlayer']:
        tasks = []
        for steamid in steamids:
            task = asyncio.ensure_future(self.get_rcc_player_or_none(steamid))
            tasks.append(task)
        rcc_players = await asyncio.gather(*tasks)
        rcc_players = clear_none_from_list(rcc_players)
        return rcc_players

    async def get_rcc_player_or_none(self, steamid: 'Steamid') -> Optional['RCCPlayer']:
        try:
            rcc_player = await self.get_rcc_player(steamid)
        except Exception as e:
            logger.exception(e)
            return None
        else:
            logger.debug(f'rcc player {steamid}: {rcc_player}')
            return rcc_player

    def _is_no_rcc_data(self, response: RCCBaseResponse | dict) -> bool:
        if isinstance(response, RCCBaseResponse):
            if response.status == RCCResponseStatus.ERROR:
                if response.error_message == RCCErrorMessages.NO_RCC_DATA:
                    return True
        return False

    def _cache_with_rcc_data_player(self, rcc_player: RCCPlayer) -> None:
        self._rcc_cache.add_player(rcc_player)

    def _cache_no_rcc_data_player(self, steamid: 'Steamid') -> None:
        self._rcc_cache.add_cache_steamid(steamid)
