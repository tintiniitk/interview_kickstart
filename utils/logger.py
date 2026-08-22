import logging


def create_logger(log_level=logging.INFO):
    """log_level can be logging.{INFO,DEBUG,WARNING,ERROR}"""
    # CONFIGURE LOGGING LEVEL DYNAMICALLY
    # If DEBUG_MODE is True, the logger captures everything down to DEBUG.
    # If False, it defaults to INFO, ignoring debug statements.
    logging.basicConfig(
        level=log_level,
        # format="%(asctime)s - [%(levelname)s] - %(message)s"
        format="[%(levelname)s] %(message)s",
    )
    # CREATE A LOGGER INSTANCE
    return logging.getLogger(__name__)
