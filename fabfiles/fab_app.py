from datetime import datetime
from fabric.api import env, run, sudo
from fabric.utils import abort
from fabric.context_managers import settings

from fab_config import *

def install_app():
    # create db & set user permissions
    # create app folder /apps/app-name
    # create repo folder /apps/app-name/repo
    # checkout repo
    # create virtualenv folder /apps/app-name/virtualenv
    # create virtualenv
    pass
    
def deploy():
    pass