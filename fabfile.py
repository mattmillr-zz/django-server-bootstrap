from fabric.api import env

env.user = 'deploy'

from fab_server import *
from fab_app import *
