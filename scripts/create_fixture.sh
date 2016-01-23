#!/bin/bash -eux

# テストで使用するfixtureデータを生成する


cp -f {,_}db.sqlite3
python ./manage.py dumpdata scrape --format=json --indent=4 > scrape/fixtures/scrape.json
mv {_,}db.sqlite3
