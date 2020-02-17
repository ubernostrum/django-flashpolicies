"""
Utilities for generating Flash cross-domain policy files.

"""

import xml.dom
from typing import Dict, Iterable, List, Optional


minidom = xml.dom.getDOMImplementation("minidom")


METAPOLICY_ERROR = (
    "Metapolicy currently forbids all access; to {}, change the metapolicy."
)
SITE_CONTROL_ERROR = (
    "'{}' is not a valid value for the 'permitted-cross-domain-policies' "
    "attribute of a 'site-control' element."
)
BAD_POLICY = (
    "Cannot produce XML from invalid policy (metapolicy forbids all access, "
    "but policy attempted to allow access anyway)."
)


#
# Acceptable values for the "permitted-cross-domain-policies"
# attribute of "site-control" elements. See section 3(b)(i) of the
# Adobe crossdomain.xml spec.
#

# All policy files are allowed:
SITE_CONTROL_ALL = "all"

# Only files served as text/x-cross-domain-policy are allowed:
SITE_CONTROL_BY_CONTENT_TYPE = "by-content-type"

# Only files named 'crossdomain.xml' are allowed:
SITE_CONTROL_BY_FTP_FILENAME = "by-ftp-filename"

# Only the master policy file is allowed:
SITE_CONTROL_MASTER_ONLY = "master-only"

# No policies are allowed, including the master policy:
SITE_CONTROL_NONE = "none"

VALID_SITE_CONTROL = (
    SITE_CONTROL_ALL,
    SITE_CONTROL_BY_CONTENT_TYPE,
    SITE_CONTROL_BY_FTP_FILENAME,
    SITE_CONTROL_MASTER_ONLY,
    SITE_CONTROL_NONE,
)


class Policy:
    """
    Wrapper object for creating and manipulating a Flash cross-domain
    policy.

    In the simplest case -- specifying one or more domains to allow
    access from -- simply pass the domains when initializing. For
    example::

        my_policy = Policy('media.example.com', 'api.example.com')

    The property ``xml_dom`` of the returned ``Policy`` object will be
    an ``xml.dom.minidom.Document`` representing the resulting policy,
    and can be serialized for serving via HTTP or writing to a
    file. For ease of use, ``__str__()`` is defined here and returns
    the policy as a Unicode string for easy inspection;
    ``serialize()`` will serialize to UTF-8 for serving or writing to
    a file.

    Consult the documentation for the various methods of this class
    for more advanced uses.

    """

    def __init__(self, *domains: str):
        self.site_control = None  # type: Optional[str]
        self.domains = {}  # type: Dict[str, dict]
        self.header_domains = {}  # type: Dict[str, dict]
        self.identities = []  # type: List[str]
        for domain in domains:
            self.allow_domain(domain)

    def allow_domain(
        self, domain: str, to_ports: Optional[Iterable[str]] = None, secure: bool = True
    ):
        """
        Allows access from ``domain``, which may be either a full
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
            raise TypeError(METAPOLICY_ERROR.format("allow a domain"))
        self.domains[domain] = {"to_ports": to_ports, "secure": secure}

    def metapolicy(self, permitted: str):
        """
        Sets metapolicy to ``permitted``. (only applicable to master
        policy files). Acceptable values correspond to those listed in
        Section 3(b)(i) of the crossdomain.xml specification, and are
        also available as a set of constants defined in this module.

        By default, Flash assumes a value of ``master-only`` for all
        policies except socket policies, (which assume a default of
        ``all``) so if this is desired (and, for security, it
        typically is), this method does not need to be called.

        Note that a metapolicy of ``none`` forbids **all** access,
        even if one or more domains, headers or identities have
        previously been specified as allowed. As such, setting the
        metapolicy to ``none`` will remove all access previously
        granted by ``allow_domain``, ``allow_headers`` or
        ``allow_identity``. Additionally, attempting to grant access
        via ``allow_domain``, ``allow_headers`` or ``allow_identity``
        will, when the metapolicy is ``none``, raise ``TypeError``.

        """
        if permitted not in VALID_SITE_CONTROL:
            raise TypeError(SITE_CONTROL_ERROR.format(permitted))
        if permitted == SITE_CONTROL_NONE:
            # Metapolicy 'none' means no access is permitted.
            self.domains = {}
            self.header_domains = {}
            self.identities = []
        self.site_control = permitted

    def allow_headers(self, domain: str, headers: Iterable[str], secure: bool = True):
        """
        Allows ``domain`` to push data via the HTTP headers named in
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
            raise TypeError(METAPOLICY_ERROR.format("allow headers from a domain"))
        self.header_domains[domain] = {"headers": headers, "secure": secure}

    def allow_identity(self, fingerprint: str):
        """
        Allows access from documents digitally signed by the key with
        ``fingerprint``.

        In theory, multiple algorithms can be added in the future for
        calculating ``fingerprint`` from the signing key, but at this
        time only one algorithm -- SHA-1 -- is supported by the
        cross-domain policy specification.

        """
        if self.site_control == SITE_CONTROL_NONE:
            raise TypeError(
                METAPOLICY_ERROR.format("allow access from signed documents")
            )
        if fingerprint not in self.identities:
            self.identities.append(fingerprint)

    def _add_domains_xml(self, document: xml.dom.minidom.Document):
        """
        Generates the XML elements for allowed domains.

        """
        for domain, attrs in self.domains.items():
            domain_element = document.createElement("allow-access-from")
            domain_element.setAttribute("domain", domain)
            if attrs["to_ports"] is not None:
                domain_element.setAttribute("to-ports", ",".join(attrs["to_ports"]))
            if not attrs["secure"]:
                domain_element.setAttribute("secure", "false")
            document.documentElement.appendChild(domain_element)

    def _add_header_domains_xml(self, document: xml.dom.minidom.Document):
        """
        Generates the XML elements for allowed header domains.

        """
        for domain, attrs in self.header_domains.items():
            header_element = document.createElement("allow-http-request-headers-from")
            header_element.setAttribute("domain", domain)
            header_element.setAttribute("headers", ",".join(attrs["headers"]))
            if not attrs["secure"]:
                header_element.setAttribute("secure", "false")
            document.documentElement.appendChild(header_element)

    def _add_identities_xml(self, document: xml.dom.minidom.Document):
        """
        Generates the XML elements for allowed digital signatures.

        """
        for fingerprint in self.identities:
            identity_element = document.createElement("allow-access-from-identity")
            signatory_element = document.createElement("signatory")
            certificate_element = document.createElement("certificate")
            certificate_element.setAttribute("fingerprint", fingerprint)
            certificate_element.setAttribute("fingerprint-algorithm", "sha-1")
            signatory_element.appendChild(certificate_element)
            identity_element.appendChild(signatory_element)
            document.documentElement.appendChild(identity_element)

    def _get_xml_dom(self) -> xml.dom.minidom.Document:
        """
        Collects all options set so far, and produce and return an
        ``xml.dom.minidom.Document`` representing the corresponding
        XML.

        """
        if self.site_control == SITE_CONTROL_NONE and any(
            (self.domains, self.header_domains, self.identities)
        ):
            raise TypeError(BAD_POLICY)

        policy_type = minidom.createDocumentType(
            qualifiedName="cross-domain-policy",
            publicId=None,
            systemId="http://www.adobe.com/xml/dtds/cross-domain-policy.dtd",
        )
        policy = minidom.createDocument(None, "cross-domain-policy", policy_type)

        if self.site_control is not None:
            control_element = policy.createElement("site-control")
            control_element.setAttribute(
                "permitted-cross-domain-policies", self.site_control
            )
            policy.documentElement.appendChild(control_element)

        for elem_type in ("domains", "header_domains", "identities"):
            getattr(self, "_add_{}_xml".format(elem_type))(policy)

        return policy

    xml_dom = property(_get_xml_dom)

    def __str__(self) -> str:
        return self.xml_dom.toprettyxml()

    def serialize(self) -> bytes:
        """
        Serializes this policy to a UTF-8 byte sequence.

        This is similar to __str__() but with one important
        difference: __str__() is required to return a Unicode string,
        and so can't use the 'encoding' argument of
        toprettyxml(). This method can return a bytes object, and will
        return a UTF-8-encoded byte sequence with appropriate encoding
        declaration in its XML prolog..

        In general, use str() if you just want to see what would be
        produced, and use serialize() if you want to pass the result
        to something that will serve the XML, or write to a file.

        """
        return self.xml_dom.toprettyxml(encoding="utf-8")
