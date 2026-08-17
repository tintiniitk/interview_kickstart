import signal
from contextlib import contextmanager


# 1. Define a custom exception for the timeout
class TimeoutException(Exception):
    pass


# 2. Create a context manager to handle the alarm setup and teardown
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    # Register the signal handler and set the alarm
    signal.signal(signal.SIGALRM, signal_handler)

    # Set interval timer (supports float seconds)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        # Disable the alarm
        signal.setitimer(signal.ITIMER_REAL, 0)
