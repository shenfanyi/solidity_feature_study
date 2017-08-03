#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)

DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI
COLL_BYTE = DB_SOLCODE.COLL_BYTE


# COLL_URL.insert_one(
#                     {
#                         'id':5.0,
#                         'url':'w'
#                     }
#                 )

# id = 1
# for i in ['z','a','o']:
#     id += 1
#     try:
#         COLL_URL.insert_one(
#             {
#                 'id': 0,
#                 'url': i
#             }
#         )
#     except:
#         continue
#
    # for n in range(10000000):
    #     try:
    #         COLL_URL.update_one(
    #                 {'id':0},
    #                 {'$set': {'id': id}}
    #                             )
    #     except :
    #         id += 1
    #         continue
    #     else:
    #         break

    #
    # COLL_URL.update_one(
    #             {'id':1},
    #             {'$set': {'id': 2}}
    #                     )

# except pymongo.errors.DuplicateKeyError:
#     continue


# DB_SOLCODE.COLL_URL.create_index([('id', pymongo.ASCENDING)],unique=True)
# DB_SOLCODE.COLL_URL.create_index([('url', pymongo.TEXT)],unique=True)
# DB_SOLCODE.COLL_SOL.create_index([('id', pymongo.ASCENDING)],unique=True)
# DB_SOLCODE.COLL_ABI.create_index([('id', pymongo.ASCENDING)],unique=True)


# DB_SOLCODE.COLL_URL.drop_index('id_1')
# DB_SOLCODE.COLL_URL.drop_index('id_1_url_text')


# print DB_SOLCODE.COLL_URL.index_information()


############ DB_SOLCODE.COLL_URL.remove({})
############ DB_SOLCODE.COLL_SOL.remove({})
############ DB_SOLCODE.COLL_ABI.remove({})


# for i in COLL_URL.find().sort([("id",-1)]).limit(1):
#     print i['id']

for i in COLL_URL.find({"id": 555}):
# for i in COLL_URL.find():
    pprint.pprint(i)

for i in COLL_SOL.find({"id": 555}):
    pprint.pprint(i)

for i in COLL_ABI.find({"id": 555}):
    pprint.pprint(i)


# pprint.pprint(COLL_URL.find_one())
# pprint.pprint(COLL_SOL.find_one())
# pprint.pprint(COLL_ABI.find_one())


print DB_SOLCODE.COLL_URL.count()
print DB_SOLCODE.COLL_SOL.count()
print DB_SOLCODE.COLL_ABI.count()
print DB_SOLCODE.COLL_BYTE.count()




