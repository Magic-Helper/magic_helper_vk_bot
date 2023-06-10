from app.entities import OnCheck
from app.views import ABCUserView


class OnCheckView(ABCUserView):
    def __init__(self, on_check_storage: dict[str, OnCheck]) -> None:
        self.on_check_storage = on_check_storage

    def render(self) -> str:
        if not self.on_check_storage:
            return 'Нет игроков на проверке'
        text = ''
        for steamid, on_check in self.on_check_storage.items():
            text += f'{steamid} - {on_check}\n'
        return text
