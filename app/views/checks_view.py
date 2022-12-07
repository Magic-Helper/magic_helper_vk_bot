from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from app.core.typedefs import ModerChecksInformation, TimeInterval


class CheckView:
    def __init__(
        self,
        checks_info: Union[list['ModerChecksInformation'], 'ModerChecksInformation'],
        time_interval: 'TimeInterval',
    ):
        """Check view.

        Args:
            checks (Union[list[Check], Check]): Checks.
            time_interval (TimeInterval): Time interval.
        """
        if not isinstance(checks_info, list):
            checks_info = [checks_info]
        self.checks_info = checks_info
        self.time_interval = time_interval

    def __repr__(self) -> str:
        return self._get_check_view()

    def _get_check_view(self) -> str:
        """Get check view."""
        cap_text = self._get_cap_text()
        body_text = self._get_body_text()
        text = cap_text + '\n\n' + body_text
        return text

    def _get_cap_text(self) -> str:
        """Get cap text."""
        start_time = self.time_interval.start.strftime('%d.%m.%Y')
        end_time = self.time_interval.end.strftime('%d.%m.%Y')
        return f'Проверки за период с {start_time} по {end_time}'

    def _get_body_text(self) -> str:
        body = ''
        for check in self.checks_info:
            body += self._get_check_text(check)
        return body

    def _get_check_text(self, check_info: 'ModerChecksInformation') -> str:
        """Get checks text."""
        if check_info.checks_count == 0:
            return ''

        return f'📝{check_info.moderator} - {check_info.checks_count} проверок\n'
