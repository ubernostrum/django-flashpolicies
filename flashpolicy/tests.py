import xml.dom.minidom

from django.test import TestCase

from flashpolicy import policies


class PolicyGeneratorTests(TestCase):
    """
    Tests for the policy-file generation utilities.
    
    """
    def test_policy_type(self):
        """
        Test that the correct ``DOCTYPE`` declaration is generated.
        
        """
        policy = policies.new_policy()
        self.assertEqual(policy.doctype.systemId, 'http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')
        self.assertEqual(policy.doctype.name, 'cross-domain-policy')
        self.assertEqual(len(policy.childNodes), 2)

    def test_policy_root_element(self):
        """
        Test that the correct root element is inserted.
        
        """
        policy = policies.new_policy()
        self.assertEqual(policy.documentElement.tagName, 'cross-domain-policy')
        self.assertEqual(len(policy.documentElement.childNodes), 0)

    def test_allow_access_domain(self):
        """
        Test that adding access for a domain inserts the proper
        element and attributes.
        
        """
        policy = policies.new_policy()
        policies.allow_access_from(policy, 'media.example.com')
        self.assertEqual(len(policy.documentElement.childNodes), 1)
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 1)
        access_elem = policy.getElementsByTagName('allow-access-from')[0]
        self.assertEqual(len(access_elem.attributes), 1)
        self.assertEqual(access_elem.getAttribute('domain'), 'media.example.com')

    def test_site_control(self):
        """
        Test that adding meta-policy information inserts the proper
        element and attributes.
        
        """
        for permitted in ('none', 'master-only', 'by-content-type',
                          'by-ftp-filename', 'all'):
            policy = policies.new_policy()
            policies.site_control(policy, permitted)
            self.assertEqual(len(policy.documentElement.childNodes), 1)
            self.assertEqual(len(policy.getElementsByTagName('site-control')), 1)
            control_elem = policy.getElementsByTagName('site-control')[0]
            self.assertEqual(len(control_elem.attributes), 1)
            self.assertEqual(control_elem.getAttribute('permitted-cross-domain-policies'), permitted)

    def test_simple_policy(self):
        """
        Test that creating a simple policy with a list of domains
        returns a correct policy document.
        
        """
        domains = ['media.example.com', 'api.example.com']
        policy = policies.simple_policy(domains)
        self.assertEqual(len(policy.documentElement.childNodes), 2)
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 2)
        domain_elems = policy.getElementsByTagName('allow-access-from')
        for i, domain in enumerate(domains):
            self.assertEqual(domain,
                             policy.documentElement.getElementsByTagName('allow-access-from')[i].getAttribute('domain'))

    def test_no_access_policy(self):
        """
        Test that creating a policy which permits no access returns a
        correct policy document.
        
        """
        policy = policies.no_access_policy()
        self.assertEqual(len(policy.documentElement.childNodes), 1)
        self.assertEqual(len(policy.getElementsByTagName('site-control')), 1)
        control_elem = policy.getElementsByTagName('site-control')[0]
        self.assertEqual(control_elem.getAttribute('permitted-cross-domain-policies'), 'none')


class PolicyViewTests(TestCase):
    urls = 'flashpolicy.test_urls'

    def test_simple(self):
        response = self.client.get('/crossdomain1.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy')
        policy = xml.dom.minidom.parseString(response.content)
        domains = ['media.example.com', 'api.example.com']
        self.assertEqual(policy.documentElement.tagName, 'cross-domain-policy')
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 2)
        domain_elems = policy.getElementsByTagName('allow-access-from')
        for i, domain in enumerate(domains):
            self.assertEqual(domain,
                             policy.documentElement.getElementsByTagName('allow-access-from')[i].getAttribute('domain'))
