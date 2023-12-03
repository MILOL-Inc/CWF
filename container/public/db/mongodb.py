import pymongo
from pymongo import MongoClient
import sys, datetime


def createDB(db_name='mongodb', host='localhost', port=27017):
    """ Open a database connection specified by db_file
    :param db_name: String | Default: 'mongodb'
    :param host: String | Default: 'localhost'
    :param port: Integer | Default: 27017
    :return: (db, client) object or []
    """
    db = []
    try:
        client = client = MongoClient('{0}:{1}'.format(host, port))
        db = client[db_name]
        logs = db['logs']
        logs.insert_one({
            'log': 'Database {0} created.'.format(db_name),
            'isotimestamp': datetime.datetime.now().isoformat(),
        })
    except:
        print("Unexpected createDB Fuction Error:", sys.exc_info()[0])
        pass
    finally:
        client.close()
    return (db, client)


def openDB(db_name='mongodb', host='localhost', port=27017):
    """ Open a database connection specified by db_file
    :param db_name: String | Default: 'mongodb'
    :param host: String | Default: 'localhost'
    :param port: Integer | Default: 27017
    :return: db object or []
    """
    db = []
    try:
        client = client = MongoClient('{0}:{1}'.format(host, port))
        db = client[db_name]
    except:
        print("Unexpected openDB Fuction Error:", sys.exc_info()[0])
        pass
    return db


def createIndex(db, db_collection, key, unique=True, sorted=0):
    """ Create an index
    :param db: db object
    :param db_collection: String
     :param sorted: Integer flag: 0: ASCENDING | 1: DESCENDING
    :param key: Array of index names as strings
    :return: res object or []
    """
    res = []
    indexes = []
    for i in key:
        if sorted == 0: indexes.append((i, pymongo.ASCENDING))
        if sorted == 1: indexes.append((i, pymongo.DESCENDING))
    try:
        collection = db[db_collection]
        res = collection.create_index(indexes, unique=unique)
    except:
        print("Unexpected createIndex Fuction Error:", sys.exc_info()[0])
        pass
    return res


def dropIndex(db, db_collection, index_name):
    """ Create an index
    :param db: db object
    :param db_collection: String
    :param index_name: String
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.drop_index(str(index_name))
    except:
        print("Unexpected dropIndex Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectIndexes(db, db_collection):
    """ Create an index
    :param db: db object
    :param db_collection: String
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = list(collection.index_information())
    except:
        print("Unexpected selectIndexes Fuction Error:", sys.exc_info()[0])
        pass
    return res


def insert(db, db_collection, document):
    """ Insert a document
    :param db: db object
    :param db_collection: String
    :param document: Document dictionary
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.insert_one(document).inserted_id
    except:
        print("Unexpected insert Fuction Error:", sys.exc_info()[0])
        pass
    return res


def insertMany(db, db_collection, array_document):
    """ Insert multiple documents
    :param db: db object
    :param db_collection: String
    :param array_document: Document dictionary array
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.insert_many(array_document).inserted_ids
    except:
        print("Unexpected insertMany Fuction Error:", sys.exc_info()[0])
        pass
    return res


def update(db, db_collection, key, document):
    """ Update a document
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :param document: Document dictionary
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.update_one( key, { "$set": document } )
    except:
        print("Unexpected update Fuction Error:", sys.exc_info()[0])
        pass
    return res


def updateMany(db, db_collection, key, document):
    """ Update one or multiple documents
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :param document: Document dictionary
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.update_many( key, { "$set": document } )
    except:
        print("Unexpected update Fuction Error:", sys.exc_info()[0])
        pass
    return res


def delete(db, db_collection, key):
    """ Delete a document
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :param document: Document dictionary
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.delete_one(key)
    except:
        print("Unexpected delete Fuction Error:", sys.exc_info()[0])
        pass
    return res


def deleteMany(db, db_collection, key):
    """ Delete one or more documents
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :param document: Document dictionary
    :return: res object or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.delete_many(key)
    except:
        print("Unexpected deleteMany Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectAll(db, db_collection):
    """ Return all documents in a collection
    :param db: db object
    :param db_collection: String
    :return: res list or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = list(collection.find({}))
    except:
        print("Unexpected selectAll Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectOne(db, db_collection, key):
    """ Query a single row in a collection
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :return: res document or []
    Use {'_id': object_id} to query by ObjectId
    """
    res = []
    try:
        collection = db[db_collection]
        res = [collection.find_one(key)]
    except:
        print("Unexpected selectOne Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectObjectId(db, db_collection, key):
    """ Return an ObjectId in a collection
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :return: res document or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = [collection.find_one(key)['_id']]
    except:
        print("Unexpected selectObjectId Fuction Error:", sys.exc_info()[0])
        pass
    return res


def select(db, db_collection, key):
    """ Query single or multiple rows in a collection
    :param db: db object
    :param db_collection: String
    :param key: key dictionary
    :return: res document or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = list(collection.find(key))
    except:
        print("Unexpected select Fuction Error:", sys.exc_info()[0])
        pass
    return res


def selectAggregate(db, db_collection, aggregate_document):
    """ Query multiple rows in a collection
    :param db: db object
    :param db_collection: String
    :param aggregate_document: Aggregate document array
    [ { "$match": { "..": { "$gt": "..." } }}, { "$group": { "_id": "$...", "...": { "$sum": "$..." } }} ]
    :return: res document or []
    """
    res = []
    try:
        collection = db[db_collection]
        res = list(collection.aggregate(aggregate_document))
    except:
        print("Unexpected selectAggregate Fuction Error:", sys.exc_info()[0])
        pass
    return res


def getCount(db, db_collection, key={}):
    """ Return a total count of documents in a collection
    :param db: db object
    :param db_collection: String
    :param key: Optional key dictionary
    :return: Count total or []
    Use {'_id': 'document_id'} to query by ObjectId
    """
    res = []
    try:
        collection = db[db_collection]
        res = collection.count_documents(key)
    except:
        print("Unexpected count Fuction Error:", sys.exc_info()[0])
        pass
    return res