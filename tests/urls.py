"""
These URLs are used by the test suite to exercise the various
views. You should not use these URLs in any sort of real deployment
situation.

"""

from django.urls import path

from flashpolicies import policies, views


def make_test_policy():
    policy = policies.Policy()
    policy.allow_domain("media.example.com")
    policy.allow_headers("media.example.com", ["SomeHeader"])
    return policy


urlpatterns = [
    path("crossdomain-serve.xml", views.serve, {"policy": make_test_policy()}),
    path(
        "crossdomain-allow-domains.xml",
        views.allow_domains,
        {"domains": ["media.example.com", "api.example.com"]},
    ),
    path(
        "crossdomain-simple-alias.xml",
        views.simple,
        {"domains": ["media.example.com", "api.example.com"]},
    ),
    path("crossdomain-no-access.xml", views.no_access),
    path(
        "crossdomain-metapolicy.xml",
        views.metapolicy,
        {"permitted": policies.SITE_CONTROL_ALL},
    ),
]
