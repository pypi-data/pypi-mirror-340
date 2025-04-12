import logging
import sys

logger = logging.getLogger("crawler")
logger.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
console = logging.StreamHandler(stream=sys.stdout)
console.setFormatter(console_formatter)


def log_to_console(level):
    console.setLevel(level)
    logger.addHandler(console)
