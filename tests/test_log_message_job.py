from unittest.mock import AsyncMock, Mock, patch
from app.console.commands.dispatch_example_command import DispatchExampleCommand
from app.jobs.log_message_job import LogMessageJob
from orionis.logging.contracts import ILogger
from orionis.queues.serializer import JobSerializer
from orionis.test import TestCase


class TestLogMessageJob(TestCase):

    def testPayloadSurvivesConsumerRestart(self) -> None:
        """
        Restore the example job through a separately initialized serializer.

        Returns
        -------
        None
            Verify that persistent state survives a producer/consumer boundary.
        """
        producer = JobSerializer()
        identity, payload = producer.encode(LogMessageJob("Persisted message"))
        consumer = JobSerializer()
        consumer.register(LogMessageJob)
        restored = consumer.decode(identity, payload)

        self.assertIsInstance(restored, LogMessageJob)
        self.assertEqual(restored.message, "Persisted message")
        self.assertEqual(identity, "app.jobs.log_message_job:LogMessageJob")

    async def testRestoredJobUsesInjectedLogger(self) -> None:
        """
        Execute a restored job using a logger supplied by the consumer.

        Returns
        -------
        None
            Verify that services are supplied after deserialization.
        """
        serializer = JobSerializer()
        identity, payload = serializer.encode(LogMessageJob("Queued message"))
        restored = serializer.decode(identity, payload)
        logger = Mock(spec=ILogger)

        await restored.handle(logger)

        logger.info.assert_called_once_with("Worker message: Queued message")

    async def testDispatchCommandAwaitsSubmission(self) -> None:
        """
        Submit the command's payload and await queue acknowledgement.

        Returns
        -------
        None
            Verify that invoking the command actually dispatches one job.
        """
        dispatch = AsyncMock(return_value="example-job-id")
        with (
            patch.object(DispatchExampleCommand, "getArgument", return_value="Queued"),
            patch.object(DispatchExampleCommand, "success") as success,
            patch(
                "app.console.commands.dispatch_example_command.Queue",
                Mock(dispatch=dispatch),
            ),
        ):
            await DispatchExampleCommand().handle()

        dispatch.assert_awaited_once()
        self.assertEqual(dispatch.call_args.args[0].message, "Queued")
        success.assert_called_once_with("Dispatched job example-job-id.")
