import tornado.web, sys, os
from handlers._path_ import PATH


# Import Global Configs:
sys.path.append('{0}'.format(PATH))
import public.config as config
from public.library import core

#Initialize variables
accessLog = config.accessLog


class DefaultHandler(tornado.web.RequestHandler):
	def prepare(self):
		# Use prepare() to handle all the HTTP methods
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [404], 'manage/DefaultHandler', '404.html'))
		self.set_status(404)
		self.render("404.html")