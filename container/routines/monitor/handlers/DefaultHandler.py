from handlers import _name_
from handlers import _path_
from handlers import _config_
import sys, os
import time


# Import Global Configs:
APP_NAME = _name_.APP_NAME
PORT = _config_.PORT
PATH = _path_.PATH
RPATH = os.path.abspath(PATH)
sys.path.append('{0}'.format(PATH))
import public.config as config
import public.library.core as core

#Initialize variables
accessLog = config.accessLog


def RunRoutine():
    accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'', [], '{APP_NAME}/RunRoutine', 'RunRoutine'))
    while 1:
        print('Running routine...')
        time.sleep(60)
        