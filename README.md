# d

## development

```bash
virtualenv d && cd $_
source bin/activate
git clone git@github.com:sakamossan/d.git && cd d
pip install -U setuptools
pip install -r requirements.txt
python ./manage.py migrate
python ./manage.py runserver
```

## env

```bash
cd ./ops
vagrant up
```

## test

```bash
python ./manage.py test -v 1 -s -p
```


## commands

### recreate_view

データベースにビューを作成する
`resources/view_sqls`に入っているファイルの内容をDBに適用している

### run_scrape

scrape処理を実行する。結果はjsonl形式で出力される

### log2db

jsonl形式で蓄積したデータをDBに入れる

