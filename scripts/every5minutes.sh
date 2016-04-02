#!/usr/bin/env bash

cd /mcsk/d/d
~/.pyenv/bin/pyenv exec python ./manage.py run_scrape
~/.pyenv/bin/pyenv exec python ./manage.py log2db
