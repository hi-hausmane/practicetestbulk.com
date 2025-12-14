# utils/logging_config.py - Centralized logging configuration

import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Configure application-wide logging

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path

    Returns:
        Configured logger instance
    """

    # Create logger
    logger = logging.getLogger("testgenius")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(levelname)s - %(message)s'
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger


# Create default logger instance
logger = setup_logging()


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (module name recommended)

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"testgenius.{name}")
    return logging.getLogger("testgenius")
