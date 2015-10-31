# -*- coding: utf-8 -*-

# pylint:disable=invalid-name

"""
Logging module for the Decomp libraries
This module can be overriden by the consumer application
"""
import os
import logging
import time

logger = logging.getLogger('DeComp')
logger.setLevel(logging.ERROR)

debug = logger.debug
error = logger.error
info = logger.info
warning = logger.warning


def set_logger(logpath='', level=None):
    """Logger intialization function

    :param logpath: optional filepath to save log outpput to
    :type logpath: string
    :param level: logging level to set the file logger to
    :type level: integer
    """
    logger.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(log_format)
    # add the handlers to logger
    if logpath:
        if not os.path.exists(logpath):
            raise
        logname = os.path.join(logpath, '%s-%s.log'
                               % ('DeComp', time.strftime('%Y%m%d-%H:%M')))
        file_handler = logging.FileHandler(logname)
        if level:
            file_handler.setLevel(level)
        else:
            file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # create console handler with a higher log level
    Console_handler = logging.StreamHandler()
    Console_handler.setLevel(logging.ERROR)
    #Console_handler.setFormatter(formatter)
    logger.addHandler(Console_handler)
