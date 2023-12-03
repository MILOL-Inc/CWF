import tornado.web

class TermsHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("terms.html")