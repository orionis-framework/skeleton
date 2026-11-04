from typing import ClassVar
from app.jobs.log_message_job import LogMessageJob
from orionis.console import Argument
from orionis.console.base import BaseCommand
from orionis.support.facades import Queue


class DispatchExampleCommand(BaseCommand):
    """Submit a persistent example job for a separate queue worker."""

    __slots__ = ()

    signature: str = "app:dispatch-example"
    description: str = "Dispatch a message to the configured job queue."
    arguments: ClassVar[list[Argument]] = [
        Argument(
            name_or_flags="--message",
            type_=str,
            default="Hello from Orionis worker.",
            help="Message to log when the queue worker processes the job.",
        ),
    ]

    async def handle(self) -> None:
        """
        Await queue submission and display the resulting job identifier.

        Returns
        -------
        None
            Submit one job using the configured connection and default queue.
        """
        identifier = await Queue.dispatch(LogMessageJob(self.getArgument("message")))
        self.success(f"Dispatched job {identifier}.")
