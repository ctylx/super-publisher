import logging
import logging.config


logging.config.fileConfig("logging.conf", encoding="utf-8")
logger = logging.getLogger()
