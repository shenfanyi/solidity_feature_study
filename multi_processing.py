#!/usr/bin/env python2
# -*- coding: UTF-8 -*-



# ----- import -----
from spider import get_code_urls
from spider import get_codes

import multiprocessing
import time
import re
import urlparse

from pymongo import MongoClient

import logging



## ----- log -----
## create logger
logger_name = "logger"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

## create file handler
log_path = "./log.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

## create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

## add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)



## ----- mongodb ------
client = MongoClient('localhost', 27017)
DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI
COLL_BYTE = DB_SOLCODE.COLL_BYTE
COLL_BZZR = DB_SOLCODE.COLL_BZZR
COLL_CHECK = DB_SOLCODE.COLL_CHECK



## ------ function -----
def get_max_id():
    for i in COLL_URL.find().sort([("id", -1)]).limit(1):
        return i['id']
# print get_max_id()


def get_source_urls(begin_page,end_page):
    ## begin_page >=1, end_page <= 400
    source_urls = list()
    end_page += 1
    for i in range(begin_page,end_page):
        source_url = urlparse.urljoin('https://etherscan.io/accounts/c/', str(i))
        source_urls.append(source_url)
    return source_urls
# print get_source_urls(1,5)


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



def main(begin_page,end_page):

    source_urls = get_source_urls(begin_page,end_page)
    code_urls = multiprocessing_get_code_urls(source_urls)

    try:
        db_id = get_max_id() + 1
    except TypeError:
        db_id = 1

    page_num = begin_page

    for i in code_urls:

        for code_url in i:

            if code_url == 2:
                continue

            else:
                code = get_codes(code_url)

                if code == 2:
                    continue
                elif len(code) == 4:
                    num = 4
                elif len(code) == 3:
                    num = 3
                elif len(code) == 2:
                    num = 2
                elif len(code) == 1:
                    num = 1
                elif len(code) == 0:
                    continue


                try:
                    COLL_URL.insert_one(
                        {
                            'id':0,
                            'url':url_to_urltail(code_url)
                        }
                    )
                except Exception as e:
                    logger.error('open exception: %s: %s' %(code_url, e))
                    continue

                COLL_URL.update_one(
                    {'id':0},
                    {'$set': {'id': db_id}}
                )

                COLL_BYTE.insert_one(
                    {
                        'id': db_id,
                        'BYTECODE': code['byte_code']
                    }
                )


                if num >= 2:
                    COLL_ABI.insert_one(
                        {
                            'id': db_id,
                            'ABICODE': code['abi_code']
                        }
                    )

                    if num >= 3:
                        COLL_SOL.insert_one(
                            {
                                'id': db_id,
                                'SOLCODE': code['sol_code']
                            }
                        )

                        if num == 4:
                            COLL_BZZR.insert_one(
                                {
                                    'id': db_id,
                                    'BZZR': code['bzzr']
                                }
                            )

                db_id += 1

        logger.info('page %d finished' %(page_num))
        page_num += 1



## ----- main ------
if __name__ == "__main__":
    start = time.time()
    logger.info('---------------------------------------')
    logger.info('crawling starts')

    begin_page = 351
    end_page = 375
    main(begin_page,end_page)

    logger.info('crawling ends')
    elapsed = (time.time() - start)
    logger.info("Time used:{}".format(elapsed))
    logger.info('---------------------------------------\n')
    print("Time used:", elapsed)
