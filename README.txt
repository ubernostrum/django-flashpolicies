This application enables simple Flash cross-domain access policies for
Django sites. For example, the following URL pattern is all you'd need
to set up cross-domain access for Flash files served from your media
server::

    url(r'^crossdomain.xml$',
        'flashpolicies.views.simple',
        { 'domains': ['media.yoursite.com'] }),

Various other views are included, handling other common and
not-so-common cases, as well as a utility class for generating and
manipulating cross-domain policies in a straightforward way and
serializing them to the correct XML.

Full documentation for all functionality is also included, as well as
an ever-growing test suite.
