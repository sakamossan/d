# coding:utf-8
from __future__ import unicode_literals
from fabric.api import *
from d import setting_secret as settings

env.hosts = settings.DEPLOY_HOSTS
env.key_filename = ['~/.ssh/mcsk_rsa']
env.user = 'mcsk'


def say_hostname():
    run('hostname')


def deploy(branch='master'):
    with cd('/mcsk/d/d'):
        run("git checkout")
        run("git checkout {}".format(branch))

