import logging


def setup_custom_logger(name):
    FORMAT = ("%(asctime)s - %(levelname)s %(filename)s " +
              "%(funcName)s %(lineno)d: %(message)s")
    formatter = logging.Formatter(fmt=FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)
    return custom_logger


logger = setup_custom_logger('global')
