from __future__ import with_statement

import os

from fabric.context_managers import lcd, cd
from fabric.api import local, run

def restart_services():
    local('sudo service nginx restart')
    local('sudo service uwsgi restart')

def deploy_local(dir="/var/www/flask-patw"):
    local('sudo cp -r patw %s/' % dir)
    restart_services()

def deploy(version="master"):
    run('rm -rf flask-social-login-demo')
    run('mkdir flask-social-login-demo')
    with cd(version):
        run('git clone -b %s git@github.com:patw0929/flask-social-login-demo.git' % version)
    with cd("flask-social-login-demo"):
        run('fab deploy_local:dir=/var/www/flask-patw')
