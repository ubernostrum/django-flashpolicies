import xml.dom.minidom

from django.test import SimpleTestCase

from flashpolicies import policies


class PolicyViewTests(SimpleTestCase):
    """
    Tests the views which serve policy files.

    """

    urls = "flashpolicies.tests.urls"

    def test_serve_response(self):
        """
        Tests that the serve() view returns a byte string response with
        the correct content type and charset.

        """
        response = self.client.get("/crossdomain-serve.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bytes, type(response.content))
        self.assertEqual(
            response["Content-Type"], "text/x-cross-domain-policy; charset=utf-8"
        )

    def test_serve(self):
        """
        Tests that the serve() view serializes the policy as expected.

        """
        response = self.client.get("/crossdomain-serve.xml")

        # Parse the returned policy and make sure it matches what was
        # passed in.
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName("allow-access-from")), 1)
        self.assertEqual(
            len(policy.getElementsByTagName("allow-http-request-headers-from")), 1
        )

    def test_allow_domains(self):
        """
        Tests the allow_domains() view.

        """
        response = self.client.get("/crossdomain-allow-domains.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "text/x-cross-domain-policy; charset=utf-8"
        )
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName("allow-access-from")), 2)
        domains = ["media.example.com", "api.example.com"]
        domains_in_xml = [
            elem.getAttribute("domain")
            for elem in policy.getElementsByTagName("allow-access-from")
        ]
        for domain in domains_in_xml:
            domains.remove(domain)

    def test_allow_domains_alias(self):
        """
        Tests the alias for the allow_domains() view.

        """
        response = self.client.get("/crossdomain-simple-alias.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "text/x-cross-domain-policy; charset=utf-8"
        )
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName("allow-access-from")), 2)
        domains = ["media.example.com", "api.example.com"]
        domains_in_xml = [
            elem.getAttribute("domain")
            for elem in policy.getElementsByTagName("allow-access-from")
        ]
        for domain in domains_in_xml:
            domains.remove(domain)

    def test_no_access(self):
        """
        Tests the view which generates a policy that forbids all
        access.

        """
        response = self.client.get("/crossdomain-no-access.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "text/x-cross-domain-policy; charset=utf-8"
        )
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName("site-control")), 1)
        self.assertEqual(
            policy.getElementsByTagName("site-control")[0].getAttribute(
                "permitted-cross-domain-policies"
            ),
            policies.SITE_CONTROL_NONE,
        )

    def test_metapolicy(self):
        """
        Tests the view which sets a meta-policy for allowing other
        policies on the same domain.

        """
        response = self.client.get("/crossdomain-metapolicy.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "text/x-cross-domain-policy; charset=utf-8"
        )
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName("site-control")), 1)
        self.assertEqual(
            policy.getElementsByTagName("site-control")[0].getAttribute(
                "permitted-cross-domain-policies"
            ),
            policies.SITE_CONTROL_ALL,
        )
