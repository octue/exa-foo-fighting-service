import logging

from exa_mandelbrot_service.mandelbrot import generate_mandelbrot_set


logger = logging.getLogger(__name__)


class App:
    def __init__(self, analysis):
        """Construct an Octue app to be run as a service.

        :param octue.resources.Analysis analysis:
        :return None:
        """
        self.analysis = analysis

    def run(self):
        """Generate a Mandelbrot set and plot it.

        :return None:
        """
        logger.info("Starting analysis.")

        x, y, z = generate_mandelbrot_set(
            width=self.analysis.configuration_values["width"],
            height=self.analysis.configuration_values["height"],
            x_range=self.analysis.configuration_values["x_range"],
            y_range=self.analysis.configuration_values["y_range"],
            number_of_iterations=self.analysis.configuration_values["n_iterations"],
        )

        # Create the data and layout for the plot.
        data = {
            "x": x.tolist(),
            "y": y.tolist(),
            "z": z.tolist(),
            "colorscale": self.analysis.configuration_values["color_scale"],
            "type": "surface",
        }

        layout = {
            "title": f"Mandelbrot set with {self.analysis.configuration_values['n_iterations']} iterations",
            "width": self.analysis.configuration_values["width"],
            "height": self.analysis.configuration_values["height"],
        }

        self.analysis.output_values = {"data": data, "layout": layout}
        logger.info("Finished analysis.")
