from aiohttp import ClientResponse
from loguru import logger
from pydantic import parse_obj_as

from app.core import constants
from app.services.base_api import BaseAPI
from app.services.discord.error_codes import DiscordErrorCodes
from app.services.discord.exceptions import (
    DiscordAPIError,
    DiscordTagNotFound,
    FriendRequestDisabled,
    Unauthorized,
    UncorrectDiscordTag,
)
from app.services.discord.models import DiscordRelationship, DiscordTag


class DiscordAPI(BaseAPI):
    """Represents a Discord API."""

    API_URL = 'https://discord.com/api/v9/'

    def __init__(self, token: str = 'None') -> None:
        super().__init__()
        self._token = token
        headers = {
            'User-Agent': constants.USER_AGENT,
            'Content-Type': 'application/json',
            'Authorization': self._token,
        }
        self._session.headers.update(headers)

    def set_token(self, token: str) -> None:
        self._token = token
        self._session.headers.update({'Authorization': token})

    async def api_request(
        self,
        http_method: str,
        api_method: str,
        api_param: str | None = None,
        json: dict | None = None,
    ) -> dict:
        api_url = self.API_URL + api_method
        if api_param:
            api_url += '/' + api_param
        response = await self.raw_request(http_method=http_method, url=api_url, json=json)

        logger.debug(f'{http_method} {api_url} {api_param}: {response.status} {response.reason}')
        logger.debug('Response: {}', await response.text())

        await self.raise_for_discord_code(response)

        if response.status == 204:
            return {}
        return await response.json()

    async def raise_for_discord_code(self, response: ClientResponse) -> None:
        if response.ok:
            return

        if response.status == 400:
            await self.raises_for_400(response)
        elif response.status == 401:
            raise Unauthorized
        else:
            raise DiscordAPIError

    async def raises_for_400(self, response: ClientResponse) -> None:
        data: dict = await response.json()
        code = data.get('code')
        if code == DiscordErrorCodes.requests_disabled:
            raise FriendRequestDisabled
        elif code == DiscordErrorCodes.no_discord_tag_exists:
            raise DiscordTagNotFound
        else:
            raise DiscordAPIError(code)

    async def add_friend(self, tag: str) -> dict:
        """Add friend by discord tag.

        Raises:
            UncorrectDiscordTag: If discord tag is uncorrect.
        """
        discord_tag = self._parse_raw_tag(tag)
        add_friend_json = discord_tag.dict()
        logger.debug(f'Add friend json: {type(add_friend_json)} {add_friend_json}')
        return await self._friend_request('POST', json=add_friend_json)

    async def remove_friend(self, discord_id: str) -> dict:
        return await self._friend_request('DELETE', api_param=discord_id)

    async def get_friends(self) -> list[DiscordRelationship]:
        response = await self._friend_request('GET')
        return parse_obj_as(list[DiscordRelationship], response)

    async def _friend_request(self, http_method: str, api_param: str | None = None, json: dict | None = None) -> dict:
        api_method = 'users/@me/relationships'
        return await self.api_request(http_method, api_method, api_param=api_param, json=json)

    def _parse_raw_tag(self, raw_tag: str) -> DiscordTag:
        splited_tag = raw_tag.split('#')
        if len(splited_tag) != 2 or not splited_tag[1].isdigit():
            raise UncorrectDiscordTag(raw_tag)
        return DiscordTag(
            username=splited_tag[0],
            discriminator=splited_tag[1],
        )
