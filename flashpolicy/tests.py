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

    def test_policy_root_element(self):
        """
        Test that the correct root element is inserted.
        
        """
        policy = utils.new_policy_file()
        self.assertEqual(policy.documentElement.tagName, 'cross-domain-policy')
