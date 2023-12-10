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

report_msg = [
    Pattern(
        '<trash1> <server_number>-й сервер\nЖалоба от игрока <author_nickname>.\nНарушитель: <trash> (https://steamcommunity.com/profiles/<steamid>)'
    ),
    Pattern(
        '<server_number>-й сервер\nЖалоба от игрока <author_nickname> на игрока <trash>:\nhttps://steamcommunity.com/profiles/<steamid>'
    ),
]

get_logs_cmd = Pattern('/log <type>')
on_check_get = Pattern('/on_check')
on_check_clear = Pattern('/on_check clear')
on_check_ban = Pattern('/on_check ban <steamid>')
on_check_cancel = Pattern('/on_check cancel <steamid>')
on_check_end = Pattern('/on_check end <steamid>')

bans_cmd = [Pattern('/bans'), Pattern('/bans <days:int>')]

new_cmd = [Pattern('/new'), Pattern('/new <days:int>'), Pattern('/new <days:int> <min_stats:float>')]

kd_cmd = [Pattern('/kd'), Pattern('/kd <min_stats:float>')]

stats_help_cmd = [Pattern('/stats')]
stats_cmd = [Pattern('/stats <server:int> <steamid:int>')]

reports_help_cmd = [Pattern('/reports')]
reports_cmd = [Pattern('/reports <steamid>')]

checks_cmd = [Pattern('/checks')]

link_cmd = [Pattern('/link <steamid>')]
