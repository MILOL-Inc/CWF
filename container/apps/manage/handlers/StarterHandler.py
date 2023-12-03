import tornado.web


class StarterHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("starter.html")
