from datetime import datetime, timedelta
from orionis.luminate.facades.commands.scheduler_facade import Schedule
from orionis.luminate.contracts.console.task_manager import ITaskManager

class TaskManager(ITaskManager):
    """
    The TaskManager class is responsible for scheduling background tasks.

    Available scheduling methods:

    - onceAt(date: datetime)
    - everySeconds(seconds: int, start_date: datetime = None, end_date: datetime = None)
    - everySecond(start_date: datetime = None, end_date: datetime = None)
    - everyTwoSeconds(start_date: datetime = None, end_date: datetime = None)
    - everyFiveSeconds(start_date: datetime = None, end_date: datetime = None)
    - everyTenSeconds(start_date: datetime = None, end_date: datetime = None)
    - everyFifteenSeconds(start_date: datetime = None, end_date: datetime = None)
    - everyTwentySeconds(start_date: datetime = None, end_date: datetime = None)
    - everyThirtySeconds(start_date: datetime = None, end_date: datetime = None)
    - everyMinutes(minutes: int, start_date: datetime = None, end_date: datetime = None)
    - everyMinute(start_date: datetime = None, end_date: datetime = None)
    - everyTwoMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyThreeMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyFourMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyFiveMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyTenMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyFifteenMinutes(start_date: datetime = None, end_date: datetime = None)
    - everyThirtyMinutes(start_date: datetime = None, end_date: datetime = None)
    - hours(hours: int, start_date: datetime = None, end_date: datetime = None)
    - hourly(start_date: datetime = None, end_date: datetime = None)
    - hourlyAt(minute: int, start_date: datetime = None, end_date: datetime = None)
    - everyOddHour(minute: int, start_date: datetime = None, end_date: datetime = None)
    - everyTwoHours(minute: int, start_date: datetime = None, end_date: datetime = None)
    - everyThreeHours(minute: int, start_date: datetime = None, end_date: datetime = None)
    - everyFourHours(minute: int, start_date: datetime = None, end_date: datetime = None)
    - everySixHours(minute: int, start_date: datetime = None, end_date: datetime = None)
    - days(days: int, start_date: datetime = None, end_date: datetime = None)
    - daily(start_date: datetime = None, end_date: datetime = None)
    - dailyAt(at: str, start_date: datetime = None, end_date: datetime = None)
    - twiceDaily(first_hour: int, second_hour: int, start_date: datetime = None, end_date: datetime = None)
    - monday(at: str, start_date: datetime = None, end_date: datetime = None)
    - tuesday(at: str, start_date: datetime = None, end_date: datetime = None)
    - wednesday(at: str, start_date: datetime = None, end_date: datetime = None)
    - thursday(at: str, start_date: datetime = None, end_date: datetime = None)
    - friday(at: str, start_date: datetime = None, end_date: datetime = None)
    - saturday(at: str, start_date: datetime = None, end_date: datetime = None)
    - sunday(at: str, start_date: datetime = None, end_date: datetime = None)
    - weekly(start_date: datetime = None, end_date: datetime = None)

    Note: Start date and end date are optional. If not provided, the task will run without a specific end date.
    """

    def schedule(self, schedule: Schedule) -> None:
        """
        Schedules a task to run at a specified interval, with a defined start and end time.

        Args:
            schedule (Schedule): The schedule object containing the task's timing.
        """

        # Schedule an example task to run every 5 seconds for a duration of 30 seconds.
        schedule.command('app:example').everyFiveSeconds(start_date=datetime.now(), end_date=datetime.now() + timedelta(seconds=30))
