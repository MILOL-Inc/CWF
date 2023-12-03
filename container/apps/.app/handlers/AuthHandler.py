import tornado, tornado.web
import sys, os
from handlers._path_ import PATH
from handlers._name_ import APP_NAME


# Import public modules:
sys.path.append('{0}'.format(PATH))

# Import Global Configs:
from public import config
from public.library import core

#Initialize variables
USERS = config.users
CYPHER = config.CYPHER
accessLog = config.accessLog

# Import Database API:
import public.db.sqlite as sqlite


class AuthBaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")


class LoginHandler(AuthBaseHandler):
	def get(self):
		params = {
			"errormessage": self.get_argument("error",''),
		}
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [params], f'{APP_NAME}/LoginHandler', 'auth/login.html'))
		self.render("auth/login.html", **params)
	
	def check_permission(self, password, username):
		username = str(username)
		passd_string = str(password)
		password_hash = core.generate_hex_password(passd_string, CYPHER)
		print('user_hash', password_hash)
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.select(conn, 'users', 'email', username)
		sqlite.closeDB(conn)
		for user in users:
			if username == user[2]:
				genmsg = user[4]
				if core.check_rsa_password(username, password_hash, genmsg):
					return True
		return False

	def post(self):
		username = self.get_argument("username", "")
		password = self.get_argument("passd", "")
		auth = self.check_permission(password, username)
		if auth:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, auth], '{APP_NAME}/LoginHandler', 'auth/login.html'))
			self.set_secure_cookie("user", username)
			self.redirect("/auth-index")
		else:
			error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error_msg], '{APP_NAME}/LoginHandler', 'auth/login.html'))
			self.render("auth/login.html", errormessage=error_msg)


class AuthLogoutHandler(AuthBaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect(self.get_argument("next", "/login"))


class IndexHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username], '{APP_NAME}/AuthLogoutHandler', 'auth/logout'))
		self.render("auth/dash.html", username=username)