#!/bin/sh

set -eu

sudo su - mcsk sh -c  "cd /mcsk/d/d; /home/mcsk/.pyenv/bin/pyenv exec gunicorn d.wsgi:application"