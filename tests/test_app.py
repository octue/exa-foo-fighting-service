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

        analysis = runner.run(
            input_values={
                "width": 400,
                "height": 600,
                "n_iterations": 64,
                "color_scale": "YlGnBu",
                "type": "png",
                "x_range": [-1.5, 0.6],
                "y_range": [-1.26, 1.26],
            },
            handle_monitor_message=print,
        )

        self.assertEqual(analysis.output_values["layout"]["height"], 600)
        self.assertEqual(analysis.output_values["layout"]["width"], 400)
        self.assertEqual(len(analysis.output_values["data"]["x"]), 600)
        self.assertEqual(len(analysis.output_values["data"]["y"]), 600)
        self.assertEqual(len(analysis.output_values["data"]["z"]), 600)
