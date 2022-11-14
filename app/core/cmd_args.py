from dataclasses import dataclass


@dataclass
class StopCheckArgs:
    """Represents a stop check args."""

    server: int
    steamid: int


@dataclass
class BanCheckArgs:
    """Represents a ban check args."""

    server: int
    steamid: int
    reason: str