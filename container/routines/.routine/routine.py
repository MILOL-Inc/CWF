from handlers import _name_
from handlers import _path_
from handlers import _config_
from handlers import DefaultHandler
import sys, os


# Import Global Configs:
APP_NAME = _name_.APP_NAME
PORT = _config_.PORT
PATH = _path_.PATH
import public.config as config
import public.library.core as core

#Get application arguments
arg = sys.argv

#Initialize variables
accessLog = config.accessLog


if __name__ == "__main__":
	accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'', [], '{APP_NAME}/__main__', '__main__'))
	DefaultHandler.RunRoutine()