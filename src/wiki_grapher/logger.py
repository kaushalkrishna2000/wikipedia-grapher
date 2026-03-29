import logging


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(name)s --%(funcName)s] [%(levelname)s] : %(message)s",
        datefmt="%H:%M:%S"
    ))
    logger = logging.getLogger("wiki_grapher")
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
