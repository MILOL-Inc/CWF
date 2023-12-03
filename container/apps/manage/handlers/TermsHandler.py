import tornado.web, sys, os
from handlers._path_ import PATH


# Import Global Configs:
sys.path.append('{0}'.format(PATH))
import public.config as config
from public.library import core

#Initialize variables
accessLog = config.accessLog


class TermsHandler(tornado.web.RequestHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], 'manage/TermsHandler', 'terms.html'))
		self.render("terms.html")