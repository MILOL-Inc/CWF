import tornado.web, sys, os
from handlers._path_ import PATH
from handlers._name_ import APP_NAME


# Import Global Configs:
RPATH = os.path.abspath(PATH)
sys.path.append(RPATH)
import public.config as config
from public.library import core

#Initialize variables
accessLog = config.accessLog


class DefaultHandler(tornado.web.RequestHandler):
	def prepare(self):
		# Use prepare() to handle all the HTTP methods
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/DefaultHandler', '404.html'))
		self.set_status(404)
		self.render("404.html")