from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.rust_banned.models import RustBannedResponse


class EacView:
    def __init__(self, eac_info: 'RustBannedResponse'):
        self.eac_info = eac_info

    def __repr__(self) -> str:
        return self._get_eac_view()

    def _get_eac_view(self) -> str:
        """Return text for user message with eac information.

        Return:
            text for user message
        """
        if self.eac_info.is_banned:
            cap = f'{self.eac_info.steamid} - получал EAC блокировку🚫\n'
            body = self._get_body()
            text = cap + body
        else:
            text = f'{self.eac_info.steamid} - не получал EAC блокировок✅'
        return text

    def _get_body(self) -> str:
        body = f'Прошло {self.eac_info.days_ago} дней c бана\n'
        body += f'Steam: https://steamcommunity.com/profiles/{self.eac_info.steamid}\n'
        body += f'Твиттер: {self.eac_info.twitter_url}\n'
        body += f'RustBanned: https://rustbanned.com/profile/{self.eac_info.steamid}'
        return body
