#!/usr/bin/env python2
# -*- coding: UTF-8 -*-



from spider import get_source_urls
from spider import get_code_urls
from spider import get_codes

import multiprocessing
import time
import pymongo
from pymongo import MongoClient

import logging



# create logger
logger_name = "logger"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
log_path = "./log.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)



client = MongoClient('localhost', 27017)
DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI



def get_max_id():
    for i in COLL_URL.find().sort([("id", -1)]).limit(1):
        return i['id']
# print get_max_id()


def multiprocessing_get_code_urls(source_urls):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # pool = multiprocessing.Pool(3)
    code_urls = pool.map(get_code_urls, source_urls)
    pool.close()
    pool.join()
    return code_urls


def url_to_urltail(url):
    urltail = url.split('/')[-1].split('#')[0]
    return urltail
# print url_to_urltail('https://etherscan.io/address/0x4f60d5605b4ceb8db307024eb5481af8e90ccfc7#code')



def main(n_pages):

    source_urls = get_source_urls(n_pages)
    code_urls = multiprocessing_get_code_urls(source_urls)

    db_id = get_max_id() + 1
    page_num = 1

    for i in code_urls:

        for code_url in i:

            if code_url == 2:
                continue

            else:
                try:
                    code = get_codes(code_url)
                    if code == 2:
                        continue
                    else:
                        sol_code = code['sol_code']
                        abi_code = code['abi_code']
                except IndexError:
                    logger.error('IndexError, code_url is unvailable!')
                    continue

                try:
                    COLL_URL.insert_one(
                        {
                            'id':0,
                            'url':url_to_urltail(code_url)
                        }
                    )
                except Exception as e:
                    logger.error('open exception: %s: %s\n' %(code_url, e))
                    continue

                COLL_URL.update_one(
                    {'id':0},
                    {'$set': {'id': db_id}}
                )

                COLL_SOL.insert_one(
                    {
                        'id': db_id,
                        'SOLCODE': sol_code
                    }
                )

                COLL_ABI.insert_one(
                    {
                        'id': db_id,
                        'ABICODE': abi_code
                    }
                )

                db_id += 1

        logger.info('page %d finished' %(page_num))
        page_num += 1


if __name__ == "__main__":
    start = time.time()
    logger.info('begin')

    n_pages = 100
    main(n_pages)

    logger.info('end')
    elapsed = (time.time() - start)
    logger.info("Time used:", elapsed)
    print("Time used:", elapsed)
