# coding:utf-8
from __future__ import unicode_literals

import re
import datetime
import json


def jsonl_file_path(date, pref=''):
    return "./resources/jsonl/{0}{1:%Y%m%d}.jsonl".format(pref, date)


class Writer(object):

    class Encoder(json.JSONEncoder):
        """
        時刻データはそのままだと文字列データに変換できない
        時刻の情報をログに落とすために
        時刻データ -> 文字列データ に変換をどう行うかを定義するためのクラス
        """
        def default(self, o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            else:
                return json.JSONEncoder.default(o)

    def __init__(self, file_path):
        self.file = open(file_path, 'a')

    def to_json(self, serializable):
        """
        :type serializable: dict|list[dict]
        :rtype: str
        """
        return json.dumps(
            serializable,
            sort_keys=True,
            ensure_ascii=False,
            cls=self.Encoder
        )

    def write(self, list_of_serializable, delim="\n", file_close=False):
        """:type list_of_serializable: list[dict|list]"""
        self.file.writelines([
            (self.to_json(d) + delim).encode('utf-8')
            for d in list_of_serializable
        ])
        if file_close:
            self.file.close()


class Reader(object):

    @staticmethod
    def hook(dict_):
        for k, v in dict_.items():
            if isinstance(v, basestring) and re.search("^\d{4}-\d{2}-\d{2}", v):
                try:
                    dict_[k] = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    pass
        return dict_

    def __init__(self, file_path):
        self.file = open(file_path, 'r')

    def readlines(self):
        for line in self.file.readlines():
            yield json.loads(line, object_hook=Reader.hook)
        self.file.close()
        raise StopIteration
