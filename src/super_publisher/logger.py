import os
import logging
import logging.config
import configparser


# create directory if not exists
config = configparser.ConfigParser()
config.read("logging.conf", encoding="utf-8")
log_file_path = eval(config["handler_infoHandler"]["args"])[0]
dir = os.path.dirname(log_file_path)
if not os.path.exists(dir):
    os.makedirs(dir)


# create logger
logging.config.fileConfig("logging.conf", encoding="utf-8")
logger = logging.getLogger()
