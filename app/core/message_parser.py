import re

from loguru import logger

from app.core.constants import REGEX_PATTERNS
from app.core.typedefs import StartedCheck


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


record_message_parser = MagicRecordMessageParser()
