#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""fabric script."""

import os
import re
import datetime

# 导入Fabric API:
from fabric.api import *

# 服务器登录用户名:
env.user = 'root'

# sudo用户为root:
env.sudo_user = 'root'

# 服务器地址，可以有多个，依次部署:
env.hosts = ['119.28.3.110']


_TAR_FILE = 'just.tar.gz'


def build():
    includes = ['.']
    excludes = ['tests', '.*', '*.pyc', '*.pyo', 'LICENSE',
                'Procfile', 'README.rst', 'sdist', 'env']
    local('rm -f sdist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'))):
        cmd = ['tar', '--dereference', '-czvf', 'sdist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=./\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))



_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/just'

def deploy():
    newdir = 'just-%s' % datetime.datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # 删除已有的tar文件:
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件:
    put('sdist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # 解压到新目录:
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f /var/www/just')
        sudo('ln -s %s /var/www/just' % newdir)
        sudo('chown www-data:www-data /var/www/just')
        sudo('chown -R www-data:www-data %s' % newdir)
    # 重启Python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('supervisorctl stop just')
        sudo('supervisorctl start just')
        sudo('/etc/init.d/nginx reload')
