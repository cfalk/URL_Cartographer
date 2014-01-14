from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home),
    url(r'^query/?$', home),

    url(r'^admin/', include(admin.site.urls)),
)
