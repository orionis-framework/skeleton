from orionis.console.base import BaseScheduler
from orionis.console.contracts import ISchedule


class Scheduler(BaseScheduler):
    """Schedule an example queue producer independently of queue consumption."""

    def tasks(self, schedule: ISchedule) -> None:
        """
        Dispatch one example message every minute while the scheduler runs.

        Parameters
        ----------
        schedule : ISchedule
            Scheduler used to register the application's console tasks.

        Returns
        -------
        None
            Register the producer with a single concurrent instance.
        """
        schedule.command("app:dispatch-example")\
            .purpose("Enqueue the example worker message")\
            .maxInstances(1)\
            .everyMinutes(1)
