import tornado.web, sys, os
from handlers._path_ import PATH
from handlers._name_ import APP_NAME


# Import Global Configs:
sys.path.append('{0}'.format(PATH))
import public.config as config
from public.library import core

#Initialize variables
accessLog = config.accessLog


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/IndexHandler', 'index.html'))
		self.render("index.html")