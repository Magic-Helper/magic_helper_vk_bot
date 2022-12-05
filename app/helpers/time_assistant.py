import pendulum

from app.core import constants
from app.core.typedefs import TimeInterval


class TimeAssistant:
    def get_current_work_time(self) -> TimeInterval:
        """Get current work time interval. Like 10.01.2021 - 10.02.2021

        Returns:
            TimeInterval: Current work time.
        """
        time_now = pendulum.now()
        start = self._get_time_start(time_now)
        end = time_now
        return TimeInterval(start=start, end=end)

    def _get_time_start(self, date: pendulum.DateTime) -> pendulum.DateTime:
        """Get start time interval for work time.

        If date is bigger then constants.DAY_WORK_MOUNTH_END then return this mounth
        else return last mounth.
        """
        if date.day <= constants.DAY_WORK_MONTH_END:
            date = date.subtract(months=1)
        return pendulum.datetime(
            year=date.year, month=date.month, day=constants.DAY_WORK_MONTH_END + 1
        )


time_assistant = TimeAssistant()
