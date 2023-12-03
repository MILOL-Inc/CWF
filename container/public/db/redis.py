import redis
import sys, datetime


def createDB(host='localhost', port=6379, db=0):
    """ create a database connection to a file database
    :return: Connection object or []
    """
    db = []
    try:
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        db = redis.Redis(connection_pool=pool)
        db.set('db-created', datetime.datetime.now().isoformat())
    except:
        print("Unexpected createDB Fuction Error:", sys.exc_info()[0])
        pass
    finally:
        db.close()
    return db


def openDB(host='localhost', port=6379, db=0):
    """ Open a database connection
    :param db_file database file
    :return: Connection object or []
    """
    db = []
    try:
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        db = redis.Redis(connection_pool=pool)
    except:
        print("Unexpected openDB Fuction Error:", sys.exc_info()[0])
        pass
    return db


def insert(db, key, value):
    """ Insert a document
    :param conn: db object
    :param key: key string
    :param value: value string | dictionary
    :return: res: [] or result
    """
    res = []
    try:
        key = str(key)
        value = str(value)
        res = db.set(key, value)
    except:
        print("Unexpected insert Fuction Error:", sys.exc_info()[0])
    return res


def update(db, key, value):
    """ Update a document
    :param conn: db object
    :param key: key string
    :param value: value string | dictionary
    :return: res: [] or result
    """
    res = []
    try:
        key = str(key)
        value = str(value)
        res = db.set(key, value)
    except:
        print("Unexpected update Fuction Error:", sys.exc_info()[0])
    return res


def delete(db, key):
    """ Delete a document
    :param conn: db object
    :param key: String key value
    :return: res: [] or result
    """
    res = []
    try:
        key = str(key)
        res = db.delete(key)
    except:
        print("Unexpected delete Fuction Error:", sys.exc_info()[0])
    return res


def selectAll(db):
    """
    Query all rows in the db instance
    :param db: db object
    :return: res array results
    """
    res = []
    try:
        for key in db.scan_iter("*"):
            res.append(key, db.get(key))
    except:
        print("Unexpected selectAll Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectOne(db, key):
    """
    Query all rows in the db instance
    :param db: db object
    :param key: index ID
    :return: res string result
    """
    res = []
    try:
        key = str(key)
        res = db.get(key)
    except:
        print("Unexpected selectOne Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectKeys(db):
    """
    Query all rows in the db instance
    :param db: db object
    :return: res array key results
    """
    res = []
    try:
        res = list(db.scan_iter("*"))
    except:
        print("Unexpected selectKeys Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectValues(db):
    """
    Query all rows in the db instance
    :param db: db object
    :return: res array values results
    """
    res = []
    try:
        list = list(db.scan_iter("*"))
        for key in db.scan_iter("*"):
            res.append(db.get(key))
    except:
        print("Unexpected selectValues Fuction Error:", sys.exc_info()[0])
        pass
    return res


def select(db, *values):
    """
    Query multiple rows in the db instance
    :param db: db object
    :param *values: multiple values array
    :return: Dictionay values results
    """
    res = []
    try:
        res = db.mget(values)
    except:
        print("Unexpected selectMany Fuction Error:", sys.exc_info()[0])
        pass
    return res