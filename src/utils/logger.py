import logging


def setup_logger():
    logger = logging.getLogger(name=__name__)
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter('%(levelname)s - %(message)s - %(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
    c_handler.setFormatter(c_format)

    logger.addHandler(c_handler)

    return logger
