import logging
import os
import sys


def get_logger() -> logging.Logger:
    """
    Sets up logging for the application, based on the environment.

    Args:
        name (str): The name of the logger.

    Returns:
        logger.Logger: A Logger instance.
    """
    logger_instance = logging.getLogger(__name__)

    LEVEL = (
        logging.DEBUG if os.getenv("DEBUG", "false").lower == "true" else logging.INFO
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(LEVEL)
    logger_instance.addHandler(handler)

    return logger_instance


logger = get_logger()
