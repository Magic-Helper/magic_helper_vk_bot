from vbml import Pattern

check_start_msg = Pattern(
    '[id<moder_id:int>|<any>] твоя команда выполнена.\nОтвет: <nickname> вызван на проверку. Напишите /cc2 <server_number:int> <steamid> для отмены проверки.\n<trash>'
)

check_end_msg = Pattern('[id<moder_id:int>|<any>] твоя команда выполнена.\nОтвет: <nickname> больше не проверяется.')

check_ban_msg = Pattern(
    '[id<moder_id:int>|<any>] твоя команда выполнена.\nОтвет: <nickname> забанен с причиной <trash>'
)


check_end_cmd = Pattern('/cc2 <server_number:int> <steamid>')
cancel_check_cmd = Pattern('/cc3 <server_number:int> <steamid>')
