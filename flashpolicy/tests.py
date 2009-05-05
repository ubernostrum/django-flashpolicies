from django.test import TestCase

from flashpolicy import policies


class PolicyGeneratorTestCase(TestCase):
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
        self.assertEqual(len(policy.documentElement.getElementsByTagName('allow-access-from')), 1)
        access_elem = policy.documentElement.getElementsByTagName('allow-access-from')[0]
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
            self.assertEqual(len(policy.documentElement.getElementsByTagName('site-control')), 1)
            control_elem = policy.documentElement.getElementsByTagName('site-control')[0]
            self.assertEqual(len(control_elem.attributes), 1)
            self.assertEqual(control_elem.getAttribute('permitted-cross-domain-policies'), permitted)

    def test_simple_policy(self):
        """
        Test that creating a simple policy with a list of domains
        returns a correct policy document.
        
        """
        domains = ['media.example.com', 'api.example.com']
        policy = policies.simple_policy(domains)
        self.assertEqual(len(policy.documentElement.getElementsByTagName('allow-access-from')), 2)
