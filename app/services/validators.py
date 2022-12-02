from pendulum import from_timestamp

from loguru import logger

from app.core import constants


def get_datetime_object(value: int):
    """Validator for datetime fields."""
    try:
        value = from_timestamp(int(value), tz=constants.TIMEZONE)
    except:
        return 0
    else:
        return value
