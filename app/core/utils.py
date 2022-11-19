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
