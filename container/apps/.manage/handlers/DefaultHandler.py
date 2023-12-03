import tornado.web

class DefaultHandler(tornado.web.RequestHandler):
    def prepare(self):
        # Use prepare() to handle all the HTTP methods
        self.set_status(404)
        self.render("404.html")