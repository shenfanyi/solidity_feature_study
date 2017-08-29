#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


import urllib2
import re
import urlparse
from bs4 import BeautifulSoup


# class GETCODE():
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


# print len(get_codes('https://etherscan.io/address/0x4f60d5605b4ceb8db307024eb5481af8e90ccfc7#code'))
res = get_codes('https://etherscan.io/address/0xd0a6e6c54dbc68db5db3a091b171a77407ff7ccf#code')
# print len(str(res['byte_code'])
res = res['byte_code']
# fo = open('a.txt','w')
# fo.write(res)
# fo.close()





# https://etherscan.io/address/0x66e32d375642ce9c8202caea1f6a83b0c3caf32c#code
# <pre class="js-sourcecopyarea" id="editor" style="height: 330px; max-height: 450px; margin-top: 5px;">
# <pre class="wordwrap" id="js-copytextarea2" style="height: 200px; max-height: 400px; margin-top: 5px;">
# < div id = "verifiedbytecode2" >
# < pre class ="wordwrap" style="margin-top: 5px; max-height: 100px" >
#
#
# https: // etherscan.io / address / 0xbd56f550212e27dcfe090d64435e1b4e20e1b31f  # code
# < pre class ="js-sourcecopyarea" id="editor" style="height: 330px; max-height: 450px; margin-top: 5px;" >
# < pre class ="wordwrap" id="js-copytextarea2" style="height: 200px; max-height: 400px; margin-top: 5px;" >
# < div id = "verifiedbytecode2" >
#
#
# https://etherscan.io/address/0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae#code
# byte:<pre class="wordwrap" style="height: 15pc;">
# abi:< pre class ="wordwrap" style="height: 12pc;" >
#
#
# https: // etherscan.io / address / 0xd2db25fde17c0a3a67538e22bb2bb28c57b2327f  # code
# byte:<pre class="wordwrap" style="height: 15pc;">



# https://etherscan.io/address/0xd0a6e6c54dbc68db5db3a091b171a77407ff7ccf#code


