from django.http import HttpResponse

from flashpolicies import policies


def simple(request, domains):
    """
    A simple Flash cross-domain access policy.

    Note that if this is returned from the URL ``/crossdomain.xml`` on
    a domain, it will act as a master policy and will not permit other
    policies to exist on that domain. If you need to set meta-policy
    information and allow other policies, use the view
    ``flashpolicies.views.metapolicy`` for the master policy instead.

    **Required arguments:**

    ``domains``
        A list of domains from which to allow access. Each value may
        be either a domain name (e.g., ``example.com``) or a wildcard
        (e.g., ``*.example.com``). Due to serious potential security
        issues, it is strongly recommended that you not use wildcard
        domain values.

    **Optional arguments:**

    None.
    
    """
    return HttpResponse(policies.Policy(*domains).xml_dom.toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')

def no_access(request):
    """
    A Flash cross-domain access policy which permits no access of any
    kind, via a meta-policy disallowing all policy files.
    
    Note that this view, if used, must become the master policy for
    the domain, and so must be served from the URL
    ``/crossdomain.xml`` on the domain -- setting meta-policy
    information in other policy files is forbidden by the
    specification.

    **Required arguments:**

    None.

    **Optional arguments:**

    None.
    
    """
    policy = policies.Policy()
    policy.metapolicy(policies.SITE_CONTROL_NONE)
    return HttpResponse(policy.xml_dom.toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')

def metapolicy(request, site_control, domains=None):
    """
    A Flash cross-domain policy which allows other policies to exist
    on the same domain.

    Note that this view, if used, must become the master policy for
    the domain, and so must be served from the URL
    ``/crossdomain.xml`` on the domain -- setting meta-policy
    information in other policy files is forbidden by the
    specification.

    **Required arguments:**

    ``site_control``
        A string indicating the extent to which other policies are
        permitted. Value values are defined as constants in
        ``flashpolicies.policies``.

    **Optional arguments:**

    ``domains``
        A list of domains from which to allow access. Each value may
        be either a domain name (e.g., ``example.com``) or a wildcard
        (e.g., ``*.example.com``). Due to serious potential security
        issues, it is strongly recommended that you not use wildcard
        domain values.
    
    """
    if domains is None:
        domains = []
    policy = policies.Policy(*domains)
    policy.metapolicy(site_control)
    return HttpResponse(policy.xml_dom.toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')
