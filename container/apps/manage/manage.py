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
import public.config as config
import public.library.core as core

#Get application arguments
arg = sys.argv

#Initialize variables
DEVELOPMENT_ENV = config.DEVELOPMENT_ENV
accessLog = config.accessLog

settings = {
    "template_path": os.path.join(PATH, "apps/{0}/templates".format(APP_NAME)),
    "static_path": os.path.join(PATH, "apps/{0}/static".format(APP_NAME)),
	"gzip": True,
	"cookie_secret": COOKIE_SECRET,
	"login_url": "/login",
	"default_handler_class": handlers.DefaultHandler.DefaultHandler,
    "debug" : DEVELOPMENT_ENV
}

application = tornado.web.Application([
	(r'/',  handlers.IndexHandler.IndexHandler),
	(r'/terms',  handlers.TermsHandler.TermsHandler),
	(r"/login", handlers.AuthHandler.LoginHandler),
	(r"/logout", handlers.AuthHandler.AuthLogoutHandler),
	(r"/auth-index", handlers.AuthHandler.IndexHandler),
	(r"/auth-users", handlers.AuthHandler.UsersHandler),
	(r"/auth-adduser", handlers.AuthHandler.AddUserHandler),
	(r"/auth-updateuser", handlers.AuthHandler.UpdateUserHandler),
	(r"/auth-apps", handlers.AuthHandler.AppsHandler),
	(r"/auth-addapp", handlers.AuthHandler.AddAppHandler),
	(r"/auth-updateapp", handlers.AuthHandler.UpdateAppHandler),
	(r"/auth-routines", handlers.AuthHandler.RoutinesHandler),
	(r"/auth-addroutine", handlers.AuthHandler.AddRoutineHandler),
	(r"/auth-updateroutine", handlers.AuthHandler.UpdateRoutineHandler),
	(r"/auth-projects", handlers.AuthHandler.ProjectsHandler),
	(r"/auth-addproject", handlers.AuthHandler.AddProjectHandler),
	(r"/auth-settings", handlers.AuthHandler.SettingsHandler),
	(r"/auth-updatesetting", handlers.AuthHandler.UpdateSettingHandler),
],**settings)

if __name__ == "__main__":
	try:
		port = int(arg[1])
		application.listen(port)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'App server running port:', [APP_NAME, port], 'manage_main_', ''))
		print('{0} running port: {1}'.format(APP_NAME, port))
	except:
		application.listen(PORT)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'App server running port:', [APP_NAME, PORT], 'manage_main_', ''))
		print('{0} running port: {1}'.format(APP_NAME, PORT))
	tornado.ioloop.IOLoop.instance().start()