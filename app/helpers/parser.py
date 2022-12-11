import re

from loguru import logger

from app.core import constants
from app.core.cmd_args import BanCheckArgs, StopCheckArgs
from app.core.constants import REGEX_PATTERNS
from app.core.exceptions import CantGetTimePassed
from app.core.typedefs import Nickname, StartedCheck
from app.core.utils import convert_to_seconds


class MessageParser:
    """Represents a base message parser."""

    def parse(self, regex_pattern: str, message: str, parser_name_: str = '') -> str | None:
        """Parses a message using a regex pattern.

        Args:
            regex_pattern (str): A regex pattern.
            message (str): A message to parse.
            parser_name_ (str): A parser name for logging.

        """
        match = re.findall(regex_pattern, message)
        if match is None:
            logger.error(f'Could not find match {parser_name_} in {message}')
        return (match[0]) if len(match) != 0 else None


class MagicRecordMessageParser(MessageParser):
    def parse_started_check(self, message: str) -> StartedCheck:
        """Parse information from message about checks start.

        Args:
            message (str): A message from magic records.

        """
        logger.debug(f'Parsing started check from {message}')
        moder_vk = int(self.parse(REGEX_PATTERNS.VK_ID, message, 'Moder VK ID'))
        nickname = self.parse(REGEX_PATTERNS.NICKNAME, message, 'Nickname')
        server = int(self.parse(REGEX_PATTERNS.SERVER_NUMBER, message, 'Server number'))
        steamid = int(self.parse(REGEX_PATTERNS.STEAMID, message, 'SteamID'))
        return StartedCheck(moder_vk=moder_vk, nickname=nickname, server=server, steamid=steamid)

    def parse_end_check(self, message: str) -> Nickname:
        """Parse information from message about checks is end.

        Args:
            message (str): A message to parse.

        """
        logger.debug(f'Parsing stoped check from {message}')

        return self.parse(REGEX_PATTERNS.NICKNAME, message, 'Nickname')


class ArgsParser:
    """Represents a args parser. Helps to parse args from a message."""

    def parse_cc(self, args: list[str]) -> StopCheckArgs:
        """Parses a stop check args. Args must be in format: server, steamid, reason."""
        logger.debug(f'Parsing stop check args from {args}')
        server = int(args[0])
        steamid = int(args[1])
        return StopCheckArgs(server=server, steamid=steamid)

    def parse_ban(self, args: list[str]) -> BanCheckArgs:
        """Parses a ban check args. Args must be in format: server, steamid, reason."""
        logger.debug(f'Parsing ban check args from {args}')
        server = int(args[0])
        steamid = int(args[1])
        reason = args[2]
        return BanCheckArgs(server=server, steamid=steamid, reason=reason)

    def parse_time_passed(self, args: list[str] | None) -> int:
        try:
            if args is None:
                return convert_to_seconds(constants.DEFAULT_TIME_PASSED)
            return convert_to_seconds(args[0])
        except Exception as e:
            raise CantGetTimePassed(e)


record_message_parser = MagicRecordMessageParser()
args_parser = ArgsParser()
