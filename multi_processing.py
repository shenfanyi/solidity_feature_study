#!/usr/bin/env python2
# -*- coding: UTF-8 -*-



from spider import get_source_urls
from spider import get_code_urls
from spider import get_codes

import multiprocessing
import time
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
DB_SOLCODE = client.DB_SOLCODE

COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI



def main(n_pages):

    start = time.time()

    source_urls = get_source_urls(n_pages)
    # print source_urls

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # pool = multiprocessing.Pool(3)
    code_urls = pool.map(get_code_urls, source_urls)
    pool.close()
    pool.join()
    # print len(code_urls[0])
    # print code_urls[0]

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # codes = list()
    db_id = 0
    for i in code_urls:

        ## test: n is to limit the number of code_urls from a source_url
        # n = 0

        for code_url in i:

            db_id += 1

            try:
                code = pool.apply_async(get_codes, (code_url,))
                # print len(code.get())
                # codes.append(code)
                sol_code = code.get()['sol_code']
                abi_code = code.get()['abi_code']
            except IndexError:
                continue
            # break

            # db_id += 1
            COLL_URL.insert_one(
                {
                    'id':db_id,
                    'url':code_url
                }
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


            # n += 1
            # if n == 10:
            #     break

    pool.close()
    pool.join()
    # print len(codes)
    # print codes[0].get()

    elapsed = (time.time() - start)
    print("Time used:", elapsed)



if __name__ == "__main__":
    n_pages = 3
    main(n_pages)