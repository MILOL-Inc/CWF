import rocksdb
import sys


def createDB(db_file):
    """ create a database connection to a file database """
    db = []
    try:
        db = rocksdb.DB(db_file, rocksdb.Options(create_if_missing=True))
    except:
        print("Unexpected createDB Fuction Error:", sys.exc_info()[0])
    finally:
        if db:
            db.close()
        pass
    return db


def openDB(db_file):
    """ Open a database connection specified by db_file
    :param db_file database file
    :return: Connection object or None
    It assings a cache of 2.5G, uses a bloom filter for faster lookups and keeps more data (64 MB) in memory before writting a .sst file.
    """
    db = []
    opts = rocksdb.Options()
    opts.create_if_missing = True
    opts.max_open_files = 300000
    opts.write_buffer_size = 67108864
    opts.max_write_buffer_number = 3
    opts.target_file_size_base = 67108864
    opts.table_factory = rocksdb.BlockBasedTableFactory(
    filter_policy=rocksdb.BloomFilterPolicy(10),
    block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
    block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
    try:
        db = rocksdb.DB(db_file, opts)
    except:
        print("Unexpected openDB Fuction Error:", sys.exc_info()[0])
        pass
    return db


def insert(db, key, value):
    """ Insert a document
    :param conn: db object
    :param key: key string
    :param value: value string
    :return: True or False
    """
    res = []
    try:
        key = bytes(str(key), 'utf-8')
        value = bytes(str(value), 'utf-8')
        db.put(key, value)
        res = [0]
    except:
        print("Unexpected insert Fuction Error:", sys.exc_info()[0])
    return res


def update(db, key, value):
    """ Update a document
    :param conn: db object
    :param key: key string
    :param value: value string
    :return: True or False
    """
    res = []
    try:
        key = bytes(str(key), 'utf-8')
        value = bytes(str(value), 'utf-8')
        db.put(key, value)
        res = [0]
    except:
        print("Unexpected update Fuction Error:", sys.exc_info()[0])
    return res


def delete(db, key):
    """ Delete a document
    :param conn: db object
    :param key: String key value
    :return: True or False
    """
    res = []
    try:
        key = bytes(str(key), 'utf-8')
        db.delete(key)
        res = [0]
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
        it = db.iteritems()
        it.seek_to_first()
        for row in list(it):
            res.append(row)
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
        key = bytes(str(key), 'utf-8')
        res = (db.get(key)).decode('utf-8')
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
        it = db.iterkeys()
        it.seek_to_first()
        for i in list(it):
            i = i.decode('utf-8')
            res.append(i)
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
        it = db.itervalues()
        it.seek_to_first()
        for i in list(it):
            i = i.decode('utf-8')
            res.append(i)
    except:
        print("Unexpected selectValues Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectMany(db, *values):
    """
    Query multiple rows in the db instance
    :param db: db object
    :param *values: multiple values array
    :return: Dictionay values results
    """
    res = []
    bvalues = []
    try:
        for key in values:
            key = bytes(str(key), 'utf-8')
            bvalues.append(key)
    except:
        print("Unexpected selectMany Fuction Error:", sys.exc_info()[0])
        pass
    res = db.multi_get(bvalues)
    return res