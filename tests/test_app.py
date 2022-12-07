import logging
import os
import unittest

from octue import Runner


PACKAGE_ROOT = os.path.dirname(os.path.dirname(__file__))


class TestApp(unittest.TestCase):
    def test_app(self):
        """Test that the app can create a simple Mandelbrot set."""
        runner = Runner(
            app_src=os.path.join(PACKAGE_ROOT, "exa_mandelbrot_service"),
            twine=os.path.join(PACKAGE_ROOT, "twine.json"),
            configuration_values={"duration_check_interval": 10},
        )

        monitor_messages = []

        analysis = runner.run(
            input_values={
                "width": 100,
                "height": 100,
                "n_iterations": 64,
                "color_scale": "YlGnBu",
                "type": "png",
                "x_range": [-1.5, 0.6],
                "y_range": [-1.26, 1.26],
                "test_id": 33,
                "max_duration": 100,
            },
            handle_monitor_message=monitor_messages.append,
        )

        self.assertEqual(analysis.output_values["layout"]["height"], 100)
        self.assertEqual(analysis.output_values["layout"]["width"], 100)
        self.assertEqual(len(analysis.output_values["data"]["x"]), 100)
        self.assertEqual(len(analysis.output_values["data"]["y"]), 100)
        self.assertEqual(len(analysis.output_values["data"]["z"]), 100)
        self.assertGreater(len(monitor_messages), 0)

    def test_app_returns_early_if_duration_limit_reached(self):
        """Test that the app returns early if the maximum duration is reached."""
        with self.assertLogs(
            logger=logging.getLogger("exa_mandelbrot_service"),
            level=logging.WARNING,
        ) as logging_context:
            runner = Runner(
                app_src=os.path.join(PACKAGE_ROOT, "exa_mandelbrot_service"),
                twine=os.path.join(PACKAGE_ROOT, "twine.json"),
                configuration_values={"duration_check_interval": 0.1},
            )

            runner.run(
                input_values={
                    "width": 100,
                    "height": 100,
                    "n_iterations": 64,
                    "color_scale": "YlGnBu",
                    "type": "png",
                    "x_range": [-1.5, 0.6],
                    "y_range": [-1.26, 1.26],
                    "test_id": 33,
                    "max_duration": 0,
                },
                handle_monitor_message=[].append,
            )

        self.assertEqual(logging_context.records[0].message, "Stop signal received - returning early.")

    def test_app_with_randomised_duration(self):
        """Test that the maximum duration can be randomised."""
        with self.assertLogs(logger=logging.getLogger("app"), level=logging.INFO) as logging_context:
            runner = Runner(
                app_src=os.path.join(PACKAGE_ROOT, "exa_mandelbrot_service"),
                twine=os.path.join(PACKAGE_ROOT, "twine.json"),
                configuration_values={"duration_check_interval": 0.1},
            )

            runner.run(
                input_values={
                    "width": 200,
                    "height": 200,
                    "n_iterations": 64,
                    "color_scale": "YlGnBu",
                    "type": "png",
                    "x_range": [-1.5, 0.6],
                    "y_range": [-1.26, 1.26],
                    "test_id": 33,
                    "max_duration": 5,
                    "randomise_duration": True,
                },
                handle_monitor_message=[].append,
            )

        self.assertIn("Maximum duration randomised to", logging_context.records[0].message)
