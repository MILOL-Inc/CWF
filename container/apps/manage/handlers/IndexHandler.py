import tornado.web, sys, os
from handlers._path_ import PATH


# Import Global Configs:
RPATH = os.path.abspath(PATH)
sys.path.append(RPATH)
import public.config as config
from public.library import core

#Initialize variables
accessLog = config.accessLog


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], 'manage/IndexHandler', 'index.html'))
		self.redirect("login")
