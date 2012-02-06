import os, sys, site

site.addsitedir('/home/apps/simpleblog/virtualenv/lib/python2.6/site-packages')

sys.path.insert(0, "/home/apps/simpleblog/current")
sys.path.insert(0, "/home/apps/simpleblog/current/django_simple_blog")
sys.path.insert(0, "/home/apps/simpleblog/virtualenv/lib/python2.6/site-packages")

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_simple_blog.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
