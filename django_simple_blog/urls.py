from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_server.simple_blog.views.index', name='simple_blog_index'),
    url(r'^admin/', include(admin.site.urls)),
)
