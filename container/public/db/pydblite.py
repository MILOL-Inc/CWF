from winreg import REG_NOTIFY_CHANGE_ATTRIBUTES
from pydblite import Base
import sys


def createDB(db_file):
    """ create a database connection to a file database
    :return: Connection object or None
    """
    db = []
    try:
        db = Base(db_file)
    except:
        print("Unexpected createDB Fuction Error:", sys.exc_info()[0])
        pass
    return db


def createIndex(db, index):
    res = []
    res = db.create_index(index)
    return res


def openDB(db):
    """ Open a database connection specified by db_file
    :param db: database object
    :return: Connection object or Empty array
    """
    res = []
    try:
        if db.exists():
            res = db.open()
    except:
        print("Unexpected openDB Fuction Error:", sys.exc_info()[0])
        pass
    return res


def createDoc(db, keys):
    """ Create document key schema to a file database
    :param db database instance
    :param values: Comma separated list: ('value1', 'value2', 'value3')
    :return: Array results or Empty array
    """
    res = []
    try:
        res = db.create(*keys)
    except:
        print("Unexpected createDoc Fuction Error:", sys.exc_info()[0])
        pass
    return res


def insert(db, values):
    """ Insert a document
    :param conn: db object
    :param values: Comma separated list: ('value1', 'value2', 'value3')
    :return: Array results or Empty array
    """
    res = []
    try:
        res = db.insert(*values)
        db.commit()
    except:
        print("Unexpected insert Fuction Error:", sys.exc_info()[0])
        pass
    return res


def update(db, record, **key_value):
    return None


def delete(db, record):
    """ Delete a document
    :param conn: db object
    :param record: Dictionary record: db[id] or db(name='value')
    :return: Array results or Empty array
    """
    res = []
    try:
        res = db.delete(record)
        db.commit()
    except:
        print("Unexpected delete Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectAll(db):
    """
    Query all rows in the db instance
    :param db: db object
    :return: Array results or Empty array
    """
    res = []
    for row in db:
        res.append(row)
    return res


def selectOne(db, id):
    """
    Query all rows in the db instance
    :param db: db object
    :param value: index ID
    :return: Array results or Empty array
    """
    res = []
    if db[id]:
        res = db[id]
    return res


def select(db, key, value):
    """
    Query all rows in the db instance
    :param db: db object
    :param key: key string
    :param value: index ID
    :return: Array results or Empty array
    """
    res = []
    for row in (db(key) == value):
        res.append(row)
    return res