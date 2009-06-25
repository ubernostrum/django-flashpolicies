"""
These URLs are used by the test suite to exercise the various
views. You should not use these URLs in any sort of real deployment
situation.

"""

from django.conf.urls.defaults import *

from flashpolicies import policies


def make_test_policy():
    policy = policies.Policy()
    policy.allow_domain('media.example.com')
    policy.allow_headers('media.example.com', ['SomeHeader'])
    return policy

urlpatterns = patterns('',
                       url(r'^crossdomain1.xml$',
                           'flashpolicies.views.simple',
                           {'domains': ['media.example.com',
                                         'api.example.com']}),
                       url(r'^crossdomain2.xml$',
                           'flashpolicies.views.no_access'),
                       url(r'^crossdomain3.xml$',
                           'flashpolicies.views.metapolicy',
                           {'permitted': policies.SITE_CONTROL_ALL}),
                       url(r'^crossdomain4.xml$',
                           'flashpolicies.views.serve',
                           {'policy': make_test_policy()}),
                       )
