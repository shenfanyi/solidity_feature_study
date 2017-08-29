#!/usr/bin/env python2
# -*- coding: UTF-8 -*-



# ----- import -----
import urllib2
import re
import urlparse
from bs4 import BeautifulSoup
import logging
from socket import error as SocketError
import errno
import time



## ----- log -----
# create logger
logger_name = "spider_logger"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
log_path = "./spider_log.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)



## ------ function -----
def get_code_urls(source_url):

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(source_url, headers=hdr)
        # request = urllib2.Request(source_url)

        response = urllib2.urlopen(request)
        # print response.getcode()

    except urllib2.HTTPError, e:
        logger.error('get_code_urls: urllib2.HTTPError: %s\n' % (e.code))
        return 2

    except urllib2.URLError, e:
        logger.error('get_code_urls: urllib2.URLError: %s\n' % (e.reason))
        return 2

    except Exception as e:
        logger.error('get_code_urls: open exception: %s\n' %e)
        return 2

    except SocketError as e:
        if e.errno == errno.ECONNRESET:
            time.sleep(0.5)
            logger.error('get_code_urls: SocketError ECONNRESET: %s\n' % e)
            return 2

    else:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
        # print soup1.prettify()

        links = soup.find_all('a', href=re.compile(r"/address/(\w|\d)*"))
        urls = list()
        for link in links:
            url = link['href']
            urls.append(url)
        urls = urls[:-2]

        code_urls = list()
        for i in urls:
            code_url = urlparse.urljoin('https://etherscan.io/address/', i)
            code_url = urlparse.urljoin(code_url, '#code')
            code_urls.append(code_url)
        # print code_urls

        return code_urls

# #test
# if __name__ == "__main__":
#     print get_code_urls('https://etherscan.io/accounts/c')
#     # print get_code_urls('accounts/c')
#     # print get_code_urls('https://aaaaaaaa')



def get_codes(code_url):

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    try:
        request = urllib2.Request(code_url, headers=hdr)
        response = urllib2.urlopen(request)

    except urllib2.HTTPError, e:
        logger.error('get_codes: urllib2.HTTPError: %s\n' % (e.code))
        return 2

    except urllib2.URLError, e:
        logger.error('get_codes: urllib2.URLError: %s\n' % (e.reason))
        return 2

    except Exception as e:
        logger.error('get_codes: open exception: %s\n' %e)
        return 2

    except SocketError as e:
        if e.errno == errno.ECONNRESET:
            time.sleep(0.5)
            logger.error('get_codes: SocketError ECONNRESET: %s\n' % e)
            return 2

    else:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')


        num43_sol_code = soup.find_all('pre', class_="js-sourcecopyarea", id="editor")
        num43_abi_code = soup.find_all('pre', class_="wordwrap", id="js-copytextarea2")
        num43_byte_code = soup.find_all('div', id="verifiedbytecode2")
        num4_bzzr = soup.find_all('pre', class_="wordwrap", style="margin-top: 5px; max-height: 100px")
        num21_byte_code = soup.find_all('pre', class_="wordwrap", style="height: 15pc;")
        num2_abi_code = soup.find_all('pre', class_="wordwrap", style = "height: 12pc;")

        def droptag(text):
            if text == []:
                return []
            else:
                soup = BeautifulSoup(str(text[0]), 'html.parser', from_encoding='utf-8')
                res = soup.get_text()
                return res

        num43_sol_code = droptag(num43_sol_code)
        num43_abi_code = droptag(num43_abi_code)
        num43_byte_code = droptag(num43_byte_code)
        num4_bzzr = droptag(num4_bzzr)
        num21_byte_code = droptag(num21_byte_code)
        num2_abi_code = droptag(num2_abi_code)


        if num4_bzzr != []:
            res = {'sol_code': num43_sol_code, 'abi_code':num43_abi_code, 'byte_code':num43_byte_code, 'bzzr':num4_bzzr}
        else:
            if num2_abi_code != []:
                res = {'abi_code':num2_abi_code, 'byte_code':num21_byte_code}
            else:
                if num21_byte_code != []:
                    res = {'byte_code':num21_byte_code}
                elif num43_sol_code!= [] and num43_abi_code!= [] and num43_byte_code!= []:
                    res = {'sol_code': num43_sol_code, 'abi_code':num43_abi_code, 'byte_code':num43_byte_code}
                else:
                    res = []

        return res


# #test
# print get_codes('https://etherscan.io/address/0xab7c74abc0c4d48d1bdad5dcb26153fc8780f83e#code')

# # test: the below url does not have sol&abi codes
# print get_codes('https://etherscan.io/address/0xba2ed0d772e0ca1f72368e7a610e42397e960946#code')