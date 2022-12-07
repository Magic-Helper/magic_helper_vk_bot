from typing import TYPE_CHECKING

from app.core.typedefs import Moderator, ModerChecksInformation

if TYPE_CHECKING:
    from vkbottle import API

    from app.core.typedefs import TimeInterval
    from app.services.storage.controller import ChecksStorageController
    from app.services.storage.memory_storage import RCCDataMemoryStorage
    from app.services.RCC.RCC_api import RustCheatCheckAPI
    from app.services.RCC.models import RCCPlayer
    from app.services.magic_rust.models import Player


class DataCollector:
    async def collect_checks_info(
        self,
        time_interval: 'TimeInterval',
        checks_storage: 'ChecksStorageController',
        vk_api: 'API',
    ) -> list[ModerChecksInformation]:
        moders = await checks_storage.get_moders()
        checks_info = []
        for moder_vk in moders:
            checks_count = await checks_storage.get_moder_checks_count(moder_vk, time_interval)
            moderator_vk = (await vk_api.users.get(user_ids=moder_vk))[0]
            checks_info.append(
                ModerChecksInformation(
                    moderator=Moderator(
                        vk_id=moder_vk,
                        name=moderator_vk.first_name,
                        surname=moderator_vk.last_name,
                    ),
                    checks_count=checks_count,
                )
            )
        return checks_info

    async def collect_rcc_data_and_caching(
        self,
        online_players: list['Player'],
        rcc_api: 'RustCheatCheckAPI',
        rcc_memory_storage: 'RCCDataMemoryStorage',
    ) -> list['RCCPlayer']:
        steamids_with_data = rcc_memory_storage.get_players_data_exists()
        online_players_steamids = [player.steamid for player in online_players]

        online_steamids_without_data = list(set(online_players_steamids) - steamids_with_data)
        online_steamids_with_rcc_data = [
            steamid for steamid in online_players_steamids if steamid in steamids_with_data
        ]

        rcc_players = await rcc_api.get_rcc_players(online_steamids_without_data)
        exists_players = rcc_memory_storage.get_players(online_steamids_with_rcc_data)

        rcc_memory_storage.add_players(rcc_players)

        return rcc_players + exists_players


data_collector = DataCollector()
