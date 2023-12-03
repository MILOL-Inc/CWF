import tornado, tornado.web
import sys, os
import hashlib
import rsa


# Import public modules:
PARENT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PARENT_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
PARENT_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
sys.path.append('{0}/public'.format(PARENT_ROOT))
###

# Import Global Configs:
import config
from library import core
USERS = config.users
CYPHER = config.CYPHER

class AuthBaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")


class LoginHandler(AuthBaseHandler):
	def get(self):
		#db2 = sqlite.createDB('dbfile')
		params = {
			"errormessage": self.get_argument("error",''),
		}
		self.render("auth/login.html", **params)

	def check_permission(self, password, username):
		pass_ = password+CYPHER
		password_hash = core.hash_sha1_hex(pass_.encode('utf8'))
		for user in USERS:
			if username == USERS[user]['email'] and password_hash == USERS[user]['passd']:
			#if username == 'ad@mail.com' and password == 'MILOL':
				return True
		return False

	def post(self):
		username = self.get_argument("username", "")
		password = self.get_argument("passd", "")
		auth = self.check_permission(password, username)
		if auth:
			self.set_secure_cookie("user", username)
			self.redirect("/auth-index")
		else:
			error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
			self.render("auth/login.html", errormessage=error_msg)


class AuthLogoutHandler(AuthBaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/login"))


class IndexHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		self.render("auth/dash.html", username=username)
