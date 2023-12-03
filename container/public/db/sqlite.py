import sqlite3
from sqlite3 import Error


def createDB(db_file):
    """ create a database connection to a SQLite database
    :memory: RAM database 
    :return: Connection object or Empty array
    """
    conn = []
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        pass
    return conn


def createIndex(conn, table, index):
    idx = 'idx_{0}_{1}'.format(table, index)
    sql = 'CREATE UNIQUE INDEX {0} ON {1} ({2})'.format(idx, table, index)
    res = []
    try:
        c = conn.cursor()
        c.execute(sql)
        res.append(0) 
    except Error as e:
        print(e)
        pass
    return res


def openDB(db_file):
    """ Open a database connection from specified by db_file
    :param db_file database file
    :param :memory: RAM database
    :return: Connection object or Empty array
    """
    conn = []
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        pass
    return conn


def closeDB(conn):
    """ Close a database connection from specified openned connection.
    :return: Connection object or Empty array
    """
    try:
        conn.close()
        return True
    except Error as e:
        print(e)
        return False


def executeRaw(conn, sql):
    """ Execute raw SQL statements
    :param conn: Connection object
    :param sql: SQL raw string
    :return: None | True
    """
    res = []
    try:
        c = conn.cursor()
        c.execute(str(sql))
        res.append(0) 
    except Error as e:
        print(e)
        pass
    return res


def selectRaw(conn, sql):
    """ Execute raw SQL statements
    :param conn: Connection object
    :param sql: SQL raw string
    :return: Array results
    """
    res = []
    try:
        c = conn.cursor()
        c.execute(str(sql))
        res = c.fetchall()
    except Error as e:
        print(e)
        pass
    return res


def insert(conn, table, values):
    """
    Insert values from document into a predefined table
    :param conn: Connection object
    :param table: String
    :param values: Python list: ('value1', 'value2', 'value3')
    :return: Array lastrowid or Empty array
    """
    res = []
    try:
        sql = """INSERT INTO {0} VALUES {1}""".format(table, values)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        res.append(cur.lastrowid)
    except Error as e:
        print(e)
        pass
    return res


def update(conn, table, key, values, id):
    """
    update document
    :param conn: Connection object
    :param table: String
    :param key: String
    :param values: Integer/String
    :param id: Int (index_id)
    :return: Array results
    """
    res = []
    try:
        sql = """UPDATE {0}
              SET {1} = '{2}'
              WHERE rowid = '{3}'""".format(table, key, values, id)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        res.append(id)
    except Error as e:
        print(e)
        pass
    return res


def delete(conn, table, id):
    """
    delete document
    :param conn: Connection object
    :param table: String
    :param id: Int (index_id)
    :return: Array results
    """
    res = []
    try:
        sql = """DELETE FROM {0} WHERE rowid = '{1}'""".format(table, id)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        res.append(id)
    except Error as e:
        print(e)
        pass
    return res


def selectAll(conn, table):
    """
    Query all rows in the document
    :param conn: Connection object
    :param table: String
    :return: Array results
    """
    res = []
    try:
        cur = conn.cursor()
        sql = '''SELECT * FROM {0}'''.format(table)
        cur.execute(sql)
        res = cur.fetchall()
    except Error as e:
        print(e)
        pass
    return res


def selectOne(conn, table, id):
    """
    Query all rows in the document
    :param conn: the Connection object
    :param table: String
    :param id: Integer
    :return: Array results
    """
    res = []
    try:
        cur = conn.cursor()
        sql = """SELECT * FROM {0} WHERE rowid = '{1}'""".format(table, id)
        cur.execute(sql)
        res = cur.fetchall()
    except Error as e:
        print(e)
        pass
    return res


def select(conn, table, key, value):
    """
    Query all rows in the document
    :param conn: the Connection object
    :param table: String
    :param key: String
    :param value: Integer/String
    :return: Array results
    """
    res = []
    try:
        cur = conn.cursor()
        sql = """SELECT * FROM {0} WHERE {1} = '{2}'""".format(table, key, value)
        cur.execute(sql)
        res = cur.fetchall()
    except Error as e:
        print(e)
        pass
    return res

