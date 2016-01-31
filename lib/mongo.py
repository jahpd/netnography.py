from pymongo import MongoClient

def connect(db, col):
    print "=> Starting mongodb://localhost:27017/"
    print "   %s" % db
    print "   %s" % col
    #client = MongoClient('mongodb://localhost:27017/')
   # _db = client[db]
   # return _db[col]
