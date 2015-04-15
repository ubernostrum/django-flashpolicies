"""
Utilities for generating Flash cross-domain policy files.

"""

import xml.dom


minidom = xml.dom.getDOMImplementation('minidom')


#
# Acceptable values for the "permitted-cross-domain-policies"
# attribute of "site-control" elements. See section 3(b)(i) of the
# Adobe crossdomain.xml spec.
#

SITE_CONTROL_ALL = "all"
SITE_CONTROL_BY_CONTENT_TYPE = "by-content-type"
SITE_CONTROL_BY_FTP_FILENAME = "by-ftp-filename"
SITE_CONTROL_MASTER_ONLY = "master-only"
SITE_CONTROL_NONE = "none"

VALID_SITE_CONTROL = (SITE_CONTROL_ALL,
                      SITE_CONTROL_BY_CONTENT_TYPE,
                      SITE_CONTROL_BY_FTP_FILENAME,
                      SITE_CONTROL_MASTER_ONLY,
                      SITE_CONTROL_NONE)


class Policy(object):
    """
    Wrapper object for creating and manipulating a Flash cross-domain
    policy.

    In the simplest case -- specifying one or more domains to allow
    access from -- simply pass the domains to the constructor. For
    example::

        my_policy = Policy('media.example.com', 'api.example.com')

    The property ``xml_dom`` of the returned ``Policy`` object will be
    an ``xml.dom.minidom.Document`` representing the resulting policy,
    and can be serialized for writing to a file or returning via
    HTTP. For ease of use, ``__str__()`` is defined here and returns
    the policy serialized to a UTF-8 bytestring.

    Consult the documentation for the various methods of this class
    for more advanced uses.

    """
    def __init__(self, *domains):
        self.site_control = None
        self.domains = {}
        self.header_domains = {}
        self.identities = []
        for domain in domains:
            self.allow_domain(domain)

    def allow_domain(self, domain, to_ports=None, secure=True):
        """
        Allow access from ``domain``, which may be either a full
        domain name, or a wildcard (e.g., ``*.example.com``, or simply
        ``*``). Due to security concerns, it is strongly recommended
        that you use explicit domains rather than wildcards.

        For socket policy files, pass a list of ports or port ranges
        as the keyword argument ``to_ports``. As with ``domain``, a
        wildcard value -- ``*`` -- will allow all ports.

        To disable Flash's requirement of security matching (e.g.,
        retrieving a policy via HTTPS will require that SWFs also be
        retrieved via HTTPS), pass ``secure=False``. Due to security
        concerns, it is strongly recommended that you not disable
        this.

        """
        if self.site_control == SITE_CONTROL_NONE:
            raise TypeError(
                "Metapolicy currently forbids all access; "
                "to allow a domain, change the metapolicy."
            )
        self.domains[domain] = {'to_ports': to_ports,
                                'secure': secure}

    def metapolicy(self, permitted):
        """
        Set meta-policy to ``permitted``. (only applicable to master
        policy files). Acceptable values correspond to those listed in
        Section 3(b)(i) of the crossdomain.xml specification, and are
        also available as a set of constants defined in this module.

        By default, Flash assumes a value of ``master-only`` for all
        policies except socket policies, (which assume a default of
        ``all``) so if this is desired (and, for security, it
        typically is), this method does not need to be called.

        Note that a metapolicy of ``none`` forbids **all** access,
        even if one or more domains have previously been specified as
        allowed. As such, setting the metapolicy to ``none`` will
        remove all access previously granted by ``allow_domain`` or
        ``allow_headers``. Additionally, attempting to grant access
        via ``allow_domain`` or ``allow_headers`` will, when the
        metapolicy is ``none``, raise ``TypeError``.

        """
        if permitted not in VALID_SITE_CONTROL:
            raise TypeError(
                '"%s" is not a valid value for the '
                '"permitted-cross-domain-policies" '
                'attribute of a site-control element' % permitted
            )
        if permitted == SITE_CONTROL_NONE:
            # Metapolicy 'none' means no access is permitted.
            self.domains = {}
            self.header_domains = {}
        self.site_control = permitted

    def allow_headers(self, domain, headers, secure=True):
        """
        Allow ``domain`` to push data via the HTTP headers named in
        ``headers``.

        As with ``allow_domain``, ``domain`` may be either a full
        domain name or a wildcard. Again, use of wildcards is
        discouraged for security reasons.

        The value for ``headers`` should be a list of header names.

        To disable Flash's requirement of security matching (e.g.,
        retrieving a policy via HTTPS will require that SWFs also be
        retrieved via HTTPS), pass ``secure=False``. Due to security
        concerns, it is strongly recommended that you not disable
        this.

        """
        if self.site_control == SITE_CONTROL_NONE:
            raise TypeError(
                "Metapolicy currently forbids all access; "
                "to allow headers from a domain, change the metapolicy."
            )
        self.header_domains[domain] = {'headers': headers,
                                       'secure': secure}

    def allow_identity(self, fingerprint):
        """
        Allow access from documents digitally signed by the key with
        ``fingerprint``.

        In theory, multiple algorithms can be added in the future for
        calculating ``fingerprint`` from the signing key, but at this
        time only one algorithm -- SHA-1 -- is supported by the
        cross-domain policy specification.

        """
        if fingerprint not in self.identities:
            self.identities.append(fingerprint)

    def _get_xml_dom(self):
        """
        Collect all options set so far, and produce and return an
        ``xml.dom.minidom.Document`` representing the corresponding
        XML.

        """
        policy_type = minidom.createDocumentType(
            qualifiedName='cross-domain-policy',
            publicId=None,
            systemId='http://www.adobe.com/xml/dtds/cross-domain-policy.dtd'
        )
        policy = minidom.createDocument(
            None,
            'cross-domain-policy',
            policy_type
        )

        if self.site_control is not None:
            control_element = policy.createElement('site-control')
            control_element.setAttribute(
                'permitted-cross-domain-policies',
                self.site_control
            )
            policy.documentElement.appendChild(control_element)

        for domain, attrs in self.domains.items():
            domain_element = policy.createElement('allow-access-from')
            domain_element.setAttribute('domain', domain)
            if attrs['to_ports'] is not None:
                domain_element.setAttribute(
                    'to-ports',
                    ','.join(attrs['to_ports'])
                )
            if not attrs['secure']:
                domain_element.setAttribute('secure', 'false')
            policy.documentElement.appendChild(domain_element)

        for domain, attrs in self.header_domains.items():
            header_element = policy.createElement(
                'allow-http-request-headers-from'
            )
            header_element.setAttribute('domain', domain)
            header_element.setAttribute('headers', ','.join(attrs['headers']))
            if not attrs['secure']:
                header_element.setAttribute('secure', 'false')
            policy.documentElement.appendChild(header_element)

        for fingerprint in self.identities:
            identity_element = policy.createElement(
                'allow-access-from-identity'
            )
            signatory_element = policy.createElement(
                'signatory'
            )
            certificate_element = policy.createElement(
                'certificate'
            )
            certificate_element.setAttribute(
                'fingerprint',
                fingerprint)
            certificate_element.setAttribute(
                'fingerprint-algorithm',
                'sha-1')
            signatory_element.appendChild(certificate_element)
            identity_element.appendChild(signatory_element)
            policy.documentElement.appendChild(identity_element)

        return policy

    xml_dom = property(_get_xml_dom)

    def __str__(self):
        return self.xml_dom.toprettyxml()

    def serialize(self):
        # This is similar to __str__() but with one important
        # difference: on Python 3, __str__() is required to return a
        # Unicode string, and so can't use the 'encoding'
        # argument. This method has no such requirement. As a result,
        # this method will return a UTF-8-encoded byte sequence (which
        # is str on Python 2, but bytes on Python 3).
        #
        # In general, use str() if you just want to see what would be
        # produced, and use serialize() if you want to pass the result
        # to something that will serve the XML, or write to a file.
        #
        return self.xml_dom.toprettyxml(encoding='utf-8')
