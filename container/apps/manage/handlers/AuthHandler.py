import tornado, tornado.web
import sys, os
from handlers._path_ import PATH


# Import Global Configs:
RPATH = os.path.abspath(PATH)
sys.path.append(RPATH)
import public.config as config
from public.library import core

#Initialize variables
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
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [params], 'manage/LoginHandler', 'auth/login.html'))
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
			self.set_secure_cookie("user", username)
			self.redirect("/auth-index")
		else:
			error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error_msg], 'manage/LoginHandler', 'auth/login.html'))
			self.render("auth/login.html", errormessage=error_msg)


class AuthLogoutHandler(AuthBaseHandler):
	def get(self):
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], 'manage/AuthLogoutHandler', 'auth/logout'))
		self.clear_cookie("user")
		self.redirect(self.get_argument("next", "/login"))


class IndexHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		conn = sqlite.openDB('./data/sys.db')
		projects = sqlite.selectAll(conn, 'projects')
		users = sqlite.selectAll(conn, 'users')
		apps = sqlite.selectAll(conn, 'apps')
		routines = sqlite.selectAll(conn, 'routines')
		settings = sqlite.selectAll(conn, 'settings')
		sqlite.closeDB(conn)
		# Strip blob data from users:
		users_ = []
		for i in users:
			users_.append((i[0], i[1], i[2], i[3], i[5]))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [users_], 'manage/IndexHandler', 'auth/dash.html'))
		self.render("auth/dash.html", username=username, projects=projects, users=users_, apps=apps, routines=routines, settings=settings)


class UsersHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		edit_user = self.get_argument('u', default=[], strip=True)
		delete_user = self.get_argument('d', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.selectAll(conn, 'users')
		user_ = []
		admin_role = 0
		deleted = []
		for i in users:
			if username == i[2]:
				admin_role = i[5]
		if delete_user and int(delete_user) != 1 and admin_role == 1:
			deleted = sqlite.delete(conn, 'users', int(delete_user))
		if edit_user:
			edit_user = int(edit_user)
		sqlite.closeDB(conn)
		# Strip blob data from users:
		users_ = []
		for i in users:
			users_.append((i[0], i[1], i[2], i[3], i[5]))
		for i in users_:
			print(i)
			if i[0] == edit_user:
				user_.append(i)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [users_, user_, edit_user, deleted], 'manage/UsersHandler', 'auth/users.html'))
		self.render("auth/users.html", username=username, users=users_, user=user_, edit_user=edit_user, deleted=deleted)


class AddUserHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		created = []
		error = []
		username = tornado.escape.xhtml_escape(self.current_user)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [], 'manage/AddUserHandler', 'auth/user_add.html'))
		self.render("auth/user_add.html", username=username, created=created, error=error)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		user_name = self.get_argument('staticName', default=[], strip=True)
		user_email = self.get_argument('staticEmail', default=[], strip=True)
		user_passd = self.get_argument('inputPassword', default=[], strip=True)
		user_admin_role = self.get_argument('inputAdmin', default=0, strip=True)
		created = []
		error = []
		if user_name and user_email and user_passd:
			created = core.createuser(sqlite, './data/sys.db', CYPHER, user_name, user_email, user_passd, int(user_admin_role))
		if not created:
			error = ['Could not create user. Check logs for more information.']
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error], 'manage/AddUserHandler', ''))
		else:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Create user POST:', [username, created], 'manage/AddUserHandler', ''))
			print('Create user post:', created)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, user_name, created, error], 'manage/AddUserHandler', 'auth/user_add.html'))
		self.render("auth/user_add.html", username=username, user_name=user_name, user_email=user_email, user_passd=user_passd, created=created, error=error)


class UpdateUserHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		edit_user = self.get_argument('u', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.selectAll(conn, 'users')
		user_ = []
		if edit_user:
			edit_user = int(edit_user)
		sqlite.closeDB(conn)
		# Strip blob data from users:
		users_ = []
		for i in users:
			users_.append((i[0], i[1], i[2], i[3], i[5]))
		for i in users_:
			if i[0] == edit_user:
				user_.append(i)
		print('user: ', user_)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, user_, edit_user], 'manage/UpdateUserHandler', 'auth/user_update.html'))
		self.render("auth/user_update.html", username=username, user=user_, edit_user=edit_user)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		user_id = self.get_argument('staticID', default=[], strip=True)
		user_name = self.get_argument('staticName', default=[], strip=True)
		user_email = self.get_argument('staticEmail', default=[], strip=True)
		user_passd = self.get_argument('inputPassword', default=[], strip=True)
		user_admin_role = self.get_argument('inputAdmin', default=0, strip=True)
		print('Post:', user_id, user_name, user_email, user_passd, user_admin_role)
		updated = core.updateuser(sqlite, './data/sys.db', int(user_id), CYPHER, user_name, user_email, user_passd, int(user_admin_role))
		if updated:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, updated], 'manage/UpdateUserHandler', ''))
			print('Updated user post:', updated)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username], 'manage/UpdateUserHandler', 'auth/auth-users'))
		self.redirect("auth-users")


class AppsHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		deleted_app_id = self.get_argument('d', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		apps = sqlite.selectAll(conn, 'apps')
		users = sqlite.selectAll(conn, 'users')
		deleted = []
		app_name = ''
		current_user_id = -1
		app_project_id = -1
		for i in users:
			if username == i[2]:
				current_user_id = int(i[0])
		if deleted_app_id:
			for i in apps:
				if int(deleted_app_id) == i[0]:
					app_project_id = i[4]
					app_name = str(i[1]).replace(' ', '')
		# Delete if the app is not the default app & user is the root user.
		if deleted_app_id and int(deleted_app_id) != 1 and current_user_id == 1:
			deleted = core.deleteFilesApp(app_name)
			if deleted:
				deleted = sqlite.delete(conn, 'apps', int(deleted_app_id))
				accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted app - Admin:', [deleted_app_id], 'manage/AppsHandler', ''))
				print('Deleted app - Admin:', deleted_app_id)
		# Delete if the app is not the default app & user belongs to the project associated with the app.
		elif deleted_app_id and int(deleted_app_id) != 1 and app_project_id == current_user_id:
			deleted = core.deleteFilesApp(app_name)
			if deleted:
				deleted = sqlite.delete(conn, 'apps', int(deleted_app_id))
				accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted app - User:', [deleted_app_id], 'manage/AppsHandler', ''))
				print('Deleted app - User:', deleted_app_id)
		else:
			pass
		if deleted:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted app ID:', [deleted_app_id], 'manage/AppsHandler', ''))
			print('App ID: {0} deleted.'.format(deleted_app_id))
		sqlite.closeDB(conn)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, apps, deleted], 'manage/AppsHandler', 'auth/apps.html'))
		self.render("auth/apps.html", username=username, apps=apps, deleted=deleted)


class AddAppHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		created = []
		error = []
		projects = []
		username = tornado.escape.xhtml_escape(self.current_user)
		conn = sqlite.openDB('./data/sys.db')
		projects_db = sqlite.selectAll(conn, 'projects')
		sqlite.closeDB(conn)
		if projects_db:
			for i in projects_db:
				projects.append((i[0], i[1]))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, created, error], 'manage/AddAppHandler', 'auth/app_add.html'))
		self.render("auth/app_add.html", username=username, created=created, error=error, projects=projects)
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_name = self.get_argument('staticName', default=[], strip=True)
		app_port = self.get_argument('staticPort', default=[], strip=True)
		app_status = self.get_argument('inputStatus', default=0, strip=True)
		app_project_id = self.get_argument('inputProjectID', default=[], strip=True)
		created = []
		error = []
		projects = []
		app_cookie = ''
		conn = sqlite.openDB('./data/sys.db')
		projects = sqlite.selectAll(conn, 'projects')
		settings = sqlite.selectAll(conn, 'settings')
		sqlite.closeDB(conn)
		if settings:
			app_cookie = settings[0][3]
		if app_name and app_port and app_project_id:
			app_name = str(app_name).replace(' ', '')
			created = core.createFilesApp(app_port, app_cookie, app_name)
			print('Creating app post:', app_name, app_port)
			if created:
				created = core.createapp(sqlite, './data/sys.db', str(app_name), int(app_port), int(app_status), int(app_project_id))
				accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Created app POST:', [username, app_name, created], 'manage/AddAppHandler', ''))
				print('Created app post:', created, app_name)
		if not created:
			error = ['Could not create app. Check logs for more information.']
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error], 'manage/AddAppHandler', ''))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, app_name, created, error], 'manage/AddAppHandler', 'auth/app_add.html'))
		self.render("auth/app_add.html", username=username, app_name=app_name, created=created, error=error, projects=projects)


class UpdateAppHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_id = self.get_argument('u', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		apps = sqlite.selectAll(conn, 'apps')
		projects = sqlite.selectAll(conn, 'projects')
		sqlite.closeDB(conn)
		app = []
		if app_id:
			app_id = int(app_id)
		for i in apps:
			if i[0] == app_id:
				app.append(i)
		print('app: ', app)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, app, app_id], 'manage/UpdateAppHandler', 'auth/app_update.html'))
		self.render("auth/app_update.html", username=username, app=app, app_id=app_id, projects=projects)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_id = self.get_argument('staticApp', default=[], strip=True)
		app_port = self.get_argument('staticPort', default=[], strip=True)
		app_status = self.get_argument('inputStatus', default=0, strip=True)
		app_project_id = self.get_argument('inputProjectID', default=[], strip=True)
		print('Updating app post:', app_id, app_port, app_status, app_project_id)
		updated = core.updateapp(sqlite, './data/sys.db', app_id, app_port, app_status, app_project_id)
		if updated:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Updated app POST:', [username, updated], 'manage/UpdateAppHandler', ''))
			print('Updated app post:', updated)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, app_id], 'manage/UpdateAppHandler', 'auth/auth-apps'))
		self.redirect("auth-apps")


class RoutinesHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		deleted_app_id = self.get_argument('d', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		apps = sqlite.selectAll(conn, 'routines')
		users = sqlite.selectAll(conn, 'users')
		deleted = []
		app_name = ''
		current_user_id = -1
		app_project_id = -1
		for i in users:
			if username == i[2]:
				current_user_id = int(i[0])
		if deleted_app_id:
			for i in apps:
				if int(deleted_app_id) == i[0]:
					app_project_id = i[4]
					app_name = str(i[1]).replace(' ', '')
		# Delete if the app is not the default app & user is the root user.
		if deleted_app_id and int(deleted_app_id) != 1 and current_user_id == 1:
			deleted = core.deleteFilesRoutine(app_name)
			if deleted:
				deleted = sqlite.delete(conn, 'routines', int(deleted_app_id))
				accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted routine app - Admin:', [username, deleted, deleted_app_id], 'manage/RoutinesHandler', ''))
				print('Deleted routine app - Admin:', deleted_app_id)
		# Delete if the app is not the default app & user belongs to the project associated with the app.
		elif deleted_app_id and int(deleted_app_id) != 1 and app_project_id == current_user_id:
			deleted = core.deleteFilesRoutine(app_name)
			if deleted:
				deleted = sqlite.delete(conn, 'routines', int(deleted_app_id))
				accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted routine app - User:', [username, deleted, deleted_app_id], 'manage/RoutinesHandler', ''))
				print('Deleted routine app - User:', deleted_app_id)
		else:
			pass
		if deleted:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Routine ID:', [username, deleted, deleted_app_id], 'manage/RoutinesHandler', ''))
			print('Routine ID: {0} deleted.'.format(deleted_app_id))
		sqlite.closeDB(conn)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, apps, deleted], 'manage/RoutinesHandler', 'auth/routines.html'))
		self.render("auth/routines.html", username=username, apps=apps, deleted=deleted)


class AddRoutineHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		created = []
		error = []
		projects = []
		username = tornado.escape.xhtml_escape(self.current_user)
		conn = sqlite.openDB('./data/sys.db')
		projects_db = sqlite.selectAll(conn, 'projects')
		sqlite.closeDB(conn)
		if projects_db:
			for i in projects_db:
				projects.append((i[0], i[1]))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, created, error], 'manage/AddRoutineHandler', 'auth/routine_add.html'))
		self.render("auth/routine_add.html", username=username, created=created, error=error, projects=projects)

	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_name = self.get_argument('staticName', default=[], strip=True)
		app_port = self.get_argument('staticPort', default=[], strip=True)
		app_status = self.get_argument('inputStatus', default=0, strip=True)
		app_project_id = self.get_argument('inputProjectID', default=[], strip=True)
		created = []
		error = []
		projects = []
		app_cookie = ''
		conn = sqlite.openDB('./data/sys.db')
		projects = sqlite.selectAll(conn, 'projects')
		settings = sqlite.selectAll(conn, 'settings')
		sqlite.closeDB(conn)
		if settings:
			app_cookie = settings[0][3]
		if app_name and app_port and app_project_id:
			app_name = str(app_name).replace(' ', '')
			created = core.createFilesRoutine(app_port, app_cookie, app_name)
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username], 'manage/AddRoutineHandler', ''))
			print('Creating app post:', app_name, app_port)
			if created:
				created = core.createroutine(sqlite, './data/sys.db', str(app_name), int(app_port), int(app_status), int(app_project_id))
				print('Created routine app post:', created, app_name)
		if not created:
			error = ['Could not create routine app. Check logs for more information.']
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error], 'manage/AddRoutineHandler', ''))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, app_name, created, error], 'manage/AddRoutineHandler', 'auth/routine_add.html'))
		self.render("auth/routine_add.html", username=username, app_name=app_name, created=created, error=error, projects=projects)


class UpdateRoutineHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_id = self.get_argument('u', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		apps = sqlite.selectAll(conn, 'apps')
		projects = sqlite.selectAll(conn, 'projects')
		sqlite.closeDB(conn)
		app = []
		if app_id:
			app_id = int(app_id)
		for i in apps:
			if i[0] == app_id:
				app.append(i)
		print('app: ', app)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, app, app_id], 'manage/UpdateRoutineHandler', 'auth/routine_update.html'))
		self.render("auth/routine_update.html", username=username, app=app, app_id=app_id, projects=projects)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		app_id = self.get_argument('staticApp', default=[], strip=True)
		app_port = self.get_argument('staticPort', default=[], strip=True)
		app_status = self.get_argument('inputStatus', default=0, strip=True)
		app_project_id = self.get_argument('inputProjectID', default=[], strip=True)
		print('Updating app post:', app_id, app_port, app_status, app_project_id)
		updated = core.updateroutine(sqlite, './data/sys.db', app_id, app_port, app_status, app_project_id)
		if updated:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Updated app POST:', [username, updated, app_id], 'manage/UpdateRoutineHandler', ''))
			print('Updated app post:', updated)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, updated], 'manage/UpdateRoutineHandler', 'auth/auth-routines'))
		self.redirect("auth-routines")


class ProjectsHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		deleted_project_id = self.get_argument('d', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		projects = sqlite.selectAll(conn, 'projects')
		users = sqlite.selectAll(conn, 'users')
		deleted = []
		current_user_id = -1
		for i in users:
			if username == i[2]:
				current_user_id = i[0]
		# Delete if the project_id is not the default project & project_id being deleted belongs to current user.
		if deleted_project_id and deleted_project_id != 1:
			if int(deleted_project_id) == int(current_user_id) or int(current_user_id) == 1:
				deleted = sqlite.delete(conn, 'projects', int(deleted_project_id))
		if deleted:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Updated app POST:', [username, deleted, deleted_project_id], 'manage/ProjectsHandler', ''))
			print('Project ID: {0} deleted.'.format(deleted_project_id))
		sqlite.closeDB(conn)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, projects, deleted], 'manage/ProjectsHandler', 'auth/projects.html'))
		self.render("auth/projects.html", username=username, projects=projects, deleted=deleted)


class AddProjectHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		created = []
		error = []
		username = tornado.escape.xhtml_escape(self.current_user)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, created, error], 'manage/AddProjectHandler', 'auth/project_add.html'))
		self.render("auth/project_add.html", username=username, created=created, error=error)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		project_name = self.get_argument('staticName', default=[], strip=True)
		created = []
		error = []
		current_user_id = -1
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.selectAll(conn, 'users')
		for i in users:
			if username == i[2]:
				current_user_id = i[0]
		if project_name and current_user_id != -1:
			created = core.createproject(sqlite, './data/sys.db', str(project_name), int(current_user_id))
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, project_name], 'manage/AddProjectHandler', ''))
		if not created:
			error = ['Could not create project. Check logs for more information.']
			accessLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'POST', [username, error], 'manage/AddProjectHandler', ''))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, created, error], 'manage/AddProjectHandler', 'auth/project_add.html'))
		self.render("auth/project_add.html", username=username, project_name=project_name, created=created, error=error)


class SettingsHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		edit_setting = self.get_argument('u', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.selectAll(conn, 'users')
		settings = sqlite.selectAll(conn, 'settings')
		sqlite.closeDB(conn)
		settings_ = []
		# Strip sensitive data from settings:
		for i in settings:
			settings_.append((i[0], i[1], i[4], i[5], i[6]))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, settings_], 'manage/SettingsHandler', 'auth/settings.html'))
		self.render("auth/settings.html", username=username, settings=settings_)


class UpdateSettingHandler(AuthBaseHandler):
	@tornado.web.authenticated
	def get(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		setting_id = self.get_argument('u', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		settings = sqlite.selectAll(conn, 'settings')
		users = sqlite.selectAll(conn, 'users')
		sqlite.closeDB(conn)
		settings_ = []
		admin_role = 0
		# Query if the user has admin role:
		for i in users:
			if username == i[2]:
				admin_role = i[5]
		if setting_id:
			setting_id = int(setting_id)
		# Strip sensitive data from settings:
		for i in settings:
			settings_.append((i[0], i[1], i[4], i[5], i[6]))
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'GET', [username, settings_], 'manage/UpdateSettingHandler', 'auth/setting_update.html'))
		self.render("auth/setting_update.html", username=username, settings=settings_, admin_role=admin_role)
	
	def post(self):
		username = tornado.escape.xhtml_escape(self.current_user)
		setting_id = self.get_argument('staticSettingID', default=[], strip=True)
		setting_exec = self.get_argument('staticExec', default=[], strip=True)
		setting_path = self.get_argument('staticPath', default=[], strip=True)
		setting_port = self.get_argument('staticPort', default=[], strip=True)
		conn = sqlite.openDB('./data/sys.db')
		users = sqlite.selectAll(conn, 'users')
		sqlite.closeDB(conn)
		admin_role = []
		updated = []
		# Query if the user has admin role:
		for i in users:
			if username == i[2]:
				admin_role = i[5]
		if setting_id and setting_exec and setting_path and setting_port and int(admin_role) == 1:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Updating setting POST:', [username, setting_id, setting_exec, setting_path, setting_port], 'manage/UpdateSettingHandler', ''))
			print('Updating setting post:', setting_id, setting_exec, setting_path, setting_port)
			updated = core.updatesetting(sqlite, './data/sys.db', int(setting_id), setting_exec, setting_path, int(setting_port))
		if updated:
			accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Settings updated POST:', [username, updated, setting_id], 'manage/UpdateSettingHandler', ''))
			print('Settings updated:', updated)
		accessLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'POST', [username, updated, setting_id], 'manage/UpdateSettingHandler', 'auth/auth-settings'))
		self.redirect("auth-settings")