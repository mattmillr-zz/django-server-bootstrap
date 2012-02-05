from datetime import datetime
from fabric.api import env, run, sudo
from fabric.utils import abort
from fabric.context_managers import settings

CONFIG = {}
CONFIG['authorizedkeys'] = (
    'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwfYSqGg+4wH3NM5X5UIufOkQFISrH5RKahpIqq/b77YfVPUa3axlv0G17Ob+8AqNuCThpn9nZqYrpXBqbevIYQV9ZsMosIGY5FowRL4fcxFpQ1gpk0IqQVUahKM9O3ta//Vz7Y0bj6njGosXZ46aLaypAJMrmcdk/bxOHmFVdfx8dJi30LgIryzJRueDVub3EJatTL0Ewtuc4MsyUwC4vfM85+B7PBOVqz8MTTVjA79pAlznGOj2NH6t0lfiATDE8pIhDO7OMhQXwiR226Mg0OZaPCwdIsQSG/U1CxpVRYABZrC1mabmvmqK9re7gpOmClusqS7+KK5ja6IVR8QmZQ== mattmiller25@gmail.com',
    )

env.user = 'deploy'

from server_configs import *

def add_deploy_user():
    # as root:
    old_user = env.user
    env.user = 'root'
    
    # create the user with a home directory and no password
    run("useradd deploy -m -s /bin/bash")
    
    # set up the authorized keys file
    run("mkdir ~deploy/.ssh")
    run("chown deploy:deploy ~deploy/.ssh")
    run("chmod 755 ~deploy/.ssh")

    run("touch ~deploy/.ssh/authorized_keys2")
    for key in CONFIG['authorizedkeys']:
        run('echo "%s" >> ~deploy/.ssh/authorized_keys2' % (key,))
    run("chown deploy:deploy ~deploy/.ssh/authorized_keys2")
    run("chmod 644 ~deploy/.ssh/authorized_keys2")
    
    # add the user to sudoers
    run('echo "" >> /etc/sudoers')
    run('echo "# Added by fab setup script:" >> /etc/sudoers')
    run('echo "deploy ALL=NOPASSWD: ALL" >> /etc/sudoers')
    
    env.user = old_user
    
def test_login():
    run("whoami")
    run("pwd")
    run("ls -al")

def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)

def update ():
    sudo("apt-get update")

def mysql():
    apt_get('mkpasswd')
    mysql_root_pw = sudo("mkpasswd 'seed'")
    sudo('echo "%s" >> /root/mysql_root_passwd' % (mysql_root_pw,))
    sudo('chmod 600 /root/mysql_root_passwd')
    sudo('echo "mysql-server-5.0 mysql-server/root_password password %s" | debconf-set-selections' % mysql_root_pw)
    sudo('echo "mysql-server-5.0 mysql-server/root_password_again password %s" | debconf-set-selections' % mysql_root_pw)
    apt_get('libmysqlclient-dev', 'mysql-server')

def tools():
    # Install build & version control tools
    apt_get('python-setuptools', 'rsync', 'python-dev', 'build-essential', 'mercurial', 'git-core', 'subversion')
    # apt-get install hg v 1.4, upgrade to latest (2.1+)
    sudo("easy_install -U mercurial")
    
def apache():
    apt_get('apache2', 'apache2.2-common', 'apache2-mpm-worker', 'apache2-threaded-dev', 'libapache2-mod-wsgi')

def nginx():
    apt_get('nginx')

def mercurial():
    apt_get()
    
def basics():
    update()
    mysql()  
    tools()
    apache()
    nginx()
    mercurial()

def app_folders():
    run('mkdir ~/apps')

def app_framework():
    app_folders()

def bootstrap():
    add_deploy_user()
    test_login()
    basics()
    app_framework()

