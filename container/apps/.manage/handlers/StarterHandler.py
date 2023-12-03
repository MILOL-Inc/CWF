import tornado.web


class StarterHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("starter.html")


class FeaturesHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("features.html")


class BlogHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("blog.html")