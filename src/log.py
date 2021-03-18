# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence

import logging


def setup_custom_logger(name: str) -> logging.Logger:
    custom_format = ("%(asctime)s - %(levelname)s %(filename)s " +
                     "%(funcName)s %(lineno)d: %(message)s")
    formatter = logging.Formatter(fmt=custom_format)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)
    return custom_logger


logger = setup_custom_logger('global')
