import os, sys, shutil, random
import public.config as config
import public.library.core as libs

PATH = config.WEBPATH
VERSION = config.VERSION
APP_LIST = config.apps
EXEC = config.EXEC

#Get application arguments
arg = sys.argv


def runRoutines():
    """ Run all enabled routines applications
        To test apps in the terminal use:
        pid = libs.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app, EXEC)) """
    res = True
    try:
        for app in APP_LIST:
            if APP_LIST[app]['status'] == True:
                pid = libs.runOS('{2} {0}/apps/{1}/{1}.py'.format(PATH, app, EXEC))
                print(APP_LIST[app]['name'], 'running on port:', APP_LIST[app]['port'], 'pid:', pid)
    except:
        print("Unexpected runRoutines Fuction Error:", sys.exc_info()[0])
        res = False
        pass
    return True


def runApps():
    """ Run all enabled user apps.
    To test apps in the terminal use:
    pid = libs.core.runOS('{2} {0}/routines/{1}/{1}.py'.format(PATH, app, EXEC)) """
    print(VERSION)
    res = True
    try:
        for app in APP_LIST:
            if APP_LIST[app]['status'] == True:
                pid = libs.runOS('{2} {0}/apps/{1}/{1}.py'.format(PATH, app, EXEC))
                print(APP_LIST[app]['name'], 'running on port:', APP_LIST[app]['port'], 'pid:', pid)
    except:
        print("Unexpected runApps Fuction Error:", sys.exc_info()[0])
        res = False
        pass
    return True


def createApp():
    """ Create application function. """
    appName = 'app_{0}'.format(random.randint(0, 99))
    try:
        appName = str(arg[2]).replace(' ', '')
    except:
        pass
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
            f.write("PORT = '{0}'".format(config.DEFAULT_PORT))
            f.write("\n")
            f.write("COOKIE_SECRET = '{0}'".format(config.COOKIE_SECRET))
    except FileNotFoundError:
        print("Unexpected runApps Fuction Error:", sys.exc_info()[0])
    print('{0} application created.'.format(appName))


def showVersion():
    """ Show application version. """
    print(VERSION)


def showHelp():
    print(VERSION)
    print("$ runserver -v | Show version number.")
    print("$ runserver -h | Shows Help Menu.")
    print("$ runserver --apps | Runs enabled apps.")
    print("$ runserver --routines | Runs enabled routines.")
    print("$ runserver --create 'myapp' | Creates app files.")


def defaultAction():
    libs.core.exitAction()


def optionCheck():
    op = str(arg[1])
    {
        '-v': None,
        '-h': showHelp,
        '--apps': runApps,
        '--routines': runRoutines,
        '--create': createApp
    }.get(op, defaultAction)()


if __name__ == "__main__":
    {1: showHelp, 2: optionCheck, 3: optionCheck}.get(len(arg), defaultAction)()
