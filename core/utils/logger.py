import logging
import sys


def configure_logging():
    """Configure logging to only use console output"""
    logging_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(logging_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO, handlers=[console_handler], format=logging_format
    )
