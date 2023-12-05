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


class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/AboutHandler', 'about.html'))
		self.render("about.html")