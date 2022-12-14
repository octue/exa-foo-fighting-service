import logging
import random
import time
from threading import Event

import numpy as np
from octue.utils.threads import RepeatingTimer

from exa_foo_fighting_service.mandelbrot import generate_mandelbrot_set


logger = logging.getLogger(__name__)

X_RANGE = (-2, 2)
Y_RANGE = (-1.26, 1.26)


class App:
    """An Octue app that generates a Mandelbrot set until the maximum duration is reached.

    :param octue.resources.Analysis analysis:
    :return None:
    """

    def __init__(self, analysis):
        self.analysis = analysis
        self._start_time = time.perf_counter()
        self._duration_checker = None
        self._stop = Event()

    def run(self):
        """Generate a Mandelbrot set until the maximum duration is reached. The duration can be randomised within the
        range 0 <= t <= `max_duration`.

        :return None:
        """
        logger.info("Starting analysis for foo-fighting test %s.", self.analysis.input_values["test_id"])

        if "max_duration" in self.analysis.input_values:
            self._calculate_mandelbrot_for_specified_duration()
        else:
            self._calculate_mandelbrot_for_specified_grid()

        # Don't return any meaningful output as this app is just for load testing.
        self.analysis.output_values = {"data": None, "layout": None}
        logger.info("Finished analysis for foo-fighting test %s.", self.analysis.input_values["test_id"])

    def _calculate_mandelbrot_for_specified_duration(self):
        logger.info("Running for specified duration.")

        if self.analysis.input_values.get("randomise_duration", False):
            self.analysis.input_values["max_duration"] = random.randint(0, self.analysis.input_values["max_duration"])
            logger.info("Maximum duration randomised to %ds.", self.analysis.input_values["max_duration"])

        self._duration_checker = RepeatingTimer(
            interval=self.analysis.configuration_values["duration_check_interval"],
            function=self._check_duration,
            kwargs={"maximum_duration": self.analysis.input_values["max_duration"]},
        )

        self._duration_checker.daemon = True
        self._duration_checker.start()

        # Pre-allocate the arrays in memory here to avoid increasing memory usage over time.
        x_array = np.linspace(X_RANGE[0], X_RANGE[1], 100)
        y_array = np.linspace(Y_RANGE[0], Y_RANGE[1], 100)
        z_array = np.zeros((100, 100))

        # Calculate the Mandelbrot set over the same grid repeatedly until the specified duration is reached.
        while not self._stop.is_set():
            generate_mandelbrot_set(self.analysis, x_array, y_array, z_array, stop_signal=self._stop)

    def _calculate_mandelbrot_for_specified_grid(self):
        logger.info("Running for specified grid size.")

        # Pre-allocate the arrays of the given grid size in memory here to avoid increasing memory usage over time.
        x_array = np.linspace(X_RANGE[0], X_RANGE[1], self.analysis.input_values["width"])
        y_array = np.linspace(Y_RANGE[0], Y_RANGE[1], self.analysis.input_values["height"])
        z_array = np.zeros((self.analysis.input_values["width"], self.analysis.input_values["height"]))

        # Calculate the Mandelbrot set over the given grid once.
        generate_mandelbrot_set(self.analysis, x_array, y_array, z_array, stop_signal=self._stop)

    def _check_duration(self, maximum_duration):
        """Check that the analysis duration hasn't exceeded the maximum duration. If it has, tell the analysis to stop.

        :param float|int maximum_duration:
        :return None:
        """
        if time.perf_counter() - self._start_time > maximum_duration:
            logger.warning("The maximum duration (%rs) has been reached - sending the stop signal.", maximum_duration)
            self._stop.set()
            self._duration_checker.cancel()
            logger.info("Duration checker thread stopped.")
