import pendulum

from app.core import constants
from app.core.typedefs import TimeInterval


class TimeAssistant:
    def get_current_work_time(self) -> TimeInterval:
        """Get current work time.

        Returns:
            TimeInterval: Current work time.
        """
        time_now = pendulum.now()
        start = self._get_time_start(time_now)
        end = time_now
        return TimeInterval(start=start, end=end)

    def _get_time_start(self, date: pendulum.DateTime) -> pendulum.DateTime:
        """Get start time.

        Args:
            date (pendulum.DateTime): Date.

        Returns:
            pendulum.DateTime: Start time.
        """
        if date.day <= constants.DAY_WORK_MONTH_END:
            date = date.subtract(months=1)
        return pendulum.datetime(
            year=date.year, month=date.month, day=constants.DAY_WORK_MONTH_END + 1
        )


time_assistant = TimeAssistant()
