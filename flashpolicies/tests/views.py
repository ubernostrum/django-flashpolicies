import xml.dom.minidom

from django.test import TestCase

from flashpolicies import policies


class PolicyViewTests(TestCase):
    """
    Tests for the views which serve policy files.

    """
    urls = 'flashpolicies.tests.urls'

    def test_serve(self):
        """
        Test the view which simply serves a policy.

        """
        response = self.client.get('/crossdomain4.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'],
                         'text/x-cross-domain-policy; charset=utf-8')

        # Parse the returned policy and make sure it matches what was
        # passed in.
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 1)
        self.assertEqual(len(policy.getElementsByTagName('allow-http-request-headers-from')), 1)

    def test_simple(self):
        """
        Test the view which generates a simple (i.e., list of domains)
        policy.

        """
        response = self.client.get('/crossdomain1.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy; charset=utf-8')
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 2)
        domain_elems = policy.getElementsByTagName('allow-access-from')
        domains = ['media.example.com', 'api.example.com']
        for i, domain in enumerate(domains):
            self.assertEqual(domain,
                             policy.getElementsByTagName('allow-access-from')[i].getAttribute('domain'))

    def test_no_access(self):
        """
        Test the view which generates a policy that forbids all
        access.

        """
        response = self.client.get('/crossdomain2.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy; charset=utf-8')
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('site-control')), 1)
        self.assertEqual(policy.getElementsByTagName('site-control')[0].getAttribute('permitted-cross-domain-policies'),
                         policies.SITE_CONTROL_NONE)

    def test_metapolicy(self):
        """
        Test the view which sets a meta-policy for allowing other
        policies on the same domain.

        """
        response = self.client.get('/crossdomain3.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy; charset=utf-8')
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('site-control')), 1)
        self.assertEqual(policy.getElementsByTagName('site-control')[0].getAttribute('permitted-cross-domain-policies'),
                         policies.SITE_CONTROL_ALL)
