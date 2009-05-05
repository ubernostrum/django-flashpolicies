"""
These URLs are used by the test suite to exercise the various
views. You should not use these URLs in any sort of real deployment
situation.

"""

from django.conf.urls.defaults import *


urlpatterns = patterns('',
                       url(r'^crossdomain1.xml$',
                           'flashpolicies.views.simple',
                           { 'domains': ['media.example.com', 'api.example.com'] }),
                       url(r'^crossdomain2.xml$',
                           'flashpolicies.views.no_access'),
                       )
