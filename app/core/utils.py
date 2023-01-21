from typing import Any


def singleton(class_):  # noqa
    """Singleton decorator."""
    instances = {}

    def getinstance(*args, **kwargs) -> Any:  # noqa:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def get_dict_from_model(model: Any) -> dict:  # noqa ANN401
    """Get dict from sqlalchemy model."""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


seconds_per_unit = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}


def convert_to_seconds(time: str) -> int:
    """Conver date like 1d 1y 30d 1m to seconds."""
    try:
        return int(time[:-1]) * seconds_per_unit[time[-1]]
    except (ValueError, KeyError) as e:
        raise ValueError('Wrong time format') from e


def clear_none_from_list(list_: list) -> list:
    """Clear None from list."""
    return [item for item in list_ if item is not None]


def split_messages_with_lines(message: str, delimiter: str = '\n', one_message_max_length: int = 4000) -> list[str]:
    """Split message to list of messages."""
    splited_message = message.split(delimiter)
    max_line_length = len(max(splited_message, key=len))
    one_message_length = one_message_max_length // max_line_length
    messages = []
    for i in range(0, len(splited_message), one_message_length):
        message = delimiter.join(splited_message[i : i + one_message_length])
        if not message:
            continue
        messages.append(message)
    return messages
