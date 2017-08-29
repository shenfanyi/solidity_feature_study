#!/usr/bin/python
# -*- coding:utf-8 -*-


from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI
COLL_BYTE = DB_SOLCODE.COLL_BYTE


@app.route('/<search_cont>')

def search(search_cont):
    cursor = COLL_SOL.find(
        {'$text': {'$search': search_cont}}
    )

    res = list()
    for doc in cursor:
        res.append(doc)

    # return str(len(res))
    return str(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

