from app.core.constants import DAY_WORK_MONTH_END
from app.core.utils import num_to_words
from app.entities import ModeratorsCheck
from app.views.abc import ABCUserView


class ModeratorChecksView(ABCUserView):
    cap = f'Проверки модераторов за месяц (с {DAY_WORK_MONTH_END + 1} числа)'

    def __init__(self, moders_checks: list[ModeratorsCheck]) -> None:
        self.moders_checks = moders_checks

    def render(self) -> str:
        return self.cap + '\n\n' + self.body

    @property
    def body(self) -> str:
        body = ''
        for moders_check in self.moders_checks:
            check_word = self._get_check_word(moders_check.count)
            body += f'📝{moders_check.name} - {moders_check.count} {check_word}\n'
        return body

    def _get_check_word(self, count: int) -> str:
        return num_to_words(count, word_forms=('проверка', 'проверки', 'проверок'))
