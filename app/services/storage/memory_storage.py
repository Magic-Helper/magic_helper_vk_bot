from typing import TYPE_CHECKING

from app.core.utils import singleton

if TYPE_CHECKING:
    from app.core.typedefs import CheckStage, Nickname, OnCheckData, Steamid


@singleton
class OnCheckMemoryStorage:
    """
    Represents a memory storage for storing data about users who are currently in the process of checking.

    The data is stored in the form of a dictionary, where the key is the steamid of the user,
    Programm have only one instance of this class.

    Attributes:
        _on_check: A dictionary that stores data about users who are currently in the process of checking.
        _nicknames_to_steamids: A dictionary that stores the relationship between the nickname and the steamid of the user.

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

    def set_on_check(
        self, steamid: 'Steamid', nickname: 'Nickname', on_check_data: 'OnCheckData'
    ) -> None:
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
