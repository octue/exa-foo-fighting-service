import logging


logger = logging.getLogger(__name__)


def generate_mandelbrot_set(
    analysis,
    x_array,
    y_array,
    z_array,
    number_of_iterations=64,
    monitor_message_period=10,
    stop_signal=False,
):
    """Compute the heightmap for a Mandelbrot set until the stop signal is received. Note that this is implemented
    deliberately inefficiently as it's being used for load-testing.

    :param octue.resources.Analysis analysis: the analysis that called this function - this must be provided so monitor messages can be sent to the parent periodically
    :param int number_of_iterations: the number of iterations limit used to compute the fractal
    :param int width: the width of the grid in pixels to calculate the Mandelbrot set over
    :param int height: the height of the grid in pixels to calculate the Mandelbrot set over
    :param int|float monitor_message_period: the period in seconds at which to send monitor messages to the parent
    :param threading.Event stop_signal: when this becomes `True`, stop and return the Mandelbrot set so far
    :return None:
    """
    if not analysis._periodic_monitor_message_sender_threads:
        analysis.set_up_periodic_monitor_message(
            create_monitor_message=lambda: {"x": x_old, "y": y_old, "z": iteration},
            period=monitor_message_period,
        )

    # Calculate heights until the stop signal is received.
    for i, x in enumerate(x_array):
        for j, y in enumerate(y_array):
            x_old = 0
            y_old = 0
            iteration = 1

            while (iteration <= number_of_iterations) and (x_old**2 + y_old**2 < 4):
                x_new = x_old**2 - y_old**2 + x
                y_new = 2 * x_old * y_old + y
                x_old = x_new
                y_old = y_new
                iteration += 1

                if stop_signal.is_set():
                    logger.warning("Stop signal received - returning.")
                    return

            z_array[i, j] = iteration
