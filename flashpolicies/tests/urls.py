"""
These URLs are used by the test suite to exercise the various
views. You should not use these URLs in any sort of real deployment
situation.

"""

from django.conf.urls import patterns
from django.conf.urls import url

from .. import policies


def make_test_policy():
    policy = policies.Policy()
    policy.allow_domain('media.example.com')
    policy.allow_headers('media.example.com', ['SomeHeader'])
    return policy

urlpatterns = patterns('',
                       url(r'^crossdomain-serve.xml$',
                           'flashpolicies.views.serve',
                           {'policy': make_test_policy()}),
                       url(r'^crossdomain-simple.xml$',
                           'flashpolicies.views.simple',
                           {'domains': ['media.example.com',
                                        'api.example.com']}),
                       url(r'^crossdomain-no-access.xml$',
                           'flashpolicies.views.no_access'),
                       url(r'^crossdomain-metapolicy.xml$',
                           'flashpolicies.views.metapolicy',
                           {'permitted': policies.SITE_CONTROL_ALL}),
                       )
