from configparser import ConfigParser
import logging


def get_logger(name):
    ini_config = ConfigParser()
    ini_config.read("proxy_list.cfg")
    conf_log_level = ini_config.get("Config", "log_level")
    log_level = get_log_level(conf_log_level)
    logging.basicConfig(level=log_level)
    return logging.getLogger(name)


def get_log_level(level_from_config):
    if level_from_config == "debug":
        return logging.DEBUG
    elif level_from_config == "info":
        return logging.INFO
    else:
        raise "Not Implemented"
