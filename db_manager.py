#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)

DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI
COLL_BYTE = DB_SOLCODE.COLL_BYTE


# DB_SOLCODE.COLL_URL.create_index([('id', pymongo.ASCENDING)],unique=True)
# DB_SOLCODE.COLL_SOL.create_index([('id', pymongo.ASCENDING)],unique=True)
# DB_SOLCODE.COLL_ABI.create_index([('id', pymongo.ASCENDING)],unique=True)


# DB_SOLCODE.COLL_URL.drop_index('id_1')
# DB_SOLCODE.COLL_URL.drop_index('id_-1')


# for index in DB_SOLCODE.COLL_URL.list_indexes():
#     print(index)


# DB_SOLCODE.COLL_URL.remove({})
# DB_SOLCODE.COLL_SOL.remove({})
# DB_SOLCODE.COLL_ABI.remove({})


# for i in COLL_URL.find({"id": 5}):
for i in COLL_URL.find():
    pprint.pprint(i)

# for i in COLL_SOL.find({"id": 5}):
#     pprint.pprint(i)
#
# for i in COLL_ABI.find({"id": 5}):
#     pprint.pprint(i)


# pprint.pprint(COLL_URL.find_one())
# pprint.pprint(COLL_SOL.find_one())
# pprint.pprint(COLL_ABI.find_one())


print DB_SOLCODE.COLL_URL.count()
print DB_SOLCODE.COLL_SOL.count()
print DB_SOLCODE.COLL_ABI.count()
print DB_SOLCODE.COLL_BYTE.count()




