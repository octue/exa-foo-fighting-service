import logging

import numpy


logger = logging.getLogger(__name__)


def generate_mandelbrot_set(
    analysis,
    width,
    height,
    x_range,
    y_range,
    number_of_iterations,
    monitor_message_period=100,
    stop_signal=False,
):
    """Compute the heightmap for a mandelbrot or julia set fractal.

    Each iteration, the new value of a pixel is calculated as z = z^2 + c, where for a mandelbrot set (default)
    c is a function of the position in the complex plane (c = x + iy) or, optionally for a julia set, c is a constant

    :param octue.resources.Analysis analysis: the analysis that called this function - this must be provided so monitor messages can be sent to the parent periodically
    :param int width: Integer width of the final fractal image in pixels
    :param int height: Integer height of the final fractal image in pixels
    :param list(float)|numpy.ndarray x_range: The range of x [min, max] for which the fractal will be drawn
    :param list(float)|numpy.ndarray y_range: The range of y [min, max] for which the fractal will be drawn
    :param int number_of_iterations: the number of iterations limit used to compute the fractal
    :param None|(float, float) c: Optional 2-tuple (or other iterable) containing real and complex parts of constant coefficient c. Giving this argument will result in creation of a julia set, not the default mandelbrot set
    :param int monitor_message_period: the period (in the number of heights calculated) at which to send monitor messages to the parent
    :param threading.Event stop_signal: if this becomes `True` while the set is still being generated, stop and return the result
    :return (numpy.ndarray, numpy.ndarray, numpy.ndarray): x, y, z values of pixel locations in the x, y complex plane and a corresponding heightmap z, with which you can plot a fancy looking 3d fractal
    """
    x_array = []
    y_array = []
    z_array = []

    # Simple loop to render the fractal set. This is not efficient python and would be vectorised in production, but the
    # purpose here is just to provide a simple demo.
    for x in numpy.linspace(x_range[0], x_range[1], width):
        for i, y in enumerate(numpy.linspace(y_range[0], y_range[1], height)):
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

    logger.info("Mandelbrot set generated.")
    return x_array, y_array, z_array
