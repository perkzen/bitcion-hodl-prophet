import logging


def get_logger():
    logger = logging.getLogger(name=__name__)
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has handlers to prevent adding duplicate ones
    if not logger.handlers:
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)

        c_format = logging.Formatter('%(levelname)s - %(message)s - %(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
        c_handler.setFormatter(c_format)

        logger.addHandler(c_handler)

    return logger
