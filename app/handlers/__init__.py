from app.handlers.magic_helper import check_msgs_labeler, reports_msgs_labeler
from app.handlers.magic_records import (
    bans_find_labeler,
    check_cmds_labeler,
    check_payloads_labeler,
    owner_cmds_labeler,
    report_cmds_labeler,
    stats_find_labeler,
    stats_labeler,
)

magic_helper_labelers = [check_msgs_labeler, reports_msgs_labeler]
magic_records_labelers = [
    check_cmds_labeler,
    owner_cmds_labeler,
    bans_find_labeler,
    stats_find_labeler,
    stats_labeler,
    report_cmds_labeler,
    check_payloads_labeler,
]
