from typing import TYPE_CHECKING

from vkbottle.bot import BotLabeler, rules

from app.core import constants
from app.helpers import args_parser
from app.helpers.custom_rules import GetOnCheckControllerRule, MyCommandRule

if TYPE_CHECKING:
    from vkbottle.bot import Message

    from app.services.storage.controller import OnCheckController

labeler = BotLabeler()
# Parse only messages from magic records group
labeler.auto_rules = [
    rules.FromPeerRule(constants.VK_FOR_MESSAGE.magic_records_peer_id),
    GetOnCheckControllerRule(),
]


@labeler.chat_message(MyCommandRule('cc2', args_count=2, prefixes=['/']))
async def stop_check(message: 'Message', on_check_storage: 'OnCheckController', args) -> None:
    check_info = args_parser.parse_cc(args)
    on_check_storage.stoping_check(check_info.steamid)


@labeler.chat_message(MyCommandRule('cc3', args_count=2, prefixes=['/']))
async def cancel_check(message: 'Message', on_check_storage: 'OnCheckController', args) -> None:
    check_info = args_parser.parse_cc(args)
    on_check_storage.canceling_check(check_info.steamid)
