import re

from loguru import logger

from app.core.constants import REGEX_PATTERNS
from app.core.typedefs import StartedCheck, Nickname
from app.core.cmd_args import StopCheckArgs, BanCheckArgs


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
            logger.error(f"Could not find match {parser_name_} in {message}")
        return (match[0]) if len(match) != 0 else None


class MagicRecordMessageParser(MessageParser):
    def parse_started_check(self, message: str) -> StartedCheck:
        """Parses a message about a started check.

        Args:
            message (str): A message to parse.

        """
        logger.debug(f"Parsing started check from {message}")
        moder_vk = self.parse(REGEX_PATTERNS.VK_ID, message, 'Moder VK ID')
        nickname = self.parse(REGEX_PATTERNS.NICKNAME, message, 'Nickname')
        server = self.parse(REGEX_PATTERNS.SERVER_NUMBER, message, 'Server number')
        steamid = self.parse(REGEX_PATTERNS.STEAMID, message, 'SteamID')
        return StartedCheck(moder_vk=moder_vk, nickname=nickname, server=server, steamid=steamid)

    def parse_end_check(self, message: str) -> Nickname:
        """Parses a message about a stoped check.

        Args:
            message (str): A message to parse.

        """
        logger.debug(f"Parsing stoped check from {message}")

        nickname = self.parse(REGEX_PATTERNS.NICKNAME, message, 'Nickname')
        return nickname
    
    


class ArgsParser:
    """Represents a args parser."""

    def parse_cc(self, args: list[str]) -> StopCheckArgs:
        """Parses a stop check args.

        Args:
            args (list[str]): A list of args.

        """
        logger.debug(f"Parsing stop check args from {args}")
        server = int(args[0])
        steamid = int(args[1])
        return StopCheckArgs(server=server, steamid=steamid)

    def parse_ban(self, args: list[str]) -> BanCheckArgs:
        """Parses a ban check args.

        Args:
            args (list[str]): A list of args.

        """
        logger.debug(f"Parsing ban check args from {args}")
        server = int(args[0])
        steamid = int(args[1])
        reason = args[2]
        return BanCheckArgs(server=server, steamid=steamid, reason=reason)

record_message_parser = MagicRecordMessageParser()
args_parser = ArgsParser()