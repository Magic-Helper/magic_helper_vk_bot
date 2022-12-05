from eac_info.model import EACInfo

__all__ = ['EacView']


class EacView:
    def __init__(self, eac_info: EACInfo):
        self.eac_info = eac_info

    def __repr__(self) -> str:
        return self._get_eac_view()

    def _get_eac_view(self) -> str:
        """Return text for user message with eac information.

        Return:
            text for user message
        """
        if self.eac_info.is_ban:
            cap = f'{self.eac_info.steamid} - получал EAC блокировку🚫\n'
            body = self._get_body()
            text = cap + body
        else:
            text = f'{self.eac_info.steamid} - не получал EAC блокировок✅'
        return text

    def _get_body(self) -> str:
        body = f'Прошло {self.eac_info.days_since_ban} дней c бана\n\n'
        body += f'Твиттер: {self.eac_info.post_link}\n'
        body += f'Nexus: {self.eac_info.nexus_link}'
        return body
