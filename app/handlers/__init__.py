from app.handlers.magic_helper import check_msgs_labeler
from app.handlers.magic_records import check_cmds_labeler

magic_helper_labelers = [check_msgs_labeler]
magic_records_labelers = [check_cmds_labeler]
