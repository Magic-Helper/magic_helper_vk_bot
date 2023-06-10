from loguru import logger

from app.services.api import CheckAPI


async def try_get_checked_players(check_api: CheckAPI, steamids: list[str]) -> dict[str, int]:
    try:
        return await check_api.get_checked_players(steamids)
    except Exception as e:
        logger.exception(e)
    return {}
