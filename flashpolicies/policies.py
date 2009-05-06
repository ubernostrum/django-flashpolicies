"""
Utilities for generating Flash cross-domain policy files.

Note that the API of this module is not stable and may change
significantly and without warning in future releases of this
application.

"""

import xml.dom


minidom = xml.dom.getDOMImplementation('minidom')


#
# Acceptable values for the "permitted-cross-domain-policies"
# attribute of "site-control" elements. See section 3(b)(i) of the
# Adobe crossdomain.xml spec.
#

SITE_CONTROL_ALL = "all"
SITE_CONTROL_BY_CONTENT_TYPE = "by-content-type"
SITE_CONTROL_BY_FTP_FILENAME = "by-ftp-filename"
SITE_CONTROL_MASTER_ONLY = "master-only"
SITE_CONTROL_NONE = "none"

VALID_SITE_CONTROL = (SITE_CONTROL_ALL,
                      SITE_CONTROL_BY_CONTENT_TYPE,
                      SITE_CONTROL_BY_FTP_FILENAME,
                      SITE_CONTROL_MASTER_ONLY,
                      SITE_CONTROL_NONE)

def new_policy():
    """
    Create and return a new policy file, as a ``minidom.Document``
    object.
    
    """
    policy_type = minidom.createDocumentType(qualifiedName='cross-domain-policy',
                                             publicId=None,
                                             systemId='http://www.adobe.com/xml/dtds/cross-domain-policy.dtd')
    return minidom.createDocument(None, 'cross-domain-policy', policy_type)

def allow_access_from(policy, domain, to_ports=None):
    """
    Insert a new ``allow-access-from`` element into ``policy``,
    allowing access from ``domain``.

    ``domain`` may be any valid domain value, but due to security
    concerns it is strongly recommended that wildcard domains be
    avoided.

    If supplied, ``to_ports`` should be a comma-separated list of port
    numbers or port ranges.

    """
    domain_element = policy.createElement('allow-access-from')
    domain_element.setAttribute('domain', domain)
    if to_ports is not None:
        domain_element.setAttribute('to-ports', to_ports)
    policy.documentElement.appendChild(domain_element)

def site_control(policy, permitted):
    """
    Insert a ``site-control`` element into ``policy``, using
    ``permitted`` as the value of the
    ``permitted-cross-domain-policies`` attribute.
    
    """
    if permitted not in VALID_SITE_CONTROL:
        raise TypeError('"%s" is not a valid value for the "permitted-cross-domain-policies" attribute of a site-control element' % permitted)
    control_element = policy.createElement('site-control')
    control_element.setAttribute('permitted-cross-domain-policies', permitted)
    policy.documentElement.appendChild(control_element)

def simple_policy(domains):
    """
    Given a list of valid domain values, create a simple policy file
    allowing access from those domains and return the resulting XML as
    a ``minidom.Document`` object.
    
    """
    policy = new_policy()
    for domain in domains:
        allow_access_from(policy, domain)
    return policy

def no_access_policy():
    """
    Create a policy file which permits no access of any sort and
    return the resulting XML as a ``minidom.Document`` object.
    
    """
    policy = new_policy()
    site_control(policy, permitted='none')
    return policy
