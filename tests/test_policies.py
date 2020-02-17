from django.test import SimpleTestCase

from flashpolicies import policies


class PolicyGeneratorTests(SimpleTestCase):
    """
    Tests the policy-file generation utilities.

    """

    dummy_fingerprint = "01:23:45:67:89:ab:cd:ef:01:23:45:67:89:ab:cd:ef:01:23:45:67"

    def test_policy_str(self):
        """
        Tests that str() on a Policy returns an object of type str with
        no encoding declared.

        """
        policy_str = str(policies.Policy())
        self.assertTrue(isinstance(policy_str, str))
        self.assertTrue(policy_str.startswith('<?xml version="1.0" ?>'))

    def test_policy_serialize(self):
        """
        Tests that serialize() returns an object of type bytes, with a
        declared encoding of UTF-8.

        """
        policy_bytes = policies.Policy().serialize()
        self.assertTrue(isinstance(policy_bytes, bytes))
        self.assertTrue(
            policy_bytes.startswith(b'<?xml version="1.0" encoding="utf-8"?>')
        )

    def test_policy_type(self):
        """
        Tests that the correct ``DOCTYPE`` declaration is generated.

        """
        policy = policies.Policy().xml_dom
        self.assertEqual(
            policy.doctype.systemId,
            "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd",
        )
        self.assertEqual(policy.doctype.name, "cross-domain-policy")
        self.assertEqual(len(policy.childNodes), 2)

    def test_policy_root_element(self):
        """
        Tests that the correct root element is inserted.

        """
        policy = policies.Policy().xml_dom
        self.assertEqual(policy.documentElement.tagName, "cross-domain-policy")
        self.assertEqual(len(policy.documentElement.childNodes), 0)

    def test_allow_access_domain(self):
        """
        Tests that adding access for a domain inserts the proper
        element and attribute.

        """
        policy = policies.Policy()
        policy.allow_domain("media.example.com")
        xml_dom = policy.xml_dom
        self.assertEqual(len(xml_dom.documentElement.childNodes), 1)
        self.assertEqual(len(xml_dom.getElementsByTagName("allow-access-from")), 1)
        access_elem = xml_dom.getElementsByTagName("allow-access-from")[0]
        self.assertEqual(len(access_elem.attributes), 1)
        self.assertEqual(access_elem.getAttribute("domain"), "media.example.com")

    def test_allow_access_ports(self):
        """
        Tests that adding port access for socket connections inserts
        the proper attribute.

        """
        policy = policies.Policy()
        ports = ["80", "8080", "9000-1000"]
        policy.allow_domain("media.example.com", to_ports=ports)
        access_elem = policy.xml_dom.getElementsByTagName("allow-access-from")[0]
        self.assertEqual(len(access_elem.attributes), 2)
        self.assertEqual(access_elem.getAttribute("to-ports"), ",".join(ports))

    def test_allow_access_secure(self):
        """
        Tests that setting non-secure access for a domain inserts the
        proper attribute.

        """
        policy = policies.Policy()
        policy.allow_domain("media.example.com", secure=False)
        access_elem = policy.xml_dom.getElementsByTagName("allow-access-from")[0]
        self.assertEqual(len(access_elem.attributes), 2)
        self.assertEqual(access_elem.getAttribute("secure"), "false")

    def test_metapolicy(self):
        """
        Tests that adding metapolicy information inserts the proper
        element and attributes.

        """
        for permitted in policies.VALID_SITE_CONTROL:
            policy = policies.Policy()
            policy.metapolicy(permitted)
            xml_dom = policy.xml_dom
            self.assertEqual(len(xml_dom.documentElement.childNodes), 1)
            self.assertEqual(len(xml_dom.getElementsByTagName("site-control")), 1)
            control_elem = xml_dom.getElementsByTagName("site-control")[0]
            self.assertEqual(len(control_elem.attributes), 1)
            self.assertEqual(
                control_elem.getAttribute("permitted-cross-domain-policies"), permitted
            )

    def test_bad_metapolicy(self):
        """
        Tests that metapolicies are restricted to the values permitted
        by the specification.

        """
        policy = policies.Policy()
        self.assertRaises(TypeError, policy.metapolicy, "not-valid")

    def test_metapolicy_none_empty_domains(self):
        """
        Tests that setting the metapolicy to ``none`` clears the list
        of permitted domains.

        """
        policy = policies.Policy("media.example.com", "api.example.com")
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertEqual(
            len(policy.xml_dom.getElementsByTagName("allow-access-from")), 0
        )

    def test_metapolicy_none_empty_identities(self):
        """
        Tests that setting the metapolicy to ``none`` clears the list
        of permitted cryptographic identities.

        """
        policy = policies.Policy()
        policy.allow_identity(self.dummy_fingerprint)
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertEqual(
            len(policy.xml_dom.getElementsByTagName("allow-access-from-identity")), 0
        )

    def test_metapolicy_none_empty_headers(self):
        """
        Tests that setting the metapolicy to ``non`` clears the list of
        domains from which headers are permitted.

        """
        policy = policies.Policy()
        policy.allow_headers("media.example.com", ["SomeHeader"])
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertEqual(
            len(policy.xml_dom.getElementsByTagName("allow-http-request-headers-from")),
            0,
        )

    def test_metapolicy_none_disallow_domains(self):
        """
        Tests that attempting to allow access from a domain, when the
        metapolicy is ``none``, raises an exception.

        """
        policy = policies.Policy()
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertRaises(TypeError, policy.allow_domain, "media.example.com")

    def test_metapolicy_none_disallow_headers(self):
        """
        Tests that attempting to allow headers from a domain, when the
        metapolicy is ``none``, raises an exception.

        """
        policy = policies.Policy()
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertRaises(
            TypeError, policy.allow_headers, "media.example.com", ["SomeHeader"]
        )

    def test_metapolicy_non_disallow_identities(self):
        """
        Tests that attempting to allow access from signed documents,
        when the metapolicy is ``none``, raises an exception.

        """
        policy = policies.Policy()
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        self.assertRaises(TypeError, policy.allow_identity, self.dummy_fingerprint)

    def test_metapolicy_manual_tinkering(self):
        """
        Tests that setting metapolicy ``none``, then manually fiddling
        with the internals to try to allow things, will fail when the
        XML gets generated.

        """
        policy = policies.Policy()
        policy.metapolicy(policies.SITE_CONTROL_NONE)
        policy.domains["api.example.com"] = {"to_ports": None, "secure": True}
        with self.assertRaises(TypeError):
            policy.xml_dom

    def test_allow_http_headers(self):
        """
        Tests that allowing HTTP headers inserts the proper element and
        attributes.

        """
        domain = "media.example.com"
        headers = ["SomeHeader", "SomeOtherHeader"]
        policy = policies.Policy()
        policy.allow_headers(domain, headers, secure=False)
        xml_dom = policy.xml_dom
        self.assertEqual(
            len(xml_dom.getElementsByTagName("allow-http-request-headers-from")), 1
        )
        header_elem = xml_dom.getElementsByTagName("allow-http-request-headers-from")[0]
        self.assertEqual(len(header_elem.attributes), 3)
        self.assertEqual(header_elem.getAttribute("domain"), domain)
        self.assertEqual(header_elem.getAttribute("headers"), ",".join(headers))
        self.assertEqual(header_elem.getAttribute("secure"), "false")

    def test_allow_http_headers_secure(self):
        """
        Tests that setting non-secure access for HTTP headers from a
        domain inserts the proper attribute.

        """
        domain = "media.example.com"
        headers = ["SomeHeader", "SomeOtherHeader"]
        policy = policies.Policy()
        policy.allow_headers(domain, headers, secure=False)
        xml_dom = policy.xml_dom
        header_elem = xml_dom.getElementsByTagName("allow-http-request-headers-from")[0]
        self.assertEqual(len(header_elem.attributes), 3)
        self.assertEqual(header_elem.getAttribute("secure"), "false")

    def test_allow_identity(self):
        """
        Tests that allowing access from digitally-signed documents
        inserts the proper elements and attributes.

        """
        policy = policies.Policy()
        policy.allow_identity(self.dummy_fingerprint)
        xml_dom = policy.xml_dom
        identity_elem = xml_dom.getElementsByTagName("allow-access-from-identity")[0]
        self.assertEqual(len(identity_elem.childNodes), 1)
        signatory_elem = identity_elem.childNodes[0]
        self.assertEqual("signatory", signatory_elem.tagName)
        self.assertEqual(len(signatory_elem.childNodes), 1)
        certificate_elem = signatory_elem.childNodes[0]
        self.assertEqual("certificate", certificate_elem.tagName)
        self.assertEqual(len(certificate_elem.attributes), 2)
        self.assertEqual(
            "sha-1", certificate_elem.getAttribute("fingerprint-algorithm")
        )
        self.assertEqual(
            self.dummy_fingerprint, certificate_elem.getAttribute("fingerprint")
        )

    def test_simple_policy(self):
        """
        Tests that creating a simple policy with a list of domains
        returns a correct policy document.

        """
        domains = ["media.example.com", "api.example.com"]
        policy = policies.Policy(*domains)
        xml_dom = policy.xml_dom

        self.assertEqual(len(xml_dom.documentElement.childNodes), 2)
        self.assertEqual(len(xml_dom.getElementsByTagName("allow-access-from")), 2)

        domains_in_xml = [
            elem.getAttribute("domain")
            for elem in xml_dom.getElementsByTagName("allow-access-from")
        ]
        for domain in domains_in_xml:
            domains.remove(domain)
