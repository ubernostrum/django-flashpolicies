This application enables simple Flash cross-domain access policies for
Django sites. For example, the following URL pattern is all you'd need
to set up cross-domain access for Flash files served from your media
server::

    url(r'^crossdomain.xml$',
        'flashpolicies.views.simple',
        { 'domains': ['media.yoursite.com'] }),

Various other views are included, handling other common and
not-so-common cases.

Also present is a class -- ``flashpolicies.policies.Policy`` -- which
provides a simple Python API for creating and manipulating
cross-domain policies, as well as serializing them to the correct
XML. This class is designed to be useful regardless of whether Django
is present or used, and depends only on modules available in the
Python standard library.

Full documentation for all functionality is also included, as well as
an ever-growing test suite.
