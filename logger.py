import logging
import sys
from logging.handlers import RotatingFileHandler

# define valid log levels
valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]


def get_logger():
    """
    common function to retrieve common log handler in project files

    Returns
    -------
    log handler
    """

    return logging.getLogger("extract-subs")


def setup_logger(log_level=None, log_file=None):
    """
    Set up logging for the whole program and return a log handler

    Parameters
    ----------
    log_level: str
        valid log level to set logging to
    log_file: str
        name of the log file to log to

    Returns
    -------
    log handler to use for logging
    """

    log_file_max_size_in_mb = 10
    log_file_max_rotation = 5

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%d/%m/%Y %H:%M:%S'

    if log_level is None or log_level == "":
        print("ERROR: log level undefined or empty. Check config please.", file=sys.stderr)
        exit(1)

    if not log_level.upper() in valid_log_levels:
        print(f"ERROR: Invalid log level: {log_level}", file=sys.stderr)
        exit(1)

    # getting logging.INFO or others
    numeric_log_level = getattr(logging, log_level.upper(), None)

    log_format = logging.Formatter(fmt=log_format, datefmt=date_format)

    # create logger instance
    logger = get_logger()

    logger.setLevel(numeric_log_level)

    # For see logs in console
    log_stream = logging.StreamHandler()
    log_stream.setFormatter(log_format)
    logger.addHandler(log_stream)

    # setup log file handler
    if log_file is not None:

        log_file_handler = None
        try:
            log_file_handler = RotatingFileHandler(
                filename=log_file,
                maxBytes=log_file_max_size_in_mb * 1024 * 1024,  # Bytes to Megabytes
                backupCount=log_file_max_rotation,
                encoding='utf-8'
            )
        except Exception as e:
            print(f"ERROR: Problems setting up log file: {e}", file=sys.stderr)
            exit(1)

        log_file_handler.setFormatter(log_format)
        logger.addHandler(log_file_handler)

    return logger
