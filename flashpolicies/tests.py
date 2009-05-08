import xml.dom.minidom

from django.test import TestCase

from flashpolicies import policies


class PolicyGeneratorTests(TestCase):
    """
    Tests for the policy-file generation utilities.
    
    """
    def test_policy_type(self):
        """
        Test that the correct ``DOCTYPE`` declaration is generated.
        
        """
        policy = policies.Policy().xml_dom
        self.assertEqual(policy.doctype.systemId, 'http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')
        self.assertEqual(policy.doctype.name, 'cross-domain-policy')
        self.assertEqual(len(policy.childNodes), 2)

    def test_policy_root_element(self):
        """
        Test that the correct root element is inserted.
        
        """
        policy = policies.Policy().xml_dom
        self.assertEqual(policy.documentElement.tagName, 'cross-domain-policy')
        self.assertEqual(len(policy.documentElement.childNodes), 0)

    def test_allow_access_domain(self):
        """
        Test that adding access for a domain inserts the proper
        element and attribute.
        
        """
        policy = policies.Policy()
        policy.allow_domain('media.example.com')
        xml_dom = policy.xml_dom
        self.assertEqual(len(xml_dom.documentElement.childNodes), 1)
        self.assertEqual(len(xml_dom.getElementsByTagName('allow-access-from')), 1)
        access_elem = xml_dom.getElementsByTagName('allow-access-from')[0]
        self.assertEqual(len(access_elem.attributes), 1)
        self.assertEqual(access_elem.getAttribute('domain'), 'media.example.com')

    def test_allow_access_ports(self):
        """
        Test that adding port access for socket connections inserts
        the proper attribute.
        
        """
        policy = policies.Policy()
        ports = ['80', '8080', '9000-1000']
        policy.allow_domain('media.example.com', to_ports=ports)
        access_elem = policy.xml_dom.getElementsByTagName('allow-access-from')[0]
        self.assertEqual(len(access_elem.attributes), 2)
        self.assertEqual(access_elem.getAttribute('to-ports'), ','.join(ports))

    def test_allow_access_secure(self):
        """
        Test that setting non-secure access for a domain inserts the
        proper attribute.
        
        """
        policy = policies.Policy()
        policy.allow_domain('media.example.com', secure=False)
        access_elem = policy.xml_dom.getElementsByTagName('allow-access-from')[0]
        self.assertEqual(len(access_elem.attributes), 2)
        self.assertEqual(access_elem.getAttribute('secure'), 'false')

    def test_site_control(self):
        """
        Test that adding meta-policy information inserts the proper
        element and attributes.
        
        """
        for permitted in policies.VALID_SITE_CONTROL:
            policy = policies.Policy()
            policy.metapolicy(permitted)
            xml_dom = policy.xml_dom
            self.assertEqual(len(xml_dom.documentElement.childNodes), 1)
            self.assertEqual(len(xml_dom.getElementsByTagName('site-control')), 1)
            control_elem = xml_dom.getElementsByTagName('site-control')[0]
            self.assertEqual(len(control_elem.attributes), 1)
            self.assertEqual(control_elem.getAttribute('permitted-cross-domain-policies'), permitted)

    def test_allow_http_headers(self):
        """
        Test that allowing HTTP headers inserts the proper element and
        attributes.
        
        """
        domain = 'media.example.com'
        headers = ['SomeHeader', 'SomeOtherHeader']
        policy = policies.Policy()
        policy.allow_headers(domain, headers, secure=False)
        xml_dom = policy.xml_dom
        self.assertEqual(len(xml_dom.getElementsByTagName('allow-http-request-headers-from')), 1)
        header_elem = xml_dom.getElementsByTagName('allow-http-request-headers-from')[0]
        self.assertEqual(len(header_elem.attributes), 3)
        self.assertEqual(header_elem.getAttribute('domain'), domain)
        self.assertEqual(header_elem.getAttribute('headers'), ','.join(headers))
        self.assertEqual(header_elem.getAttribute('secure'), 'false')

    def test_allow_http_headers_secure(self):
        """
        Test that setting non-secure access for HTTP headers from a
        domain inserts the proper attribute.
        
        """
        domain = 'media.example.com'
        headers = ['SomeHeader', 'SomeOtherHeader']
        policy = policies.Policy()
        policy.allow_headers(domain, headers, secure=False)
        xml_dom = policy.xml_dom
        header_elem = xml_dom.getElementsByTagName('allow-http-request-headers-from')[0]
        self.assertEqual(len(header_elem.attributes), 3)
        self.assertEqual(header_elem.getAttribute('secure'), 'false')

    def test_bad_site_control(self):
        """
        Test that meta-policies are restricted to the values permitted
        by the specification.
        
        """
        policy = policies.Policy()
        self.assertRaises(TypeError, policy.site_control, 'not-valid')

    def test_element_order(self):
        """
        Test that when multiple types of elements are present in the
        XML, they occur in the order mandated by the DTD, regardless
        of the order in which the relevant options were applied.
        
        """
        domain = 'media.example.com'
        header_elem = { 'domain': 'media.example.com', 'headers': ['SomeHeader', 'SomeOtherHeader'] }
        site_control = policies.SITE_CONTROL_ALL

        # This policy has methods called in the proper order for the DTD.
        policy1 = policies.Policy()
        policy1.metapolicy(site_control)
        policy1.allow_domain(domain)
        policy1.allow_headers(**header_elem)

        # This policy has methods called in reverse order.
        policy2 = policies.Policy()
        policy2.allow_headers(**header_elem)
        policy2.allow_domain(domain)
        policy2.metapolicy(site_control)

        # This policy has methods called in no particular order.
        policy3 = policies.Policy()
        policy3.allow_domain(domain)
        policy3.allow_headers(**header_elem)
        policy3.metapolicy(site_control)

        for policy in (policy1, policy2, policy3):
            root = policy.xml_dom.documentElement
            self.assertEqual(len(root.childNodes), 3)
            self.assertEqual(root.childNodes[0].tagName, 'site-control')
            self.assertEqual(root.childNodes[1].tagName, 'allow-access-from')
            self.assertEqual(root.childNodes[2].tagName, 'allow-http-request-headers-from')

    def test_simple_policy(self):
        """
        Test that creating a simple policy with a list of domains
        returns a correct policy document.
        
        """
        domains = ['media.example.com', 'api.example.com']
        policy = policies.Policy(*domains)
        xml_dom = policy.xml_dom
        self.assertEqual(len(xml_dom.documentElement.childNodes), 2)
        self.assertEqual(len(xml_dom.getElementsByTagName('allow-access-from')), 2)
        domain_elems = xml_dom.getElementsByTagName('allow-access-from')
        for i, domain in enumerate(domains):
            self.assertEqual(domain,
                             xml_dom.documentElement.getElementsByTagName('allow-access-from')[i].getAttribute('domain'))


class PolicyViewTests(TestCase):
    urls = 'flashpolicies.test_urls'

    def test_simple(self):
        """
        Test the view which generates a simple (i.e., list of domains)
        policy.
        
        """
        response = self.client.get('/crossdomain1.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy')
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
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy')
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
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy')
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('site-control')), 1)
        self.assertEqual(policy.getElementsByTagName('site-control')[0].getAttribute('permitted-cross-domain-policies'),
                         policies.SITE_CONTROL_ALL)

    def test_serve_policy(self):
        """
        Test the view which simply serves a policy.
        
        """
        response = self.client.get('/crossdomain4.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/x-cross-domain-policy')

        # Parse the returned policy and make sure it matches what was
        # passed in.
        policy = xml.dom.minidom.parseString(response.content)
        self.assertEqual(len(policy.getElementsByTagName('allow-access-from')), 1)
        self.assertEqual(len(policy.getElementsByTagName('allow-http-request-headers-from')), 1)
