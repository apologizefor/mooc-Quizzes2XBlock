# coding: utf8
# luofuwen

import logging


class Util:
    @staticmethod
    def logger(config):
        fh = logging.FileHandler(config['logFile'], encoding="utf-8")
        fmt = logging.Formatter(config['logFmt'])
        fh.setFormatter(fmt)
        logger = logging.getLogger(config['logName'])
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        return logger