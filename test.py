#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


import unittest
from spider import get_source_urls
from spider import get_code_urls
from spider import get_codes


class TestDict(unittest.TestCase):

    def setUp(self):
        self.source_url = 'https://etherscan.io/accounts/c'
        self.code_url = 'https://etherscan.io/address/0xab7c74abc0c4d48d1bdad5dcb26153fc8780f83e#code'
        print 'setUp...'

    def tearDown(self):
        print 'tearDown...'

    def test_get_source_urls(self):
        self.assertEqual(len(get_source_urls(5)), 5, 'test get_source_urls fail')

    # def test_get_code_urls(self):
    #     self.assertEqual(len(get_code_urls(self.source_url)), 25, 'test get_code_urls fail')

    def test_get_codes(self):
        self.assertEqual(len(get_codes(self.code_url)), 2, 'test get_codes fail')


if __name__ =='__main__':
    unittest.main()