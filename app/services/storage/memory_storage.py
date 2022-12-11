from typing import TYPE_CHECKING

from app.core.utils import singleton

if TYPE_CHECKING:
    from app.core.typedefs import CheckStage, Nickname, OnCheckData, Steamid
    from app.services.RCC.models import RCCPlayer


@singleton
class OnCheckMemoryStorage:
    """
    Represents a memory storage for storing data about users who are currently in the process of checking.

    The data is stored in the form of a dictionary, where the key is the steamid of the user,
    Programm have only one instance of this class.

    Attributes:
        _on_check: A dictionary that stores data about users who are currently in the process of checking.
        _nicknames_to_steamids: A dictionary that stores the relationship between the nickname and the steamid of the user.  # noqa: E501

    Methods:
        get_on_check(steamid: 'Steamid') -> 'OnCheckData':
            Returns the data of the user who is currently in the process of checking.

        set_on_check(steamid: 'Steamid', nickname: 'Nickname', on_check_data: 'OnCheckData') -> None:
            Sets the data of the user who is currently in the process of checking.

        change_state(steamid: 'Steamid', stage: 'CheckStage') -> None:
            Changes the stage of the user who is currently in the process of checking.

        get_data_by_nickname(nickname: 'Nickname') -> 'OnCheckData':
            Returns the data of the user who is currently in the process of checking by nickname.

        delete_on_check(nickname: 'Nickname') -> None:
            Deletes the data of the user who is currently in the process of checking.

    """

    def __init__(self) -> None:
        self._on_check: dict['Steamid', 'OnCheckData'] = {}
        self._nicknames_to_steamids: dict['Nickname', 'Steamid'] = {}

    def get_data_by_steamid(self, steamid: 'Steamid') -> 'OnCheckData':
        return self._on_check.get(steamid)

    def set_on_check(self, steamid: 'Steamid', nickname: 'Nickname', on_check_data: 'OnCheckData') -> None:
        self._on_check[steamid] = on_check_data
        self._nicknames_to_steamids[nickname] = steamid

    def change_state(self, steamid: 'Steamid', stage: 'CheckStage') -> None:
        self._on_check[steamid].stage = stage

    def get_data_by_nickname(self, nickname: 'Nickname') -> 'OnCheckData':
        steamid = self._nicknames_to_steamids.get(nickname)
        return self._on_check.get(steamid)

    def get_steamid(self, nickname: 'Nickname') -> 'Steamid':
        return self._nicknames_to_steamids.get(nickname)

    def delete_on_check(self, nickname: 'Nickname') -> None:
        steamid = self._nicknames_to_steamids.get(nickname)
        if steamid:
            del self._on_check[steamid]
            del self._nicknames_to_steamids[nickname]


@singleton
class RCCDataMemoryStorage:
    def __init__(self) -> None:
        self._players: dict['Steamid', 'RCCPlayer'] = {}
        self._steamids_data_exists: set['Steamid'] = set()
        self._steamids_with_no_data: set['Steamid'] = set()

    def get_player(self, steamid: 'Steamid') -> 'RCCPlayer':
        return self._players.get(steamid)

    def get_players(self, steamids: list['Steamid']) -> list['RCCPlayer']:
        return [self._players.get(steamid) for steamid in steamids]

    def add_player(self, player: 'RCCPlayer') -> None:
        self._players[player.steamid] = player

    def add_players_with_exists_data(self, steamids: list['Steamid']) -> None:
        self._steamids_data_exists.update(steamids)

    def add_players_with_no_data(self, steamids: list['Steamid']) -> None:
        self._steamids_with_no_data.update(steamids)

    def add_players(self, players: list['RCCPlayer']) -> None:
        for player in players:
            self.add_player(player)

    def get_players_data_exists(self) -> set['Steamid']:
        return self._steamids_data_exists

    def get_players_with_no_data(self) -> set['Steamid']:
        return self._steamids_with_no_data

    def clear_data(self) -> None:
        self._players.clear()
        self._steamids_data_exists.clear()
        self._steamids_with_no_data.clear()
