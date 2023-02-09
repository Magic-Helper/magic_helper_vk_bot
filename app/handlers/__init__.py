from .checks_cmd import labeler as checks_cmd_labeler
from .discord_cmd import labeler as discord_cmd_labeler
from .get_bans import get_bans_labeler
from .get_logs import labeler as get_logs_labeler
from .magic_records import labeler as magic_records_labeler
from .magic_records_cmd import labeler as magic_records_cmd_labeler
from .magic_reports import labeler as magic_reports_labeler
from .other_cmd import labeler as other_cmd_labeler
from .owner_cmd import labeler as owner_cmd_labeler
from .players_cmd import labeler as players_cmd_labeler
from .reports_cmd import reports_cmd_labeler

__all__ = [
    'magic_records_labeler',
    'checks_cmd_labeler',
    'other_cmd_labeler',
    'magic_records_cmd_labeler',
    'players_cmd_labeler',
    'owner_cmd_labeler',
    'magic_reports_labeler',
    'get_logs_labeler',
    'discord_cmd_labeler',
    'reports_cmd_labeler',
    'get_bans_labeler',
]
