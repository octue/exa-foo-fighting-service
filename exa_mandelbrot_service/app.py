import logging
import random
import time
from threading import Event

from octue.utils.threads import RepeatingTimer

from exa_mandelbrot_service.mandelbrot import generate_mandelbrot_set


logger = logging.getLogger(__name__)


class App:
    def __init__(self, analysis):
        """Construct an Octue app to be run as a service.

        :param octue.resources.Analysis analysis:
        :return None:
        """
        self.analysis = analysis
        self._start_time = time.perf_counter()
        self._duration_checker = None
        self._stop = Event()

    def run(self):
        """Generate a Mandelbrot set and plot it.

        :return None:
        """
        if self.analysis.input_values.get("randomise_duration", False):
            self.analysis.input_values["max_duration"] = random.randint(0, self.analysis.input_values["max_duration"])
            logger.info("Maximum duration randomised to %ds.", self.analysis.input_values["max_duration"])

        self._duration_checker = RepeatingTimer(
            interval=self.analysis.configuration_values["duration_check_interval"],
            function=self._check_duration,
            kwargs={"maximum_duration": self.analysis.input_values["max_duration"]},
        )

        try:
            self._duration_checker.daemon = True
            self._duration_checker.start()

            logger.info("Starting analysis for foo-fighting test %s.", self.analysis.input_values["test_id"])

            generate_mandelbrot_set(
                analysis=self.analysis,
                x_increment=self.analysis.input_values["width"],
                y_increment=self.analysis.input_values["height"],
                number_of_iterations=self.analysis.input_values["n_iterations"],
                monitor_message_period=10000,
                stop_signal=self._stop,
            )

            # Don't return any output as this app is for load testing.
            self.analysis.output_values = {"data": None, "layout": None}
            logger.info("Finished analysis for foo-fighting test %s.", self.analysis.input_values["test_id"])

        finally:
            self._duration_checker.cancel()

    def _check_duration(self, maximum_duration):
        """Check that the analysis duration hasn't exceeded the maximum duration. If it has, tell the analysis to stop.

        :param float|int maximum_duration:
        :return None:
        """
        if time.perf_counter() - self._start_time > maximum_duration:
            logger.warning("The maximum duration (%rs) has been reached - sending the stop signal.", maximum_duration)
            self._stop.set()
