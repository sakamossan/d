# coding:utf-8
from __future__ import unicode_literals


class Page(object):

    # 最低限検索に引っかからないようにする
    domain = "".join([chr(ord(c)+3) for c in 'eqqm7,,ttt+`fqveb^sbk+kbq,'])

    def __init__(self, shop):
        self.shop = shop

    def url(self):
         return self.domain


