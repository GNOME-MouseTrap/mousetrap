import logging


def get_logger(name):
    return logging.getLogger(name)


def _initialize_mousetrap_logger():
    app_logger = logging.getLogger('mousetrap')
    app_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)


_initialize_mousetrap_logger()
