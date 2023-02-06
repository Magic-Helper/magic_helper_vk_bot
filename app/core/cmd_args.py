from dataclasses import dataclass

from pendulum import DateTime


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


@dataclass
class GetStatsArgs:
    """
    server: int
    steamid: int
    """

    server: int
    steamid: int


@dataclass
class GetReportsArgs:
    """
    report_start_time: pendelum.DateTime
    min_reports: int
    """

    report_start_time: DateTime
    min_reports: int


@dataclass
class GetReportCount:
    """
    steamid: int
    report_start_time: pendelum.DateTime
    """

    steamid: int
    report_start_time: DateTime
