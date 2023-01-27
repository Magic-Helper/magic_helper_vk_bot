from loguru import logger

from app.core.utils import singleton
from app.services.discord.discord_api import DiscordAPI
from app.services.discord.exceptions import FriendNotFound
from app.services.discord.models import DiscordRelationship, DiscordUser


@singleton
class DiscordClient:
    def __init__(self):
        self._api = DiscordAPI()

    def set_token(self, token: str) -> None:
        self._api.set_token(token)

    async def get_discord_id(self, discord_tag: str) -> int:
        """Get discord id by discord tag.

        Raises:
            FriendNotFound: If friend not found.
            UnccorectDiscordTag: If discord tag is uncorrect.
        """
        await self._api.add_friend(discord_tag)

        friends = await self._api.get_friends()
        friend = self._find_friend_tag(discord_tag, friends)
        await self._try_remove_friend(friend.id)

        return friend.id

    async def _try_remove_friend(self, discord_id: int) -> None:
        try:
            await self._api.remove_friend(str(discord_id))
        except Exception as e:
            logger.error(f'Failed to delete friend {discord_id}.\nError: {e}')

    def _find_friend_tag(self, discord_tag: str, friend_list: list[DiscordRelationship]) -> DiscordRelationship:
        for friend in friend_list:
            friend_tag = self._get_tag_from_user(friend.user)
            if friend_tag == discord_tag:
                return friend

        raise FriendNotFound

    def _get_tag_from_user(self, user: DiscordUser) -> str:
        return f'{user.username}#{user.discriminator}'
