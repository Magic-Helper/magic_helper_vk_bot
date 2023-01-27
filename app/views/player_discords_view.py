class PlayerDiscordsView:
    def __init__(self, discord_id: int, discord_tag: str, banned_steamids: list[int] | None = None) -> None:
        self.discord_id = discord_id
        self.discord_tag = discord_tag
        self.banned_steamids = banned_steamids

    def __repr__(self) -> str:
        return self._get_players_discord_view()

    def _get_players_discord_view(self) -> str:
        cap_text = self._get_cap_text()
        if not self.banned_steamids:
            return cap_text
        body_text = self._get_body_text()
        text = cap_text + '\n' + body_text
        return text[:-2]

    def _get_cap_text(self) -> str:
        return f'Дискорд айди {self.discord_tag}: {self.discord_id}'

    def _get_body_text(self) -> str:
        body = 'Другие аккаунты: '
        # TODO: Убрать повторения тем, что в скобках писать сколько раз был этот дискорд
        unique_steamid = set(self.banned_steamids)  # type: ignore [arg-type]
        for steamid in unique_steamid:
            body += str(steamid)
            body += ', '
        return body
