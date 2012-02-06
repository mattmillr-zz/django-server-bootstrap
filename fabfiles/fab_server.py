from fabric.api import env, run, sudo

GITHUB_URL_TEMPLATE = "git://github.com/%(git-username)s/%(git-repo)s.git"
GITHUB_KEY = "github.com,207.97.227.239 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=="

from fab_config import *

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
    
def install_basics():
    update()
    mysql()  
    tools()
    apache()
    nginx()
    mercurial()

def clone_git_config_repo():
    run('touch ~/.ssh/known_hosts')
    run ('echo "%s" >> ~/.ssh/known_hosts' % GITHUB_KEY)
    git_repo_url = GITHUB_URL_TEMPLATE % CONFIG
    run('rm -rf %(git-repo)s' % CONFIG)
    run('git clone %s server_config_repo/%s' % (git_repo_url, CONFIG['git-repo']))
    run('ls -al')

def config_apache():
    sudo('cp /home/deploy/server_config_repo/%(git-repo)s/conf/ports.conf /etc/apache2/' % CONFIG)
    sudo('cp /home/deploy/server_config_repo/%(git-repo)s/conf/apache2.conf /etc/apache2/' % CONFIG)
    sudo('/etc/init.d/apache2 restart')
    
def config_nginx():
    sudo('mkdir /var/www/cache/one -p')
    sudo('mkdir /var/www/cache/temp -p')
    sudo('cp /home/deploy/server_config_repo/%(git-repo)s/conf/nginx.conf /etc/nginx/' % CONFIG)
    sudo('/etc/init.d/nginx restart')
     
def server_settings():
    clone_git_config_repo()
    config_apache()
    config_nginx()
    
def user_folders():
    run('mkdir ~/server_config_repo')
    run('mkdir ~/apps')

def bootstrap():
    add_deploy_user()
    test_login()
    install_basics()
    user_folders()
    server_settings()

