.. -*-restructuredtext-*-

.. image:: https://travis-ci.org/ubernostrum/django-flashpolicies.svg?branch=master
    :target: https://travis-ci.org/ubernostrum/django-flashpolicies

This application provides management of Flash cross-domain access
policies for `Django <https://www.djangoproject.com>`_ sites. For
example, the following URL pattern is all you'd need to set up
cross-domain access for Flash files served from your media server:

.. code:: python

    from django.conf.urls import url

    from flashpolicies.views import allow_domains

    urlpatterns = [
        # ...your other URL patterns here...
        url(r'^crossdomain.xml$',
            allow_domains,
            {'domains': ['media.yoursite.com']}),
    ]


Various other views are included, handling other common and
not-so-common cases, as well as utilities for generating custom
cross-domain policies.

Full documentation for all functionality is also included and
`available online
<https://django-flashpolicies.readthedocs.io/>`_.
