import sqlite3, os, sys
from sqlite3 import Error
import public.library.core as core
import public.config as config


# Global Settings:
VERSION = config.VERSION
EXEC = config.EXEC
DPORT = config.DEFAULT_PORT
PASSD_STRING = config.PASS
severLog = config.severLog

if not os.path.exists(f"{config.WEBPATH}/data/sys.db"):
	COOKIE_SECRET = ''
	CYPHER = ''
	print('Database does NOT exists.')
else:
	COOKIE_SECRET = config.COOKIE_SECRET
	CYPHER = config.CYPHER


def openDB(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'', [], 'openDB', ''))
		print('ERROR')
		pass

	return conn


def createDoc(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'', [], 'createDoc', ''))
		print('ERROR', 'createDoc')


def gendb(path=os.getcwd()):
	""" Generare init database schema. """
	path = path
	path = ''.join(str(path).split())
	database_name = r"{0}/data/sys.db".format(path)
	if not os.path.exists(database_name):
		try:
			# Create or connect to the database file
			# conn = sqlite3.connect(database_name)
			conn = openDB(database_name)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Create the 'users' table
			sql_create_users_table = '''CREATE TABLE IF NOT EXISTS users (
							_id INTEGER PRIMARY KEY,
							name TEXT NOT NULL,
							email TEXT UNIQUE,
							passd TEXT,
							passb BLOB,
							admin INTEGER DEFAULT 0
							);'''
			createDoc(conn, sql_create_users_table)

			# Create the 'projects' table
			sql_create_projects_table = '''CREATE TABLE IF NOT EXISTS projects (
												_id integer PRIMARY KEY,
												name text NOT NULL,
												user_id INTEGER NOT NULL,
												FOREIGN KEY (user_id) REFERENCES users (_id)
											);'''
			createDoc(conn, sql_create_projects_table)

			# Create the 'routines' table
			sql_create_routines_table = '''CREATE TABLE IF NOT EXISTS routines (
							_id INTEGER PRIMARY KEY,
							name TEXT UNIQUE,
							port INTEGER,
							status INTEGER DEFAULT 1,
							project_id INTEGER NOT NULL,
							FOREIGN KEY (project_id) REFERENCES projects (_id)
							);'''
			createDoc(conn, sql_create_routines_table)

			# Create the 'apps' table
			sql_create_apps_table = '''CREATE TABLE IF NOT EXISTS apps (
							_id INTEGER PRIMARY KEY,
							name TEXT UNIQUE,
							port INTEGER NOT NULL,
							status INTEGER DEFAULT 1,
							project_id INTEGER NOT NULL,
							FOREIGN KEY (project_id) REFERENCES projects (_id)
							);'''
			createDoc(conn, sql_create_apps_table)

			# Create the 'settings' table
			sql_create_settings_table = '''CREATE TABLE IF NOT EXISTS settings (
							_id INTEGER PRIMARY KEY,
							version TEXT,
							cypher TEXT,
							csecret TEXT,
							exec TEXT,
							webpath TEXT,
							dport TEXT
							);'''
			createDoc(conn, sql_create_settings_table)

			# Commit the changes and close the connection
			conn.commit()
			conn.close()

			severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Database created successfully.', [database_name], 'gendb', ''))
			print(f"Database '{database_name}' created successfully.")
		except sqlite3.Error as e:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'SQLite error:', [e], 'gendb', ''))
			print(f"SQLite error: {e}")
	else:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'WARN', f'Database already exists.', [database_name], 'gendb', ''))
		print(f"Database '{database_name}' already exists.")


def geninitfiles(path=os.getcwd(), PASSD_STRING=PASSD_STRING, COOKIE_SECRET=COOKIE_SECRET, CYPHER=CYPHER, reset=[]):
	""" Create init files into public directory. """
	path = path
	path = ''.join(str(path).split())
	PASSD_STRING = PASSD_STRING
	COOKIE_SECRET = COOKIE_SECRET
	CYPHER = CYPHER
	pass_file = '_pass_.py'
	csecret_file = '_csecret_.py'
	cypher_file = '_cypher_.py'
	dport_file = '_dport_.py'
	exec_file = '_exec_.py'
	path_file = '_path_.py'
	version_file = '_version_.py'
	passd_file = '_passd_.py'
	generated_user_passd = '''{0}'''.format(core.generate_hex_password(PASSD_STRING, CYPHER))
	try:
		if os.path.exists(f"{path}/public/{pass_file}"):
			with open("{0}/public/{1}".format(path, pass_file), 'w') as f:
				f.write("PASS = '{0}'".format(PASSD_STRING))
		else:
			print('File pass DOES NOT exists.')
		with open("{0}/public/{1}".format(path, csecret_file), 'w') as f:
			f.write("COOKIE_SECRET = '{0}'".format(COOKIE_SECRET))
		with open("{0}/public/{1}".format(path, cypher_file), 'w') as f:
			f.write("CYPHER = '{0}'".format(CYPHER))
		with open("{0}/public/{1}".format(path, dport_file), 'w') as f:
			f.write("DEFAULT_PORT = '{0}'".format(DPORT))
		with open("{0}/public/{1}".format(path, exec_file), 'w') as f:
			f.write("EXEC = '{0}'".format(EXEC))
		with open("{0}/public/{1}".format(path, path_file), 'w') as f:
			f.write("PATH = '{0}'".format(path))
		with open("{0}/public/{1}".format(path, version_file), 'w') as f:
			f.write("VERSION = '{0}'".format(VERSION))
		with open("{0}/public/{1}".format(path, passd_file), 'w') as f:
			f.write("""PASSD = '{0}'""".format(generated_user_passd))
	except FileNotFoundError:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected Fuction Error:', [sys.exc_info()[0]], 'geninitfiles', ''))
		print("Unexpected geninitfiles Fuction Error:", sys.exc_info()[0])
	severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Init files created.', [VERSION], 'geninitfiles', ''))
	if not reset:
		print('Version {0} init files created.'.format(VERSION))
		print('Password:', PASSD_STRING)
	else:
		print('Version {0} init files re-created.'.format(VERSION))


def gencredentials(path=os.getcwd(), PASSD_STRING=PASSD_STRING, COOKIE_SECRET=COOKIE_SECRET, CYPHER=CYPHER):
	""" Generate init system credentials. """
	path = path
	path = ''.join(str(path).split())
	PASSD_STRING = PASSD_STRING
	COOKIE_SECRET = COOKIE_SECRET
	CYPHER = CYPHER
	database_name = r"{0}/data/sys.db".format(path)
	generated_user_passd = '''{0}'''.format(core.generate_hex_password(PASSD_STRING, CYPHER))
	generated_user_passb = core.generate_rsa_password(PASSD_STRING, CYPHER)
	if os.path.exists(database_name):
		try:
			# Create or connect to the database file
			# conn = sqlite3.connect(database_name)
			conn = openDB(database_name)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'settings' table
			cursor.execute('''INSERT INTO settings (version, cypher, csecret, exec, webpath, dport)
								VALUES (?, ?, ?, ?, ?, ?)''',
							(VERSION, CYPHER, COOKIE_SECRET, EXEC, path, DPORT))
			
			# Insert default values into the 'users' table
			cursor.execute('''INSERT INTO users (name, email, passd, passb, admin)
								VALUES (?, ?, ?, ?, ?)''',
							('Admin', 'ad@cwf.local', generated_user_passd, generated_user_passb, 1))

			# Insert default values into the 'projects' table
			cursor.execute('''INSERT INTO projects (name, user_id)
								VALUES (?, ?)''',
							('manage', 1))

			# Insert default values into the 'apps' table
			cursor.execute('''INSERT INTO apps (name, port, status, project_id)
								VALUES (?, ?, ?, ?)''',
							('manage', DPORT, 1, 1))

			# Commit the changes and close the connection
			conn.commit()
			conn.close()

			severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Database Credentials created successfully:', [database_name], 'gencredentials', ''))
			print(f"Database Credentials created successfully.")
		except sqlite3.Error as e:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'SQLite Error:', [e], 'gencredentials', ''))
			print(f"SQLite error: {e}")
	else:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_name], 'gencredentials', ''))
		print(f"Database '{database_name}' does NOT exists.")
	pass


def createuser(name, email, passd_string, admin_role):
	""" Create a new user. """
	CYPHER = core.generate_passphrase(16)
	res = []
	path = os.getcwd()
	name = str(name)
	email = str(email)
	passd_string = str(passd_string)
	admin_role = int(admin_role)
	database_name = r"{0}/data/sys.db".format(path)
	generated_user_passd = '''{0}'''.format(core.generate_hex_password(passd_string, CYPHER))
	generated_user_passb = core.generate_rsa_password(passd_string, CYPHER)
	if os.path.exists(database_name):
		try:
			# Create or connect to the database file
			# conn = sqlite3.connect(database_name)
			conn = openDB(database_name)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'users' table
			cursor.execute('''INSERT INTO users (name, email, passd, passb, admin)
								VALUES (?, ?, ?, ?, ?)''',
							(name, email, generated_user_passd, generated_user_passb, admin_role))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes and close the connection
			conn.commit()
			conn.close()

			print(f"New user on '{database_name}' created successfully.")
		except sqlite3.Error as e:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'SQLite Error:', [e], 'createuser', ''))
			print(f"SQLite error: {e}")
	else:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_name], 'createuser', ''))
		print(f"Database '{database_name}' does NOT exists. createuser()")
	pass
	return res


def checkdbfile(path=os.getcwd()):
	""" Check if sys.db already exist.
	Return True - If database exists.
	Return False - If database does NOT exists.
	"""
	path = path
	path = ''.join(str(path).split())
	database_name = r"{0}/data/sys.db".format(path)
	res = []
	if not os.path.exists(database_name):
		res = False
		severLog.error(config.jsonLogger(core.getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_name], 'checkdbfile', ''))
		print(f"Initial database '{database_name}' NOT created yet.\n")
	else:
		res = True
		severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Database exist.', [database_name, res], 'checkdbfile', ''))
		print(f"Database '{database_name}' already exists.\n")
	return res


def resetdbfiles(path):
	path = path
	path = ''.join(str(path).split())
	path = r"{0}".format(path)
	print('Reseting database...')
	try:
		os.remove(f"{path}/data/sys.db")
		severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleted {path}/data/sys.db', [], 'resetfiles', ''))
	except:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Could not delete file: {path}/data/sys.db', [], 'resetfiles', ''))


def main(path=os.getcwd()):
	path = path
	path = ''.join(str(path).split())
	path = r"{0}".format(path)
	PASSD_STRING = core.generate_passphrase()
	CYPHER = core.generate_passphrase(16)
	COOKIE_SECRET = core.generate_passphrase(32)
	if not checkdbfile():
		# Generate cryptografic key pairs:
		core.generate_secret(4096, path)
		# Generate init files:
		geninitfiles(path, PASSD_STRING, COOKIE_SECRET, CYPHER)
		# Generare init database schema:
		gendb(path)
		# Generate init admin credetials:
		gencredentials(path, PASSD_STRING, COOKIE_SECRET, CYPHER)
	else:
		print(f"Skiping... System database already exists.\nTo re-initialize system, delete data/sys.db and run runsever --gendb.\n")


if __name__ == '__main__':
	main()