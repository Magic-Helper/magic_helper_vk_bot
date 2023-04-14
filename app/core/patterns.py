from vbml import Pattern

check_start = Pattern(
    """@id<moder_id:int> твоя команда выполнена.
Ответ: <nickname:str> вызван на проверку. Напишите /cc2 <server_number: int> <steamid:str> для отмены проверки.
<trash>"""
)

check_end = Pattern(
    """@id<moder_id:int> твоя команда выполнена.
Ответ: <nickname:str> больше не проверяется."""
)

check_ban = Pattern(
    """@id<moder_id: int> твоя команда выполнена.
Ответ: <nickname:str> забанен с причиной <reason:str> ."""
)
