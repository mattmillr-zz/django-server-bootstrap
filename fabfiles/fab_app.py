from datetime import datetime
from fabric.api import env, run, sudo
from fabric.utils import abort
from fabric.context_managers import settings

from fab_config import *

def install():
    
    global DJANGO_ENV
    global CONFIG
    
    if not DJANGO_ENV:
        abort("You must specify a Django environment to set up.")
    
    # create app folder /apps/app-name
    # create repo folder /apps/app-name/repo
    # checkout repo

    # create db & set user permissions
    # create virtualenv folder /apps/app-name/virtualenv
    # create virtualenv
    pass
    
def deploy():
    # config timestamp
    # pull & update repo on server
    # copy files to release dir
    # update virtualenv dependencies
    # symlink current --> release
    # copy apache config
    # copy nginx confi
    # reload apache
    # restart nginx
    pass