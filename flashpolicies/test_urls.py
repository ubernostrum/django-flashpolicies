"""
These URLs are used by the test suite to exercise the various
views. You should not use these URLs in any sort of real deployment
situation.

"""

from django.conf.urls.defaults import *

from flashpolicies.policies import SITE_CONTROL_ALL


urlpatterns = patterns('',
                       url(r'^crossdomain1.xml$',
                           'flashpolicies.views.simple',
                           { 'domains': ['media.example.com', 'api.example.com'] }),
                       url(r'^crossdomain2.xml$',
                           'flashpolicies.views.no_access'),
                       url(r'^crossdomain3.xml$',
                           'flashpolicies.views.metapolicy',
                           { 'site_control': SITE_CONTROL_ALL }),
                       )
