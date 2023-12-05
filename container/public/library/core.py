import os, sys, subprocess, datetime, time, shutil
import hashlib, rsa
import random, string


# Import public modules:
PARENT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PARENT_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
PARENT_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
sys.path.append(PARENT_ROOT)

# Import Global Configs:
import public.config as config

#Initializing variables
PATH = config.WEBPATH
severLog = config.severLog


#Utility Functions:

def exitAction():
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Exiting...', [], 'exitAction', ''))
	print("Exiting...")
	sys.exit(1)


def runOS(cmd):
	""" Run function using os.system libraries. """
	out = os.system(cmd)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Run function using os.system libraries.', [cmd, out], 'runOS', ''))
	return out


def runSP(cmd):
	""" Run OS application in the background using subprocess libraries. """
	p = subprocess.Popen(str(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Run OS application in the background using subprocess libraries.', [cmd, p.pid], 'runSP', ''))
	return p.pid


def getOidDateNow(oid):
	""" Returns integer concatinaring Today date UTC time without Seconds and oid. """
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Returns integer concatinaring Today date UTC time without Seconds and oid.', [oid], 'getOidDateNow', ''))
	return int(str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')) + str(oid))


def cNow():
	""" Returns string long date and time. """
	return time.ctime()


def getISOStrFormatNow():
	""" Returns string local iso format, striping especial characters with spaces. """
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Returns string iso format, striping especial characters with spaces.', [], 'getISOStrFormatNow', ''))
	return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def getISONow():
	""" Returns string local iso format with miliseconds. """
	res = datetime.datetime.now().isoformat()
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Returns string local iso format with miliseconds.', [res], 'getISONow', ''))
	return res


def getUTCNow():
	""" Returns string UTC iso format with miliseconds. """
	now = datetime.datetime.now().utcnow().isoformat()
	return now


def getUTCOffset():
	""" Calculate UTC Offset. """
	UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Calculate UTC Offset.', [UTC_OFFSET_TIMEDELTA], 'getUTCOffset', ''))
	return UTC_OFFSET_TIMEDELTA


def getDeltaISO(value):
	""" Delta local time
	:value: Positive Integer
	:metric: minutes, seconds, days, months, years """
	now = datetime.datetime.now()
	delta = datetime.timedelta(seconds=value)
	res = (now - delta)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Delta local time.', [now, delta, res], 'getDeltaISO', ''))
	return res.isoformat()


def getDeltaUTCISO(value):
	""" Delta UTC time
	:value: Positive Integer
	:metric: minutes, seconds, days, months, years """
	now = datetime.datetime.utcnow()
	delta = datetime.timedelta(seconds=value)
	res = (now - delta)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Delta UTC time.', [now, delta, res], 'getDeltaUTCISO', ''))
	return res


def covertToISO(dateString):
	""" Convert String to local ISOdate string format and return current timestanp if string is not properly formatted. """
	now = datetime.datetime.now().isoformat()
	try:
		s = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
		now = s.isoformat()
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Convert String to local ISOdate string format.', [s, now], 'covertToISO', ''))
	except:
		print("Unexpected covertToISO Fuction Error:", sys.exc_info()[0])
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Convert String to local ISOdate string format.', [now], 'covertToISO', ''))
		pass
	return now


def covertToUTCISO(dateString):
	""" Convert String to UTC ISOdate string format and return current timestanp if string is not properly formatted. """
	now = datetime.datetime.utcnow()
	try:
		s = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
		now = s
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Convert String to UTC ISOdate string format.', [], 'covertToUTCISO', ''))
	except:
		print("Unexpected covertToISO Fuction Error:", sys.exc_info()[0])
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Convert String to UTC ISOdate string format.', [], 'covertToUTCISO', ''))
		pass
	return now


def convertLocalToUTC(localDatetimeString, offset):
	""" Offset is calculated by UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now(): """
	local = datetime.datetime.strptime(localDatetimeString, '%Y-%m-%d %H:%M:%S')
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Offset is calculated by UTC_OFFSET_TIMEDELTA.', [local, offset], 'convertLocalToUTC', ''))
	return (local + offset)


def covertToISOFormat(dateString):
	""" Convert String to local ISOdate format and return current timestanp if string is not properly formatted. """
	now = datetime.datetime.now().isoformat()
	try:
		now = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Convert String to local ISOdate format.', [now], 'covertToISOFormat', ''))
	except:
		print("Unexpected covertToISO Fuction Error:", sys.exc_info()[0])
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Convert String to local ISOdate format.', [now], 'covertToISOFormat', ''))
		pass
	return now


def covertToISOFormatUTC(dateString):
	""" Convert String to UTC ISOdate format and return current timestanp if string is not properly formatted. """
	now = datetime.datetime.now().utcnow()
	try:
		now = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S').utcnow()
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Convert String to UTC ISOdate format.', [now], 'covertToISOFormatUTC', ''))
	except:
		print("Unexpected covertToISOFormatUTC Fuction Error:", sys.exc_info()[0])
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Convert String to UTC ISOdate format.', [now], 'covertToISOFormatUTC', ''))
		pass
	return now


def covertUnixToUTC(unixtime=0):
	""" Convert unixtime interger to UTC string timestamp. """
	dt_utc_aware = datetime.datetime.fromtimestamp(int(unixtime), datetime.timezone.utc)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Convert unixtime interger to UTC string timestamp.', [dt_utc_aware], 'covertUnixToUTC', ''))
	return str(dt_utc_aware)


def isNumber(s):
	""" Check is value is a number. """
	try:
		float(s)
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Check is value is a number.', [s], 'isNumber', ''))
		return True
	except ValueError:
		print("isNumber() Error")
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Check is value is a number.', [s], 'isNumber', ''))
		return False


def delete_directory(directory_path):
	""" Delete directory. """
	try:
		# List all files and subdirectories within the directory
		for item in os.listdir(directory_path):
			item_path = os.path.join(directory_path, item)
			
			if os.path.isfile(item_path):
				# If it's a file, remove it
				os.remove(item_path)
			elif os.path.isdir(item_path):
				# If it's a subdirectory, recursively delete it
				delete_directory(item_path)

		# Finally, remove the empty directory
		os.rmdir(directory_path)
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Deleted successfully.', [directory_path], 'delete_directory', ''))
		print(f"Directory '{directory_path}' deleted successfully.")

	except Exception as e:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'', [directory_path], 'delete_directory', ''))
		print(f"Error deleting directory '{directory_path}': {str(e)}")


# Encryption functions:

def generate_passphrase(length=13):
	""" Generate passphrarse. """
	length = length
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'generate_passphrase', ''))
	return ''.join(random.choice(chars) for i in range(length))


def generate_secret(bits=4096, keys_path='.'):
	""" Generate rsa keys for authentication. """
	(pubkey, privkey) = rsa.newkeys(bits, poolsize=4)
	pub_key_file = open('{0}/public/.keys/pubkey'.format(keys_path), 'w+')
	pub_key_file.write(pubkey.save_pkcs1().decode('utf-8'))
	pub_key_file.close()
	priv_key_file = open('{0}/public/.keys/privkey'.format(keys_path), 'w+')
	priv_key_file.write(privkey.save_pkcs1().decode('utf-8'))
	priv_key_file.close()
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Generate rsa keys for authentication.', [], 'generate_secret', ''))
	print(f"Generated rsa keys for authentication.\n")


def load_secret(keys_path='.'):
	"""Load rsa keys from file."""
	with open('{0}/public/.keys/pubkey'.format(keys_path), 'rb') as fp:         
		fpkey = fp.read()
		pubkey = rsa.PublicKey.load_pkcs1(fpkey)
	with open('{0}/public/.keys/privkey'.format(keys_path), 'rb') as fs:           
		fskey = fs.read()
		privkey = rsa.PrivateKey.load_pkcs1(fskey)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'load_secret', ''))
	return (pubkey, privkey)


def load_pubkey(keys_path='.'):
	"""Load rsa public key from file."""
	with open('{0}/public/.keys/pubkey'.format(keys_path), 'rb') as fp:         
		fpkey = fp.read()
		pubkey = rsa.PublicKey.load_pkcs1(fpkey)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'load_pubkey', ''))
	return pubkey


def encrypt_message(message, pubkey):
	""" rsa.encrypt method is used to encrypt
	string with public key string should be
	encode to byte string before encryption
	with encode method
	message: string
	"""
	encMessage = rsa.encrypt(message.encode('utf8'), pubkey)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'encrypt_message', ''))
	return encMessage


def decrypt_message(encMessage, privkey):
	""" The encrypted message can be decrypted
	with rsa.decrypt method and private key
	decrypt method returns encoded byte string,
	use decode method to convert it to string
	public key cannot be used for decryption
	encMessage: encrypted message
	"""
	decMessage = rsa.decrypt(encMessage, privkey).decode()
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'decrypt_message', ''))
	return decMessage


def compute_hash_sha1(message):
	""" Input message can be an encoded string or byte. 
	Encoded message string.encode('utf8')
	"""
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'compute_hash_sha1', ''))
	return rsa.compute_hash(message, 'SHA-1')


def get_hash_sha1_hex(message):
	""" Encoded message string.encode('utf8')"""
	hash_object = hashlib.sha1(message)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'get_hash_sha1_hex', ''))
	return hash_object.hexdigest()


def generate_hex_password(passd_string, cypher_string):
	""" Generate hash hex from raw password string and a given cypher. """
	passd_string = passd_string
	cypher_string = cypher_string
	hex = get_hash_sha1_hex((passd_string+cypher_string).encode('utf8'))
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'generate_hex_password', ''))
	return hex


def generate_rsa_password(passd_string, cypher_string):
	""" Generate encrypted rsa object from a hash hex, raw password string and a given cypher.
	#At the client level:
	#client_hex_str = get_hash_sha1_hex(user_string_passd+CYPHER.encode('utf8'))
	#At the server level:
	#encObject = encrypt_message(client_hex_str.encode('utf8'), pubkey)
	"""
	passd_string = passd_string
	cypher_string = cypher_string
	pubkey = load_pubkey()
	hex = get_hash_sha1_hex((passd_string+cypher_string).encode('utf8'))
	encobject = encrypt_message(hex, pubkey)
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'generate_rsa_password', ''))
	return encobject


def check_rsa_password(user, hex_string, enc_msg):
	""" Check hash hex string agaist an encrypted rsa object from db. """
	hex_string = hex_string
	user = user
	enc_msg = enc_msg
	pubkey, privkey = load_secret()
	decobject = decrypt_message(enc_msg, privkey)
	print('decrypred:', decobject)
	print('hex_string:', hex_string)
	if hex_string == decobject:
		severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'check_rsa_password', ''))
		return True
	else:
		severLog.error(config.jsonLogger(getUTCNow(), 'WARN', f'Password does NOT match.', [user, hex_string, decobject], 'check_rsa_password', ''))
		return False
     

# File system function:

def createFilesApp(appPort, appCookie, appName=[]):
	""" Generate application files. """
	if appName:
		appName = str(appName).replace(' ', '')
	else:
		appName = 'app_{0}'.format(random.randint(0, 99))
	appPort = int(appPort)
	appCookie = str(appCookie)
	path = os.getcwd()
	source_folder = r"{0}/apps/.app".format(path)
	destination_folder = r"{0}/apps/{1}".format(path, appName)
	try:
		shutil.copytree(source_folder, destination_folder)
		with open("{0}/apps/{1}/handlers/_name_.py".format(path, appName), 'w') as f:
			f.write("APP_NAME = '{0}'".format(appName))
		os.rename("{0}/apps/{1}/app.py".format(path, appName), "{0}/apps/{1}/{1}.py".format(path, appName))
		with open("{0}/apps/{1}/handlers/_path_.py".format(path, appName), 'w') as f:
			f.write("PATH = '{0}'".format(path))
		with open("{0}/apps/{1}/handlers/_config_.py".format(path, appName), 'w') as f:
			f.write("PORT = '{0}'".format(appPort))
			f.write("\n")
			f.write("COOKIE_SECRET = '{0}'".format(appCookie))
	except FileNotFoundError:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Unexpected Fuction Error:', [sys.exc_info()[0]], 'createFilesApp', ''))
		print("Unexpected createFilesApp Fuction Error:", sys.exc_info()[0])
		return []
	print('{0} application files created.'.format(appName))
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Application files created.', [source_folder, destination_folder], 'createFilesApp', ''))
	return 1


def deleteFilesApp(app_name):
	""" Delete application files. """
	try:
		app_name = str(app_name.replace(' ', ''))
		if app_name:
			# Delete the app files from the "apps/" directory
			path = os.getcwd()
			app_directory = r"{0}/apps/{1}".format(path, app_name)
			if os.path.exists(app_directory):
				delete_directory(app_directory)
				severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Application files deleted.', [1], 'deleteFilesApp', ''))
				return 1  # Return True
		else:
			return []  # App not found, return an empty array
	except Exception as e:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Error deleting app files:', [e], 'deleteFilesApp', ''))
		print("Error deleting app files:", str(e))
		return []  # Return an empty array in case of an error


def createFilesRoutine(appPort, appCookie, appName=[]):
	""" Generate routine application files. """
	if appName:
		appName = str(appName).replace(' ', '')
	else:
		appName = 'routine_{0}'.format(random.randint(0, 99))
	appPort = int(appPort)
	appCookie = str(appCookie)
	path = os.getcwd()
	source_folder = r"{0}/routines/.routine".format(path)
	destination_folder = r"{0}/routines/{1}".format(path, appName)
	try:
		shutil.copytree(source_folder, destination_folder)
		with open("{0}/routines/{1}/handlers/_name_.py".format(path, appName), 'w') as f:
			f.write("APP_NAME = '{0}'".format(appName))
		os.rename("{0}/routines/{1}/routine.py".format(path, appName), "{0}/routines/{1}/{1}.py".format(path, appName))
		with open("{0}/routines/{1}/handlers/_path_.py".format(path, appName), 'w') as f:
			f.write("PATH = '{0}'".format(path))
		with open("{0}/routines/{1}/handlers/_config_.py".format(path, appName), 'w') as f:
			f.write("PORT = '{0}'".format(appPort))
			f.write("\n")
			f.write("COOKIE_SECRET = '{0}'".format(appCookie))
	except FileNotFoundError:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Unexpected Fuction Error:', [sys.exc_info()[0]], 'createFilesRoutine', ''))
		print("Unexpected createFilesRoutine Fuction Error:", sys.exc_info()[0])
		return []
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Routine application files created.', [source_folder, destination_folder], 'createFilesRoutine', ''))
	print('{0} routine application files created.'.format(appName))
	return 1


def deleteFilesRoutine(app_name):
	try:
		app_name = str(app_name.replace(' ', ''))
		if app_name:
			# Delete the app files from the "routines/" directory
			path = os.getcwd()
			app_directory = r"{0}/routines/{1}".format(path, app_name)
			if os.path.exists(app_directory):
				delete_directory(app_directory)
				severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Routine application files deleted.', [1], 'deleteFilesRoutine', ''))
				return 1  # Return True
		else:
			return []  # App not found, return an empty array
	except Exception as e:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'Error deleting routine app files:', [e], 'deleteFilesRoutine', ''))
		print("Error deleting routine app files:", str(e))
		return []  # Return an empty array in case of an error


# Database functions:

def getdbtable(dbtype, database_path, db_table):
	""" Get database table records. """
	res = []
	sql = dbtype
	table = ''
	if db_table:
		table = str(db_table).replace(' ', '')

	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Update values into the 'given' table
			sql = """SELECT * FROM {0};""".format(table)
			cursor.execute(sql)

			# Get rows
			res = cursor.fetchall()

			# Commit the changes
			conn.commit()

			print(f"Query '{table}' on '{database_path}' executed successfully.")
		except sql.Error as e:
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'', [table, res], 'getdbtable', ''))
		print(f"Database table '{table}' does NOT exists. getdbtable()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [table, res], 'getdbtable', ''))
	return res


def createuser(dbtype, database_path, CYPHER, name, email, passd_string, admin_role):
	""" Create a new user. """
	res = []
	sql = dbtype
	name = str(name)
	email = str(email)
	passd_string = str(passd_string)
	admin_role = int(admin_role)
	database_path = r"{0}".format(database_path)
	generated_user_passd = '''{0}'''.format(generate_hex_password(passd_string, CYPHER))
	generated_user_passb = generate_rsa_password(passd_string, CYPHER)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'users' table
			cursor.execute('''INSERT INTO users (name, email, passd, passb, admin)
								VALUES (?, ?, ?, ?, ?)''',
							(name, email, generated_user_passd, generated_user_passb, admin_role))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"New user on '{database_path}' created successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'createuser', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exist.', [database_path], 'createuser', ''))
		print(f"Database '{database_path}' does NOT exists. createuser()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'User created.', [res], 'createuser', ''))
	return res


def updateuser(dbtype, database_path, user_id, CYPHER, name, email, passd_string, admin_role):
	""" Update a new user. """
	res = []
	sql = dbtype
	table = 'users'
	user_id = int(user_id)
	name = str(name)
	email = str(email)
	passd_string = str(passd_string)
	admin_role = int(admin_role)
	database_path = r"{0}".format(database_path)
	generated_user_passd = '''{0}'''.format(generate_hex_password(passd_string, CYPHER))
	generated_user_passb = generate_rsa_password(passd_string, CYPHER)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'users' table
			sql = """UPDATE {0} SET name = ?, email = ?, passd = ?, passb = ?, admin = ? WHERE _id = ?;""".format(table)
			cursor.execute(sql, (name, email, generated_user_passd, generated_user_passb, admin_role, user_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"User on '{database_path}' updated successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'updateuser', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'', [], 'updateuser', ''))
		print(f"Database '{database_path}' does NOT exists. updateuser()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'User updated.', [res], 'updateuser', ''))
	return res


def deleteuser(user_id, dbtype, database_path):
	res = []
	sql = dbtype
	table = 'users'
	user_id = int(user_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Delete user from the 'users' table
			sql = """DELETE FROM {0} WHERE rowid = '{1}'""".format(table, user_id)
			cursor.execute(sql)

			# Get lastrowid
			res.append(cursor.rowcount)

			# Commit the changes
			conn.commit()
			if res[0] != 0:
				print(f"User on '{database_path}' deleted successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'deleteuser', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'deleteuser', ''))
		print(f"Database '{database_path}' does NOT exists. deleteuser()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'User deleted.', [res], 'deleteuser', ''))
	return res


def createapp(dbtype, database_path, name, port, status, project_id=1):
	""" Create a new app record. """
	res = []
	sql = dbtype
	name = str(name)
	port = str(port)
	status = str(status)
	project_id = int(project_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'apps' table
			cursor.execute('''INSERT INTO apps (name, port, status, project_id)
								VALUES (?, ?, ?, ?)''',
							(name, port, status, project_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"New app on '{database_path}' created successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'createapp', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'createapp', ''))
		print(f"Database '{database_path}' does NOT exists. createapp()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'App created.', [res], 'createapp', ''))
	return res


def deleteapp(app_name, dbtype, database_path):
	""" Delete an app record. """
	res = []
	sql = dbtype
	table = 'apps'
	app_name = str(app_name)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Delete user from the 'apps' table
			sql = """DELETE FROM {0} WHERE name = '{1}'""".format(table, app_name)
			print(sql)
			cursor.execute(sql)

			# Get lastrowid
			res.append(cursor.rowcount)

			# Commit the changes
			conn.commit()
			if res[0] != 0:
				print(f"Delete app statement ran on '{database_path}' successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'deleteapp', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'deleteapp', ''))
		print(f"Database '{database_path}' does NOT exists. deleteapp()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'App deleted.', [res], 'deleteapp', ''))
	return res


def updateapp(dbtype, database_path, app_id, port, status, project_id):
	""" Update app record. """
	res = []
	sql = dbtype
	table = 'apps'
	app_id = int(app_id)
	port = int(port)
	status = int(status)
	project_id = int(project_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Update values into the 'apps' table
			sql = """UPDATE {0} SET port = ?, status = ?, project_id = ? WHERE _id = ?;""".format(table)
			cursor.execute(sql, (port, status, project_id, app_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"Updated app on '{database_path}' successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'updateapp', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'updateapp', ''))
		print(f"Database '{database_path}' does NOT exists. updateapp()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'App updated.', [res], 'updateapp', ''))
	return res


def createroutine(dbtype, database_path, name, port, status, project_id=1):
	""" Create a new routine app record. """
	res = []
	sql = dbtype
	name = str(name)
	port = str(port)
	status = str(status)
	project_id = int(project_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'routine' table
			cursor.execute('''INSERT INTO routines (name, port, status, project_id)
								VALUES (?, ?, ?, ?)''',
							(name, port, status, project_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"New routine app on '{database_path}' created successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'createroutine', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'createroutine', ''))
		print(f"Database '{database_path}' does NOT exists. createroutine()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'createroutine', ''))
	return res


def deleteroutine(app_name, dbtype, database_path):
	""" Delete a routine app record. """
	res = []
	sql = dbtype
	table = 'routines'
	app_name = str(app_name)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Delete user from the 'routines' table
			sql = """DELETE FROM {0} WHERE name = '{1}'""".format(table, app_name)
			print(sql)
			cursor.execute(sql)

			# Get lastrowid
			res.append(cursor.rowcount)

			# Commit the changes
			conn.commit()
			if res[0] != 0:
				print(f"Delete routine app statement ran on '{database_path}' successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'deleteroutine', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'deleteroutine', ''))
		print(f"Database '{database_path}' does NOT exists. deleteroutine()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'deleteroutine', ''))
	return res


def updateroutine(dbtype, database_path, app_id, port, status, project_id):
	""" Update routine app record. """
	res = []
	sql = dbtype
	table = 'routines'
	app_id = int(app_id)
	port = int(port)
	status = int(status)
	project_id = int(project_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Update values into the 'routines' table
			sql = """UPDATE {0} SET port = ?, status = ?, project_id = ? WHERE _id = ?;""".format(table)
			cursor.execute(sql, (port, status, project_id, app_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"Updated routine app on '{database_path}' successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'updateroutine', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'updateroutine', ''))
		print(f"Database '{database_path}' does NOT exists. updateroutine()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'updateroutine', ''))
	return res


def createproject(dbtype, database_path, name, user_id=1):
	""" Create a new project record. """
	res = []
	sql = dbtype
	name = str(name)
	user_id = int(user_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'projects' table
			cursor.execute('''INSERT INTO projects (name, user_id)
								VALUES (?, ?)''',
							(name, user_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"New project on '{database_path}' created successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'createproject', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'createproject', ''))
		print(f"Database '{database_path}' does NOT exists. createproject()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'createproject', ''))
	return res


def deleteproject(project_id, dbtype, database_path):
	""" Delete a project record. """
	res = []
	sql = dbtype
	table = 'projects'
	project_id = int(project_id)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Delete user from the 'users' table
			sql = """DELETE FROM {0} WHERE rowid = '{1}'""".format(table, project_id)
			print(sql)
			cursor.execute(sql)

			# Get lastrowid
			res.append(cursor.rowcount)

			# Commit the changes
			conn.commit()
			if res[0] != 0:
				print(f"Delete project statement ran on '{database_path}' successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'deleteproject', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'deleteproject', ''))
		print(f"Database '{database_path}' does NOT exists. deleteproject()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'', [], 'deleteproject', ''))
	return res


def updatesetting(dbtype, database_path, setting_id, setting_exec, setting_path, setting_port):
	""" Update settings. """
	res = []
	sql = dbtype
	table = 'settings'
	setting_id = int(setting_id)
	setting_exec = str(setting_exec)
	setting_path = str(setting_path)
	setting_port = int(setting_port)
	database_path = r"{0}".format(database_path)
	if os.path.exists(database_path):
		try:
			# Create or connect to the database file
			conn = sql.openDB(database_path)

			# Create a cursor object to execute SQL commands
			cursor = conn.cursor()

			# Insert default values into the 'users' table
			sql = """UPDATE {0} SET exec = ?, webpath = ?, dport = ? WHERE _id = ?;""".format(table)
			cursor.execute(sql, (setting_exec, setting_path, setting_port, setting_id))

			# Get lastrowid
			res.append(cursor.lastrowid)

			# Commit the changes
			conn.commit()

			print(f"Settings on '{database_path}' updated successfully.")
		except sql.Error as e:
			severLog.error(config.jsonLogger(getUTCNow(), 'ERROR', f'SQLite error:', [e], 'updatesetting', ''))
			print(f"SQLite error: {e}")
		finally:
			# Close the database connection
			conn.close()
	else:
		severLog.warning(config.jsonLogger(getUTCNow(), 'WARN', f'Database path does NOT exists.', [database_path], 'updatesetting', ''))
		print(f"Database '{database_path}' does NOT exists. updatesetting()")
	severLog.info(config.jsonLogger(getUTCNow(), 'INFO', f'Settings updated.', [res], 'updatesetting', ''))
	return res