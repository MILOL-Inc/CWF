from handlers import _name_
from handlers import _path_
from handlers import _config_

#App Name: Name must match directory.
APP_NAME = _name_.APP_NAME
PORT = _config_.PORT
PATH = _path_.PATH
COOKIE_SECRET = _config_.COOKIE_SECRET

import os, sys, tornado.web, tornado.ioloop
import handlers


settings = {
    "template_path": os.path.join(PATH, "apps/{0}/templates".format(APP_NAME)),
    "static_path": os.path.join(PATH, "apps/{0}/static".format(APP_NAME)),
	"gzip": True,
	"cookie_secret": COOKIE_SECRET,
	"login_url": "/login",
	"default_handler_class": handlers.DefaultHandler.DefaultHandler,
    "debug" : True
}

application = tornado.web.Application([
	(r'/',  handlers.IndexHandler.IndexHandler),
	(r'/about',  handlers.AboutHandler.AboutHandler),
	(r'/terms',  handlers.TermsHandler.TermsHandler),
	(r"/login", handlers.AuthHandler.LoginHandler),
	(r"/logout", handlers.AuthHandler.AuthLogoutHandler),
	(r"/auth-index", handlers.AuthHandler.IndexHandler),
	(r'/starter',  handlers.StarterHandler.StarterHandler),
	(r'/features',  handlers.StarterHandler.FeaturesHandler),
	(r'/blog',  handlers.StarterHandler.BlogHandler),
],**settings)

if __name__ == "__main__":
	application.listen(PORT)
	tornado.ioloop.IOLoop.instance().start()