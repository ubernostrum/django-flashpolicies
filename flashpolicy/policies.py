"""
Utilities for generating Flash cross-domain policy files.

"""

import xml.dom


minidom = xml.dom.getDOMImplementation('minidom')

def new_policy_file():
    """
    Create and return a new policy file, as a ``minidom.Document``
    object.
    
    """
    policy_type = minidom.createDocumentType(qualifiedName='cross-domain-policy',
                                             publicId=None,
                                             systemId='http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')
    return minidom.createDocument(None, 'cross-domain-policy', policy_type)

def allow_access_from(policy, domain, to_ports=None, secure=None):
    """
    Insert a new ``allow-access-from`` element into ``policy``,
    allowing access from ``domain``.

    ``domain`` may be any valid domain value, but due to security
    concerns it is strongly recommended that wildcard domains be
    avoided.

    """
    domain_element = policy.createElement('allow-access-from')
    domain_element.setAttribute('domain', domain)
    policy.documentElement.appendChild(domain_element)

def site_control(policy, permitted):
    """
    Insert a ``site-control`` element into ``policy``, using
    ``permitted`` as the value of the
    ``permitted-cross-domain-policies`` attribute.
    
    """
    control_element = policy.createElement('site-control')
    control_element.setAttribute('permitted-cross-domain-policies', permitted)
    policy.documentElement.appendChild(control_element)

def simple_policy_file(domains):
    """
    Given a list of valid domain values, create a simple policy file
    allowing access from those domains and return the resulting XML as
    a string.
    
    """
    policy = new_policy_file()
    for domain in domains:
        allow_access_from(policy, domain)
    return policy.toprettyxml()

def no_access_policy_file():
    """
    Create a policy file which permits no access of any sort and
    return the resulting XML as a string.
    
    """
    policy = new_policy_file()
    site_control(policy, permitted='none')
    return policy.toprettyxml()
