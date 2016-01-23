# coding:utf-8
from __future__ import unicode_literals

import datetime
import json


def jlfile_path(date, pref=''):
    return "./log/{0}{1:%Y%m%d}.jl".format(pref, date)


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

    def write_jsonlines(self, list_of_serializable, delim="\n", file_close=False):
        """:type list_of_serializable: list[dict|list]"""
        self.file.writelines([
            (self.to_json(d) + delim).encode('utf-8')
            for d in list_of_serializable
        ])
        if file_close:
            self.file.close()
