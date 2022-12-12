import logging

import numpy


logger = logging.getLogger(__name__)


def generate_mandelbrot_set(
    analysis,
    number_of_iterations=64,
    x_increment=0.01,
    y_increment=0.01,
    monitor_message_period=100,
    stop_signal=False,
):
    """Compute the heightmap for a Mandelbrot set until the stop signal is received. Note that this is implemented
    deliberately inefficiently as it's being used for load-testing.

    :param octue.resources.Analysis analysis: the analysis that called this function - this must be provided so monitor messages can be sent to the parent periodically
    :param int number_of_iterations: the number of iterations limit used to compute the fractal
    :param int x_increment: the amount to increment the x value by between points
    :param int y_increment: the amount to increment the y value by between points
    :param int monitor_message_period: the period (in the number of heights calculated) at which to send monitor messages to the parent
    :param threading.Event stop_signal: when this becomes `True`, stop and return the Mandelbrot set so far
    :return (numpy.ndarray, numpy.ndarray, numpy.ndarray): x, y, z values of pixel locations in the x, y complex plane and a corresponding heightmap z, with which you can plot a fancy looking 3d fractal
    """
    x_array = []
    y_array = []
    z_array = []

    x = -1.5
    y_range = -1.26, 1.26

    # Calculate heights until the stop signal is received.
    while True:
        x += x_increment

        for i, y in enumerate(numpy.arange(y_range[0], y_range[1], y_increment)):
            x_old = 0
            y_old = 0
            iteration = 1

            while (iteration <= number_of_iterations) and (x_old**2 + y_old**2 < 4):
                x_new = x_old**2 - y_old**2 + x
                y_new = 2 * x_old * y_old + y
                x_old = x_new
                y_old = y_new
                iteration += 1

            x_array.append(x)
            y_array.append(y)
            z_array.append(iteration)

            if i % monitor_message_period == 0:
                analysis.send_monitor_message({"x": x_old, "y": y_old, "z": iteration})

            if stop_signal.is_set():
                logger.warning("Stop signal received - returning early.")
                return x_array, y_array, z_array
