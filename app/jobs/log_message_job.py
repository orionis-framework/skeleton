from typing import ClassVar
from orionis.logging.contracts import ILogger
from orionis.queues import BaseJob


class LogMessageJob(BaseJob):
    """Log a message restored from persistent queue storage."""

    __slots__ = ("message",)

    message: str
    tries: ClassVar[int] = 3
    timeout: ClassVar[float] = 30.0
    backoff: ClassVar[tuple[float, ...]] = (1.0, 5.0)

    def __init__(self, message: str) -> None:
        """
        Store the message independently of runtime services.

        Parameters
        ----------
        message : str
            Text to retain in the serialized job payload.

        Returns
        -------
        None
            Initialize the job's persistent state.
        """
        self.message = message

    async def handle(self, logger: ILogger) -> None:
        """
        Log the stored message through the worker's injected logger.

        Parameters
        ----------
        logger : ILogger
            Logger resolved when the worker executes this job.

        Returns
        -------
        None
            Write an informational application log entry.
        """
        message = f"Worker message: {self.message}"
        logger.info(message)
