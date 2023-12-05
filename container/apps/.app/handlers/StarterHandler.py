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


class StarterHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/StarterHandler', 'starter.html'))
		self.render("starter.html")


class FeaturesHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/FeaturesHandler', 'features.html'))
		self.render("features.html")


class BlogHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], f'{APP_NAME}/BlogHandler', 'blog.html'))
		self.render("blog.html")