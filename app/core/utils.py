def singleton(class_):
    """Singleton decorator."""
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def get_dict_from_model(model) -> dict:
    """Get dict from sqlalchemy model."""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


seconds_per_unit = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}


def convert_to_seconds(time: str):
    """Conver date like 1d 1y 30d 1m to seconds."""
    try:
        return int(time[:-1]) * seconds_per_unit[time[-1]]
    except (ValueError, KeyError):
        raise ValueError('Wrong time format')


def clear_none_from_list(list_: list) -> list:
    """Clear None from list."""
    return [item for item in list_ if item is not None]
