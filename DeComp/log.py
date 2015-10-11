
import logging

logger = logging.getLogger('DeComp')
logger.setLevel(logging.ERROR)

debug = logger.debug
error = logger.error
info = logger.info
warning = logger.warning


def set_logger(logpath='', level=None):
    logger.setLevel(log_levels['INFO'])
    # create formatter and add it to the handlers
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(log_format)
    # add the handlers to logger
    if logpath:
        ensure_dirs(logpath, mode=dirmode, fatal=True)
        os.umask(filemask)
        logname = os.path.join(logpath,
            '%s-%s.log' % (namespace, time.strftime('%Y%m%d-%H:%M')))
        file_handler = logging.FileHandler(logname)
        if level:
            file_handler.setLevel(log_levels[level])
        else:
            file_handler.setLevel(log_levels['DEBUG'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # create console handler with a higher log level
    Console_handler = logging.StreamHandler()
    Console_handler.setLevel(logging.ERROR)
    #Console_handler.setFormatter(formatter)
    logger.addHandler(Console_handler)
