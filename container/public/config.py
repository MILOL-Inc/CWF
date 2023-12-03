import public._version_ as _version_
import public._pass_ as _pass_
import public._cypher_ as _cypher_
import public._csecret_ as _csecret_
import public._exec_ as _exec_
import public._path_ as _path_
import public._dport_ as _dport_
import logging, logging.handlers, json, smtplib, time, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#System settings: (True: development | False: production)
DEVELOPMENT_ENV = True

#Version:
COMPANY_NAME = 'CWF'
VERSION = _version_.VERSION
RELEASE = '''{0} {1}'''.format(COMPANY_NAME, _version_.VERSION)

#####################################################################
# After initdb is initiated. Refer to system database for settings. #
#####################################################################

#String Initial Password:
PASS = _pass_.PASS

#Cypher Passphrase:
CYPHER = _cypher_.CYPHER

#Cookie Passphrase:
COOKIE_SECRET = _csecret_.COOKIE_SECRET

#Pyhton runtime enviroment. Ex. python, pyhton3, pypy, pypy3:
EXEC = _exec_.EXEC

#Full Path where the application is deployed:
WEBPATH = _path_.PATH

#Default App Port:
DEFAULT_PORT = _dport_.DEFAULT_PORT

#Email settings:
EMAILSRV = '127.0.0.1'
FROM = 'email_from@domain_name'
TO = 'email_to@domain_name'
CC = ''

#Initializing Email function variables:
emailServer = EMAILSRV
eFrom = FROM
eTo = TO
eCc = CC

#Apps list:
# 'app_name': {'name': 'APP_NAME', 'port': 8090, 'status': 1, 'project_id': 1}
# ('APP_NAME', 8090, 1)
apps = [(1, 'manage', 8090, 1, 1)]

#Routines list:
# 'routine_name': {'name': 'ROUTINE_NAME', 'port': 9090, 'status': 1, 'project_id': 1}
# ('ROUTINE_NAME', 9090, 1, 1)
routines = []

#Default Users:
# 'username': {'name': 'Admin', 'email': 'demo@cwf.local', 'passd': 'e981cad14d8fdde4be2f8439a61c27a7c7c1df5e'}
users = { 'admin': {'name': 'Admin', 'email': 'ad@cwf.local', 'passd': 'e4cc659f57a92b95d42916b539e03002b73f47c5'}, }

#Global Config Functions:

def createLog(client, path):
	""" Create a log object. """
	logFile = "{0}/logs/{1}.log".format(path, client)
	logObject = logging.getLogger(client)
	logObject.setLevel(logging.DEBUG)
	handlerERROR = logging.handlers.RotatingFileHandler(logFile, maxBytes=15769600, backupCount=18)
	logObject.addHandler(handlerERROR)
	return logObject


#Initialize Logs:
severLog = createLog('server', WEBPATH)
accessLog = createLog('access', WEBPATH)



def insertErrorLogLine(logErrorObject, logLine):
	""" Creates imcomplete line to a difined log. """
	try:
		logErrorObject.error(logLine)
	except:
		print("Unexpected insertErrorLogLine Fuction Error:", sys.exc_info()[0])
		pass


def jsonLogger(timestamp='', type='', msg='', data=[], action='', access=''):
	""" {"timestamp": "", "type": "", "msg": "", "data": "" "action": "", "access": ""} """
	res = {"timestamp": str(timestamp), "type": str(type), "msg": str(msg), "data": data, "action": str(action), "access": str(access)}
	res = json.dumps(res)
	return res


def sendMail(s, b, emailServer, logObject):
	""" sendMail("Subject", "ALERT: msg.\nMsg {0}".format(time.ctime())) """
	srv = emailServer
	msg = {}
	msg["Subject"] = s
	msg["From"] = eFrom
	msg["To"] = eTo
	msg["Cc"] = eCc
	body = b
	msg.attach(body)
	try:
		smtp = smtplib.SMTP(srv)
		smtp.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
		smtp.quit()
		logObject.info("{0}: Email sent. {1}".format(time.ctime(), msg["Subject"]))
	except:
		print('ERROR - Unable to send email')
		logObject.error("{0}: ERROR - Unable to send email alert. {1}".format(time.ctime(), msg["Subject"]))