from fabric.api import env

env.user = 'deploy'

from fabfiles.fab_server import *
from fabfiles.fab_app import *
