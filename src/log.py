import logging

global logger

def setup_custom_logger(name):
    FORMAT = ("%(asctime)-s %(levelname)s %(filename)s " +
             "%(funcName)s %(lineno)d: %(message)s")
    formatter = logging.Formatter(fmt=FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

logger = setup_custom_logger('global')
