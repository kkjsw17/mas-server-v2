import logging
import os
import sys

from loguru import logger

from mas.utils.const import LOGGERS


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def initialize_logger():
    logging.getLogger().handlers = [InterceptHandler()]

    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=logging.INFO)]

    logger.configure(handlers=[{"sink": sys.stderr, "level": logging.INFO}])
    os.makedirs("./logs", exist_ok=True)

    pid = os.getpid()
    logger.add(f"./logs/[{pid}]_{{time}}.log")

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
