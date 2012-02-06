from fabric.api import env

CONFIG = {}
CONFIG['authorizedkeys'] = (
    'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwfYSqGg+4wH3NM5X5UIufOkQFISrH5RKahpIqq/b77YfVPUa3axlv0G17Ob+8AqNuCThpn9nZqYrpXBqbevIYQV9ZsMosIGY5FowRL4fcxFpQ1gpk0IqQVUahKM9O3ta//Vz7Y0bj6njGosXZ46aLaypAJMrmcdk/bxOHmFVdfx8dJi30LgIryzJRueDVub3EJatTL0Ewtuc4MsyUwC4vfM85+B7PBOVqz8MTTVjA79pAlznGOj2NH6t0lfiATDE8pIhDO7OMhQXwiR226Mg0OZaPCwdIsQSG/U1CxpVRYABZrC1mabmvmqK9re7gpOmClusqS7+KK5ja6IVR8QmZQ== mattmiller25@gmail.com',
    )
    
# TODO: There's probably a way to get all this from the local .git stuff
CONFIG['git-username'] = 'mattmillr'
CONFIG['git-repo'] = 'django-server-bootstrap'

def bksw1():
    env.hosts = ['66.228.46.218',]
    global DJANGO_ENV
    DJANGO_ENV = 'dev'
    