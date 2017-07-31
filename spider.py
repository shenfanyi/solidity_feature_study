#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


import urllib2
import re
import urlparse
from bs4 import BeautifulSoup



def get_source_urls(n_pages):
    # 1< n_pages < 400

    source_urls = list()
    n_pages += 1
    for i in range(1, n_pages):
        source_url = urlparse.urljoin('https://etherscan.io/accounts/c/', str(i))
        source_urls.append(source_url)

    return source_urls

# #test
# print get_source_urls(5)



def get_code_urls(source_url):

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    request = urllib2.Request(source_url, headers=hdr)
    response = urllib2.urlopen(request)
    # print response.getcode()

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
# print get_code_urls('https://etherscan.io/accounts/c')



def get_codes(code_url):

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    request = urllib2.Request(code_url, headers=hdr)
    response = urllib2.urlopen(request)
    # print response.getcode()

    html_doc = response.read()
    soup1 = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')

    sol_code = soup1.find_all('pre', id="editor")
    # print str(sol_code[0])
    soup2 = BeautifulSoup(str(sol_code[0]), 'html.parser', from_encoding='utf-8')
    sol_code = soup2.get_text()

    abi_code = soup1.find_all('pre', id="js-copytextarea2")
    # print str(abi_code[0])
    soup3 = BeautifulSoup(str(abi_code[0]), 'html.parser', from_encoding='utf-8')
    abi_code = soup3.get_text()

    return {'sol_code':sol_code, 'abi_code':abi_code}

# #test
# print get_codes('https://etherscan.io/address/0xab7c74abc0c4d48d1bdad5dcb26153fc8780f83e#code')

# # test: the below url does not have sol&abi codes
# print get_codes('https://etherscan.io/address/0xba2ed0d772e0ca1f72368e7a610e42397e960946#code')