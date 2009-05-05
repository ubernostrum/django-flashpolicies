"""
Utilities for generating Flash cross-domain policy files.

"""

import xml.dom


minidom = xml.dom.getDOMImplementation('minidom')

policy_type = minidom.createDocumentType(qualifiedName='cross-domain-policy',
                                         publicId=None,
                                         systemId='http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')

def simple_policy_file(domains):
    """
    Given a list of valid domain values, create a simple policy file
    allowing access from those domains and return the resulting XML as
    a string.
    
    """
    policy_doc = minidom.createDocument(None, 'cross-domain-policy', policy_type)
    policy = policy_doc.documentElement
    for domain in domains:
        domain_element = policy_doc.createElement('allow-access-from')
        domain_element.setAttribute('domain', domain)
        policy.appendChild(domain_element)
    return policy_doc.toprettyxml()
