import os, sys, shutil, random
import public.config as config
import public.library.core as core
import initdb as initdb

PATH = config.WEBPATH
VERSION = config.VERSION
APP_LIST = config.apps
ROUTINE_LIST = config.routines
EXEC = config.EXEC
PORT = config.DEFAULT_PORT

#Initializing Global Logs Objects:
severLog = config.severLog

#Get application arguments
arg = sys.argv

# Import Database API:
import public.db.sqlite as sqlite


def getSystemSettings(db_table='settings'):
	# 'settings': {'_id': 1, 'version': '0.14', 'cypher': '***', 'csecret': '***', 'exec': 'python', 'webpath': '/path' 'port': 8090}
	sql = sqlite
	db_table = str(db_table)
	SETTINGS_LIST = [(1, VERSION, '', '', EXEC, PATH, PORT)]
	print('Config Settings:', SETTINGS_LIST)
	json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Config Settings: {db_table}', [SETTINGS_LIST], 'getSystemSettings', '')
	severLog.info(json_msg)
	print(json_msg)
	data = core.getdbtable(sql, './data/sys.db', db_table)
	if data:
		print('DB Settings:', data)
		return data
	return SETTINGS_LIST


def getTableDB(db_table=''):
	# Query table from database.
	sql = sqlite
	table = str(db_table).replace(' ', '')
	db_table = str(table)
	data = []
	data = core.getdbtable(sql, './data/sys.db', db_table)
	if data:
		json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'DB table query: {db_table}', [data], 'getTableDB', '')
		severLog.info(json_msg)
		print(data)
		return data

	json_msg = config.jsonLogger(core.getUTCNow(), 'WARNING', f'Empty DB table query: {db_table}', [data], 'getTableDB', '')
	severLog.info(json_msg)
	return data


def getAppList():
	# 'name': {'name': 'NAME_APP', 'port': 8090, 'status': 1}
	sql = sqlite
	table = 'apps'
	db_table = str(table)
	APP_LIST = config.apps
	data = core.getdbtable(sql, './data/sys.db', db_table)
	if data:
		json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'DB table query: {db_table}', [data], 'getAppList', '')
		severLog.info(json_msg)
		print(data)
		return data
	json_msg = config.jsonLogger(core.getUTCNow(), 'WARNING', f'Config file apps: {db_table}', [APP_LIST], 'getAppList', '')
	severLog.info(json_msg)
	print(APP_LIST)
	return APP_LIST


def getRoutineList():
	# 'name': {'name': 'NAME_ROUTINE', 'port': 9090, 'status': 1}
	sql = sqlite
	table = 'routines'
	db_table = str(table)
	ROUTINE_LIST = config.routines
	data = core.getdbtable(sql, './data/sys.db', db_table)
	if data:
		json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'DB table query: {db_table}', [data], 'getRoutineList', '')
		severLog.info(json_msg)
		print(data)
		return data
	json_msg = config.jsonLogger(core.getUTCNow(), 'WARNING', f'Config file apps: {db_table}', [ROUTINE_LIST], 'getRoutineList', '')
	severLog.info(json_msg)
	print(ROUTINE_LIST)
	return ROUTINE_LIST


def runRoutines():
	""" Run all enabled routines applications
		To test apps in the terminal use:
		pid = core.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app[1], EXEC)) """
	print(VERSION)
	res = True
	APP_LIST = getRoutineList('routines')
	try:
		for app in APP_LIST:
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running routine.', [app], 'runRoutines', '')
			severLog.info(json_msg)
			print('runRoutines', app)
			if app[3] == 1:
				pid = core.runSP('{2} {0}/apps/{1}/{1}.py {3}'.format(PATH, app[1], EXEC, app[2]))
				json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running routine pid: {pid}', [app], 'runRoutines', '')
				severLog.info(json_msg)
				print(app[0], 'running on port:', app[2], 'pid:', pid)
	except:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected runRoutines Fuction Error: {sys.exc_info()[0]}', [app], 'runRoutines', '')
		severLog.error(json_msg)
		print("Unexpected runRoutines Fuction Error:", sys.exc_info()[0])
		res = False
		pass
	return True


def runApps():
	""" Run all enabled user apps.
	To test apps in the terminal use:
	pid = core.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app[1], EXEC)) """
	print(VERSION)
	res = True
	APP_LIST = getAppList()
	try:
		for app in APP_LIST:
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running app.', [app], 'runApps', '')
			severLog.info(json_msg)
			print('runApps', app)
			if app[3] == 1:
				print(app)
				cmd = '{2} {0}/apps/{1}/{1}.py {3}'.format(PATH, app[1], EXEC, app[2])
				print(cmd)
				pid = core.runSP(cmd)
				json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running app pid: {pid}', [app], 'runApps', '')
				severLog.info(json_msg)
				print(app[0], 'running on port:', app[2], 'pid:', pid)
				print(f"http://localhost:{app[2]}")
	except:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected runRoutines Fuction Error: {sys.exc_info()[0]}', [app], 'runApps', '')
		severLog.error(json_msg)
		print("Unexpected runApps Fuction Error:", sys.exc_info()[0])
		res = False
		pass
	return True


def runApp():
	""" Run apps in the foreground.
	To test apps on the terminal use:
	pid = core.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app[1], EXEC)) """
	print(VERSION)
	settings = getSystemSettings()
	EXEC = settings[0][4]
	PATH = settings[0][5]
	res = True
	APP_LIST = getAppList()
	app_name = str(arg[2]).replace(' ', '')
	try:
		for app in APP_LIST:
			if app[1] == app_name:
				json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running app.', [app], 'runApp', '')
				severLog.info(json_msg)
				print('runApps', app)
				pid = core.runOS('{2} {0}/apps/{1}/{1}.py {3}'.format(PATH, app[1], EXEC, app[2]))
				json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running app pid: {pid}', [app], 'runApp', '')
				severLog.info(json_msg)
				print(app[0], 'running on port:', app[2], 'pid:', pid)
				print(f"http://localhost:{app[2]}")
	except:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected runRoutines Fuction Error: {sys.exc_info()[0]}', [app], 'runApp', '')
		severLog.error(json_msg)
		print("Unexpected testApp Fuction Error:", sys.exc_info()[0])
		res = False
		pass
	return True


def createApp():
	""" Create UI application function. """
	appName = 'app_{0}'.format(random.randint(0, 99))
	port = '8080'
	status = 1
	project_id = 1
	try:
		sql = sqlite
		appName = str(arg[2]).replace(' ', '')
		port = int(arg[3])
		status = int(arg[4])
		project_id = int(arg[5])
	except:
		pass

	# Query the database to delete the app record
	app_id = core.createapp(sql, './data/sys.db', appName, port, status, project_id)
	json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Generating app id: {app_id}', [appName, port, status, project_id], 'createApp', '')
	severLog.info(json_msg)
	print('Generating app:', app_id)

	path = os.getcwd()
	source_folder = r"{0}/apps/.app".format(path)
	destination_folder = r"{0}/apps/{1}".format(path, appName)
	if not os.path.exists(destination_folder):
		try:
			shutil.copytree(source_folder, destination_folder)
			with open("{0}/apps/{1}/handlers/_name_.py".format(path, appName), 'w') as f:
				f.write("APP_NAME = '{0}'".format(appName))
			os.rename("{0}/apps/{1}/app.py".format(path, appName), "{0}/apps/{1}/{1}.py".format(path, appName))
			with open("{0}/apps/{1}/handlers/_path_.py".format(path, appName), 'w') as f:
				f.write("PATH = '{0}'".format(path))
			with open("{0}/apps/{1}/handlers/_config_.py".format(path, appName), 'w') as f:
				f.write("PORT = '{0}'".format(port))
				f.write("\n")
				f.write("COOKIE_SECRET = '{0}'".format(config.COOKIE_SECRET))
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Created app: {appName}', [appName, port, status, project_id], 'createApp', '')
			severLog.info(json_msg)
			print('{0} application created.'.format(appName))
		except FileNotFoundError:
			json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected Fuction Error: {sys.exc_info()[0]}', [appName, port, status, project_id], 'createApp', '')
			severLog.error(json_msg)
			print("Unexpected createapp Fuction Error:", sys.exc_info()[0])
	else:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Application files already exist: {appName}', [appName, port, status, project_id], 'createApp', '')
		severLog.error(json_msg)
		print('{0} application files already exist. createApp()'.format(appName))


def deleteApp():
	try:
		sql = sqlite
		app_name = str(arg[2]).replace(' ', '')
		sys_app_name = 'manage'
		
		# Query the database to delete the app record
		if not sys_app_name == app_name:
			app_id = core.deleteapp(app_name, sql, './data/sys.db')
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleting app: {app_id}', [app_id, app_name], 'deleteApp', '')
			severLog.info(json_msg)
			print('Deleting app:', app_id)

			if app_id[0] > 0:
				# Delete the app files from the "apps/" directory
				path = os.getcwd()
				app_directory = r"{0}/apps/{1}".format(path, app_name)
				if os.path.exists(app_directory):
					core.delete_directory(app_directory)

			return app_id  # Return the deleted app ID
		else:
			return []  # App not found, return an empty array

	except Exception as e:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Error deleting app: {str(e)}', [app_id, app_name], 'deleteApp', '')
		severLog.error(json_msg)
		print("Error deleting app:", str(e))
		return []  # Return an empty array in case of an error
    

def updateApp():
	try:
		try:
			sql = sqlite
			app_id = int(arg[2])
			port = int(arg[3])
			status = int(arg[4])
			project_id = int(arg[5])
		except:
			json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected Fuction Error: {sys.exc_info()[0]}', [app_id], 'updateApp', '')
			severLog.error(json_msg)
			print("Unexpected updateApp Fuction Error:", sys.exc_info()[0])
			
		# Query the database to delete the app record
		app_id = core.updateapp(sql, './data/sys.db', app_id, port, status, project_id)
		json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Updating app: {app_id}', [app_id, port, status, project_id], 'updateApp', '')
		severLog.info(json_msg)
		print('Updating app:', app_id)

		if app_id[0] > 0:
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Updated app: {app_id}', [app_id, port, status, project_id], 'updateApp', '')
			severLog.info(json_msg)
			print('Updated app:', app_id)
			return app_id  # Return the updated app ID
		else:
			return []  # App not found, return an empty array

	except Exception as e:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Error updating app: {str(e)}', [app_id], 'updateApp', '')
		severLog.error(json_msg)
		print("Error updating app:", str(e))
		return []  # Return an empty array in case of an error


def runRoutine():
	""" Run routines in the foreground.
	To test routines on the terminal use:
	pid = core.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app[1], EXEC)) """
	print(VERSION)
	settings = getSystemSettings()
	EXEC = settings[0][4]
	PATH = settings[0][5]
	res = True
	ROUTINE_LIST = getRoutineList()
	routine_name = str(arg[2]).replace(' ', '')
	try:
		for app in ROUTINE_LIST:
			if app[1] == routine_name:
				print('runRoutine', app)
				pid = core.runOS('{2} {0}/routines/{1}/{1}.py {3}'.format(PATH, app[1], EXEC, app[2]))
				json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Running app pid: {pid}', [pid, app], 'runRoutine', '')
				severLog.info(json_msg)
				print(app[0], 'running on port:', app[2], 'pid:', pid)
	except:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected testApp Fuction Error: {sys.exc_info()[0]}', [routine_name], 'runRoutine', '')
		severLog.error(json_msg)
		print("Unexpected testApp Fuction Error:", sys.exc_info()[0])
		res = False
		pass
	return True


def createRoutine():
	""" Create routines application function. """
	appName = 'app_{0}'.format(random.randint(0, 99))
	port = '9090'
	status = 1
	project_id = 1
	try:
		sql = sqlite
		appName = str(arg[2]).replace(' ', '')
		port = int(arg[3])
		status = int(arg[4])
		project_id = int(arg[5])
	except:
		pass

	# Query the database to delete the app record
	app_id = core.createroutine(sql, './data/sys.db', appName, port, status, project_id)
	json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Generating routines id: {app_id}', [appName, port, status, project_id], 'createRoutine', '')
	severLog.info(json_msg)
	print('Generating routine:', app_id)

	path = os.getcwd()
	source_folder = r"{0}/routines/.routine".format(path)
	destination_folder = r"{0}/routines/{1}".format(path, appName)
	if not os.path.exists(destination_folder):
		try:
			shutil.copytree(source_folder, destination_folder)
			with open("{0}/routines/{1}/handlers/_name_.py".format(path, appName), 'w') as f:
				f.write("APP_NAME = '{0}'".format(appName))
			os.rename("{0}/routines/{1}/routine.py".format(path, appName), "{0}/routines/{1}/{1}.py".format(path, appName))
			with open("{0}/routines/{1}/handlers/_path_.py".format(path, appName), 'w') as f:
				f.write("PATH = '{0}'".format(path))
			with open("{0}/routines/{1}/handlers/_config_.py".format(path, appName), 'w') as f:
				f.write("PORT = '{0}'".format(port))
				f.write("\n")
				f.write("COOKIE_SECRET = '{0}'".format(config.COOKIE_SECRET))
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Created routines app: {appName}', [appName, port, status, project_id], 'createRoutine', '')
			severLog.info(json_msg)
			print('{0} routine application created.'.format(appName))
		except FileNotFoundError:
			json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected Fuction Error: {sys.exc_info()[0]}', [appName, port, status, project_id], 'createRoutine', '')
			severLog.error(json_msg)
			print("Unexpected createRoutine Fuction Error:", sys.exc_info()[0])
	else:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Application files already exist: {appName}', [appName, port, status, project_id], 'createRoutine', '')
		severLog.error(json_msg)
		print('{0} application files already exist. createRoutine()'.format(appName))


def deleteRoutine():
	try:
		sql = sqlite
		app_name = str(arg[2]).replace(' ', '')
		sys_app_name = 'manage'
		
		# Query the database to delete the app record
		if not sys_app_name == app_name:
			app_id = core.deleteroutine(app_name, sql, './data/sys.db')
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Deleting routine app: {app_id}', [app_id, app_name], 'deleteRoutine', '')
			severLog.info(json_msg)
			print('Deleting routine:', app_id)

			if app_id[0] > 0:
				# Delete the app files from the "apps/" directory
				path = os.getcwd()
				app_directory = r"{0}/routines/{1}".format(path, app_name)
				if os.path.exists(app_directory):
					core.delete_directory(app_directory)

			return app_id  # Return the deleted app ID
		else:
			return []  # App not found, return an empty array

	except Exception as e:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Error routine deleting app: {str(e)}', [app_id, app_name], 'deleteRoutine', '')
		severLog.error(json_msg)
		print("Error deleting routine app:", str(e))
		return []  # Return an empty array in case of an error
    

def updateRoutine():
	try:
		try:
			sql = sqlite
			app_id = int(arg[2])
			port = int(arg[3])
			status = int(arg[4])
			project_id = int(arg[5])
		except:
			json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Unexpected Fuction Error: {sys.exc_info()[0]}', [app_id], 'updateRoutine', '')
			severLog.info(json_msg)
			print("Unexpected updateRoutine Fuction Error:", sys.exc_info()[0])
			
		# Query the database to delete the app record
		app_id = core.updateroutine(sql, './data/sys.db', app_id, port, status, project_id)
		json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Updating routine: {app_id}', [app_id, port, status, project_id], 'updateRoutine', '')
		severLog.info(json_msg)
		print('Updating routine:', app_id)

		if app_id[0] > 0:
			json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Updated routine: {app_id}', [app_id, port, status, project_id], 'updateRoutine', '')
			severLog.info(json_msg)
			print('Updated routine:', app_id)
			return app_id  # Return the updated app ID
		else:
			return []  # App not found, return an empty array

	except Exception as e:
		json_msg = config.jsonLogger(core.getUTCNow(), 'ERROR', f'Error updating routine app: {str(e)}', [app_id], 'updateRoutine', '')
		severLog.error(json_msg)
		print("Error updating routine app:", str(e))
		return []  # Return an empty array in case of an error


def setPath(path=os.getcwd()):
	""" Set path across system stettings.. """
	path = path
	manage = '_path_.py'
	monitor = '_path_.py'
	public = '_path_.py'
	try:
		path = str(arg[2]).replace(' ', '')
		path = ''.join(str(path).split())
		path = r"{0}".format(path)
	except:
		pass
	destination_app = r"{0}/apps/manager/{1}".format(path, manage)
	destination_routine = r"{0}/routines/monitor/{1}".format(path, monitor)
	destination_public = r"{0}/public/{1}".format(path, public)
	print('Setting path directory:', path)
	if os.path.exists(f"{path}/public"):
		try:
			with open("{0}/apps/manage/handlers/{1}".format(path, manage), 'w') as f:
				f.write("PATH = '{0}'".format(path))
			severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Path set.', [path, 'manage', manage], 'setPath', ''))
			print('{0} {1} path set.'.format(path, 'manage'))
		except FileNotFoundError:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Path set.', [path, 'manage', manage, sys.exc_info()[0]], 'setPath', ''))
			print("Unexpected setPath Fuction Error:", sys.exc_info()[0])
		
		try:
			with open("{0}/routines/monitor/handlers/{1}".format(path, monitor), 'w') as f:
				f.write("PATH = '{0}'".format(path))
			severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Path set.', [path, 'monitor', monitor], 'setPath', ''))
			print('{0} {1} path set.'.format(path, 'monitor'))
		except FileNotFoundError:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Path set.', [path, 'monitor', manage, sys.exc_info()[0]], 'setPath', ''))
			print("Unexpected setPath Fuction Error:", sys.exc_info()[0])
		
		try:
			with open("{0}/public/{1}".format(path, public), 'w') as f:
				f.write("PATH = '{0}'".format(path))
			severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Path set.', [path, 'public', manage], 'setPath', ''))
			print('{0} {1} path set.'.format(path, 'public'))
		except FileNotFoundError:
			severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Path set.', [path, 'public', manage, sys.exc_info()[0]], 'setPath', ''))
			print("Unexpected setPath Fuction Error:", sys.exc_info()[0])
	else:
		severLog.error(config.jsonLogger(core.getUTCNow(), 'ERROR', f'Path config directory not found.', [path], 'setPath', ''))
		print('{0} config directory not found. setPath()'.format(f"{path}/public"))


def showVersion():
	""" Show application version. """
	print(VERSION)


def gendb():
	""" Generate initial database settings. """
	path=os.getcwd()
	try:
		path = ''.join(str(arg[2]).split())
		path = r"{0}".format(path)
	except:
		pass
	initdb.main(path)
	setPath(path)
	json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Generate initial database settings.', [], 'gendb', '')
	severLog.info(json_msg)


def resetdb():
	""" Reset initial database settings. """
	path=os.getcwd()
	PASSD_STRING = core.generate_passphrase()
	COOKIE_SECRET = core.generate_passphrase(32)
	CYPHER = core.generate_passphrase(16)
	try:
		path = ''.join(str(arg[2]).split())
		path = r"{0}".format(path)
	except:
		pass
	initdb.resetdbfiles(path)
	initdb.geninitfiles(path, PASSD_STRING, COOKIE_SECRET, CYPHER, reset=1)
	initdb.main(path)
	setPath(path)
	json_msg = config.jsonLogger(core.getUTCNow(), 'INFO', f'Reset initial database settings.', [], 'resetdb', '')
	severLog.info(json_msg)


def showHelp():
	print(VERSION)
	print("$ cwf -v | Show version number.")
	print("$ cwf -h | Shows Help Menu.")
	print("$ cwf --init | Initialize database settings using current directory as path.")
	print("$ cwf --init '/path/to/cwf/container' | Initialize database settings.")
	print("$ cwf --reset | Reset database settings using current directory as path.")
	print("$ cwf --reset '/path/to/cwf/container' | Reset database settings.")
	print("$ cwf --setpath '/path/to/cwf/container' | Set/Update container path settings.")
	print("$ cwf --listapps | List all apps.")
	print("$ cwf --listroutines | List all routine apps.")
	print("$ cwf --apps | Runs enabled apps.")
	print("$ cwf --routines | Runs all enabled routine apps.")
	print("$ cwf --runapp 'myapp_name' | Run app in foreground mode.")
	print("$ cwf --runroutine 'myapp_name' | Run routine app in foreground mode.")
	print("$ cwf --createapp 'myapp_name' | Creates app.")
	print("$ cwf --createapp 'myapp_name' [PORT] [1|0] [project_id] | Creates app with values. status = 0|1")
	print("$ cwf --deleteapp 'myapp_name' | Deletes app.")
	print("$ cwf --updateapp 'myapp_id [PORT] [STATUS] [project_id]' | Update app. status = 0|1")
	print("$ cwf --createroutine 'myapp_name' | Creates routine app.")
	print("$ cwf --createroutine 'myapp_name' [PORT] [1|0] [project_id] | Creates routine app with values. status = 0|1")
	print("$ cwf --deleteroutine 'myapp_name' | Deletes routine app.")
	print("$ cwf --updateroutine 'myapp_id [PORT] [STATUS] [project_id]' | Update routine app. status = 0|1")
	severLog.info(config.jsonLogger(core.getUTCNow(), 'INFO', f'Printing menu.', [], 'showHelp', ''))


def defaultAction():
	core.exitAction()


# Commands with one(1) variable:
def optionCheck():
	op = str(arg[1])
	{
		'-v': showVersion,
		'-h': showHelp,
		'--init': gendb,
		'--reset': resetdb,
		'--setpath': setPath,
		'--apps': runApps,
		'--runapp': runApp,
		'--runroutine': runRoutine,
		'--routines': runRoutines,
		'--listapps': getAppList,
		'--listroutines': getRoutineList,
		'--createapp': createApp,
		'--deleteapp': deleteApp,
		'--createroutine': createRoutine,
		'--deleteroutine': deleteRoutine,
	}.get(op, defaultAction)()


# Commands with more than one(1) variable:
def multiCheck():
	op = str(arg[1])
	{
		'--createapp': createApp,
		'--updateapp': updateApp,
		'--createroutine': createRoutine,
		'--updateroutine': updateRoutine,
	}.get(op, defaultAction)()


if __name__ == "__main__":
	{1: showHelp, 2: optionCheck, 3: optionCheck, 4: multiCheck, 5: multiCheck, 6: multiCheck}.get(len(arg), defaultAction)()
