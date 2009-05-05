from django.test import TestCase

from flashpolicy import utils


class PolicyGeneratorTestCase(TestCase):
    """
    Tests for the policy-file generation utilities.
    
    """
    def test_policy_type(self):
        """
        Test that the correct ``DOCTYPE`` declaration is generated.
        
        """
        policy = utils.new_policy_file()
        self.assertEqual(policy.doctype.systemId, 'http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')
        self.assertEqual(policy.doctype.name, 'cross-domain-policy')
        self.assertEqual(len(policy.childNodes), 2)

    def test_policy_root_element(self):
        """
        Test that the correct root element is inserted.
        
        """
        policy = utils.new_policy_file()
        self.assertEqual(policy.documentElement.tagName, 'cross-domain-policy')
        self.assertEqual(len(policy.documentElement.childNodes), 0)

    def test_allow_access_domain(self):
        """
        Test that adding access for a domain inserts the proper
        element and attributes.
        
        """
        policy = utils.new_policy_file()
        utils.allow_access_from(policy, 'media.example.com')
        self.assertEqual(len(policy.documentElement.childNodes), 1)
        self.assertEqual(len(policy.documentElement.getElementsByTagName('allow-access-from')), 1)
        access_elem = policy.documentElement.getElementsByTagName('allow-access-from')[0]
        self.assertEqual(len(access_elem.attributes), 1)
        self.assertEqual(access_elem.getAttribute('domain'), 'media.example.com')
