import pendulum

from app.core import constants
from app.core.typedefs import TimeInterval


class TimeAssistant:
    def get_current_work_time(self) -> TimeInterval:
        """Get current work time interval. Like 10.01.2021 - 10.02.2021

        Returns:
            TimeInterval: Current work time.
        """
        time_now = pendulum.now(tz=constants.TIMEZONE)
        start = self._get_time_start(time_now)
        end = time_now
        return TimeInterval(start=start, end=end)

    def get_next_wipe_day(self) -> pendulum.DateTime:
        time_now = pendulum.now(tz=constants.TIMEZONE)
        if time_now.day_of_week > pendulum.FRIDAY:
            return self._monday_wipe_date(time_now)
        else:
            return self._friday_wipe_date(time_now)

    def _get_time_start(self, date: pendulum.DateTime) -> pendulum.DateTime:
        """Get start time interval for work time.

        If date is bigger then constants.DAY_WORK_MOUNTH_END then return this mounth
        else return last mounth.
        """
        if date.day <= constants.DAY_WORK_MONTH_END:
            date = date.subtract(months=1)
        return pendulum.datetime(
            year=date.year, month=date.month, day=constants.DAY_WORK_MONTH_END + 1, tz=constants.TIMEZONE
        )

    def _monday_wipe_date(self, time_now: pendulum.DateTime) -> pendulum.DateTime:
        days_to_monday = self._days_to_next_day(time_now, pendulum.MONDAY)
        wipe_day = time_now.add(days=days_to_monday)
        return pendulum.datetime(
            year=wipe_day.year, month=wipe_day.month, day=wipe_day.day, hour=constants.WIPE_TIME, tz=constants.TIMEZONE
        )

    def _friday_wipe_date(self, time_now: pendulum.DateTime) -> pendulum.DateTime:
        days_to_friday = self._days_to_next_day(time_now, pendulum.FRIDAY)
        wipe_day = time_now.add(days=days_to_friday)
        return pendulum.datetime(
            year=wipe_day.year, month=wipe_day.month, day=wipe_day.day, hour=constants.WIPE_TIME, tz=constants.TIMEZONE
        )

    def _days_to_next_day(self, date_now: pendulum.DateTime, day_of_week: int) -> int:
        days_to_day_of_week = day_of_week - date_now.day_of_week
        if days_to_day_of_week <= 0:
            days_to_day_of_week += 7
        return days_to_day_of_week


time_assistant = TimeAssistant()
