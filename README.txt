This application enables simple Flash cross-domain access policies for
Django sites. For example, the following URL pattern is all you'd need
to set up cross-domain access for Flash files served from your media
server::

    url(r'^crossdomain.xml$',
        'flashpolicies.views.simple',
        { 'domains': ['media.yoursite.com'] }),

For details, see the file ``docs/overview.txt``.
