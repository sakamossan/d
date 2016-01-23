# d

## env

```bash
virtualenv d && cd $_
source bin/activate
git clone git@github.com:sakamossan/d.git cd d
pip install -r requirements.txt
python ./manage.py runserver
```

## test

```bash
python ./manage.py test -v 1 -s -p
```