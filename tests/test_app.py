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
