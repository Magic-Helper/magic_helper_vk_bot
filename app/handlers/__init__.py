from .checks_cmd import labeler as checks_cmd_labeler
from .magic_records import labeler as magic_records_labeler
from .magic_records_cmd import labeler as magic_records_cmd_labeler
from .other_cmd import labeler as other_cmd_labeler
from .owner_cmd import labeler as owner_cmd_labeler
from .players_cmd import labeler as players_cmd_labeler

__all__ = [
    'magic_records_labeler',
    'checks_cmd_labeler',
    'other_cmd_labeler',
    'magic_records_cmd_labeler',
    'players_cmd_labeler',
    'owner_cmd_labeler',
]
