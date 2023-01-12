from pendulum import from_timestamp

from app.core import constants
from app.core.exceptions import UncorrectDiscord


def get_datetime_object(value: int):
    """Validator for datetime fields. Get pendulum.DateTime object from timestamp."""
    try:
        value = from_timestamp(int(value), tz=constants.TIMEZONE)
    except Exception:
        return 0
    else:
        return value


def validate_discord(discord: str) -> str:
    if '#' not in discord:
        raise UncorrectDiscord
    splited_discord = discord.split('#')

    if discord.count('#') > 1:
        discord = '#'.join(splited_discord[:2])

    if len(splited_discord[1]) != 4 or not splited_discord[1].isdigit():
        raise UncorrectDiscord
    return discord
