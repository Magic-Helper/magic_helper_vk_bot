from vkbottle import DocMessagesUploader
from vkbottle.bot import BotLabeler, Message, rules

from app.core import patterns, settings
from app.core.custom_rules import FromUserIdRule, GetCheckCollector
from app.entities import CheckStage
from app.tools.on_check import CheckCollector
from app.views import OnCheckView

owner_cmds_labeler = BotLabeler()
owner_cmds_labeler.auto_rules = [FromUserIdRule(settings.OWNER_ID)]


@owner_cmds_labeler.private_message(rules.VBMLRule(patterns.get_logs_cmd))
async def get_logs(message: Message, type: str) -> None:
    upload_doc = await DocMessagesUploader(message.ctx_api).upload(
        f'logs/{type}.log', peer_id=message.peer_id, group_id=message.group_id, title=f'{type}.log'
    )
    await message.answer(attachment=upload_doc)


@owner_cmds_labeler.private_message(rules.VBMLRule(patterns.on_check_get), GetCheckCollector())
async def get_on_check(message: Message, check_collector: CheckCollector) -> None:
    await message.answer(OnCheckView(check_collector.on_check._storage).render())


@owner_cmds_labeler.private_message(rules.VBMLRule(patterns.on_check_clear), GetCheckCollector())
async def clear_on_check(message: Message, check_collector: CheckCollector) -> None:
    check_collector.clear_storages()
    await message.reply('Очищено')


@owner_cmds_labeler.message(rules.VBMLRule(patterns.on_check_ban), GetCheckCollector())
async def ban_on_check(message: Message, steamid: str, check_collector: CheckCollector) -> None:
    await check_collector.ban_check_by_steamid(steamid)
    await message.reply('Проверка завершена баном')


@owner_cmds_labeler.message(rules.VBMLRule(patterns.on_check_cancel), GetCheckCollector())
async def cancel_check(message: Message, steamid: str, check_collector: CheckCollector) -> None:
    check_collector.change_stage(steamid, CheckStage.CANCELING)
    await check_collector.end_check_by_steamid(steamid)
    await message.reply('Проверка отменена')


@owner_cmds_labeler.message(rules.VBMLRule(patterns.on_check_end), GetCheckCollector())
async def comlete_check(message: Message, steamid: str, check_collector: CheckCollector) -> None:
    check_collector.change_stage(steamid, CheckStage.STOPING)
    await check_collector.end_check_by_steamid(steamid)
    await message.reply('Проверка завершена')
