.. -*-restructuredtext-*-

.. image:: https://github.com/ubernostrum/django-registration/workflows/CI/badge.svg
   :alt: CI status image
   :target: https://github.com/ubernostrum/django-flaskpolicies/actions?query=workflow%3ACI

This application provides management of Flash cross-domain access
policies for `Django <https://www.djangoproject.com>`_ sites. For
example, the following URL pattern is all you'd need to set up
cross-domain access for Flash files served from your media server:

.. code:: python

    from django.urls import path

    from flashpolicies.views import allow_domains

    urlpatterns = [
        # ...your other URL patterns here...
        path(
            'crossdomain.xml',
            allow_domains,
            {'domains': ['media.example.com']}
        ),
    ]


Various other views are included, handling other common and
not-so-common cases, as well as utilities for generating custom
cross-domain policies.

Full documentation for all functionality is also included and
`available online
<https://django-flashpolicies.readthedocs.io/>`_.
