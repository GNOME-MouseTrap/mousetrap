import logging


class MouseTrapLoggerInitializer():
    initialized = False

    @classmethod
    def initialize(cls):
        if not cls.initialized:
            cls._initialize_logger()
            cls.initialized = True

    @classmethod
    def _initialize_logger(cls):
        app_logger = logging.getLogger('mousetrap')
        app_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app_logger.addHandler(handler)


MouseTrapLoggerInitializer.initialize()
