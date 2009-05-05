"""
Utilities for generating Flash cross-domain policy files.

"""

import xml.dom


minidom = xml.dom.getDOMImplementation('minidom')

policy_type = minidom.createDocumentType(qualifiedName='cross-domain-policy',
                                         publicId=None,
                                         systemId='http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')

def new_policy_file():
    """
    Create and return a new policy file, as a ``minidom.Document``
    object.
    
    """
    return minidom.createDocument(None, 'cross-domain-policy', policy_type)

def allow_access_from(policy, domain, to_ports=None, secure=None):
    """
    Insert a new ``allow-access-from`` element into ``policy``,
    allowing access from ``domain``.

    ``domain`` may be any valid domain value, but due to security
    concerns it is strongly recommended that wildcard domains be
    avoided.

    If supplied, ``to_ports`` must be a list of valid port numbers or
    port ranges, and will be inserted as the ``to-ports`` attribute of
    the ``allow-access-from`` element.

    If supplied, ``secure`` must be a boolean value, and will be
    inserted as the value of the ``secure`` attribute of the
    ``allow-access-from`` element. Due to security concerns it is
    strongly recommended that you never set this attribute to
    ``False``.
    
    """
    domain_element = policy.createElement('allow-access-from')
    domain_element.setAttribute('domain', domain)
    if to_ports is not None:
        domain_element.setAttribute('to-ports', ','.join(to_ports))
    if secure is not None:
        domain_element.setAttribute('secure', str(secure).lower())
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
