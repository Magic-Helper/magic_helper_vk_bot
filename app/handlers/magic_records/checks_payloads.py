from vkbottle import GroupEventType
from vkbottle.bot import BotLabeler, MessageEvent

from app.core.custom_rules import GetProfileAPI, GetRCCAPI, PydanticPayloadRule
from app.entities.payloads import GiveCheckerAccessPayload
from app.services.api import RCCAPI, ProfileAPI

check_payloads_labeler = BotLabeler()


@check_payloads_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PydanticPayloadRule(GiveCheckerAccessPayload),
    GetRCCAPI(),
    GetProfileAPI(),
)
async def give_checker_access(
    event: MessageEvent, payload: GiveCheckerAccessPayload, rcc_api: RCCAPI, profile_api: ProfileAPI
) -> None:
    moderator = await profile_api.get_profile_by_vk(event.object.user_id)
    moder_steamid = moderator.steamid if moderator else None
    await rcc_api.give_access(payload.give_checker_steamid, moder_steamid)
    await event.show_snackbar('Доступ выдан!')
