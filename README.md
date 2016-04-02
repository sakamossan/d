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
