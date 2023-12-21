import logging
from config import LOG_FILE


def configure_logging(log_level):
    
    formatter = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filemode="a",
        filename=LOG_FILE,
        level=log_level,
        format=formatter
    )