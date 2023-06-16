from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns

other_cmds_labeler = BotLabeler()

BASE_STEAM_LINK = 'https://steamcommunity.com/profiles/'


@other_cmds_labeler.message(rules.VBMLRule(patterns.link_cmd))
async def get_link_by_steamid(message: Message, steamid: str) -> None:
    await message.answer(BASE_STEAM_LINK + steamid)
