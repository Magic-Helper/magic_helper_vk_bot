from typing import TYPE_CHECKING

from app.core.typedefs import Moderator, ModerChecksInformation

if TYPE_CHECKING:
    from vkbottle import API

    from app.core.typedefs import TimeInterval
    from app.services.storage.controller import ChecksStorage


class DataCollector:
    async def collect_checks_info(
        self, time_interval: 'TimeInterval', checks_storage: 'ChecksStorage', vk_api: 'API'
    ) -> ModerChecksInformation:
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


data_collector = DataCollector()
