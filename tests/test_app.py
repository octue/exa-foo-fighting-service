import logging
import os
import unittest

from octue import Runner


PACKAGE_ROOT = os.path.dirname(os.path.dirname(__file__))


class TestApp(unittest.TestCase):
    def test_app_returns_early_if_duration_limit_reached(self):
        """Test that the app returns early if the maximum duration is reached."""
        runner = Runner(
            app_src=os.path.join(PACKAGE_ROOT, "exa_mandelbrot_service"),
            twine=os.path.join(PACKAGE_ROOT, "twine.json"),
            configuration_values={"duration_check_interval": 0.1},
        )

        with self.assertLogs(
            logger=logging.getLogger("exa_mandelbrot_service"),
            level=logging.WARNING,
        ) as logging_context:
            runner.run(
                input_values={
                    "test_id": "33",
                    "max_duration": 0,
                },
                handle_monitor_message=[].append,
            )

        self.assertEqual(logging_context.records[0].message, "Stop signal received - returning.")

    def test_app_with_randomised_duration(self):
        """Test that the maximum duration can be randomised."""
        runner = Runner(
            app_src=os.path.join(PACKAGE_ROOT, "exa_mandelbrot_service"),
            twine=os.path.join(PACKAGE_ROOT, "twine.json"),
            configuration_values={"duration_check_interval": 0.1},
        )

        with self.assertLogs(logger=logging.getLogger("app"), level=logging.INFO) as logging_context:
            runner.run(
                input_values={
                    "test_id": "33",
                    "max_duration": 2,
                    "randomise_duration": True,
                },
                handle_monitor_message=[].append,
            )

        self.assertIn("Maximum duration randomised to", logging_context.records[2].message)
