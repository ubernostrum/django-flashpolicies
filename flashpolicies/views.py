"""
Views for generating and serving policy files.

"""

from django.http import HttpResponse

from flashpolicies import policies


def serve(request, policy):
    """
    Given a ``flashpolicies.policies.Policy`` instance, serialize it
    to XML and serve it. Internally, this is used by all other views as
    the mechanism which actually serves the policy file.

    **Required arguments:**

    ``policy``
        The ``flashpolicies.policies.Policy`` instance to serve.

    **Optional arguments:**

    None.

    """
    return HttpResponse(str(policy),
                        content_type='text/x-cross-domain-policy; charset=utf-8')


def simple(request, domains):
    """
    A simple Flash cross-domain access policy.

    Note that if this is returned from the URL ``/crossdomain.xml`` on
    a domain, it will act as a master policy and will not permit other
    policies to exist on that domain. If you need to set meta-policy
    information and allow other policies, use the view
    :view:`flashpolicies.views.metapolicy` for the master policy instead.

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
    return serve(request, policies.Policy(*domains))


def metapolicy(request, permitted, domains=None):
    """
    A Flash cross-domain policy which allows other policies to exist
    on the same domain.

    Note that this view, if used, must be the master policy for the
    domain, and so must be served from the URL ``/crossdomain.xml`` on
    the domain: setting metapolicy information in other policy files
    is forbidden by the cross-domain policy specification.

    **Required arguments:**

    ``permitted``
        A string indicating the extent to which other policies are
        permitted. A set of constants is available in
        ``flashpolicies.policies``, defining acceptable values for
        this argument.

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
    policy.metapolicy(permitted)
    return serve(request, policy)


def no_access(request):
    """
    A Flash cross-domain access policy which permits no access of any
    kind, via a metapolicy declaration disallowing all policy files.

    Note that this view, if used, must be the master policy for the
    domain, and so must be served from the URL ``/crossdomain.xml`` on
    the domain: setting metapolicy information in other policy files
    is forbidden by the cross-domain policy specification.

    **Required arguments:**

    None.

    **Optional arguments:**

    None.

    """
    return metapolicy(request,
                      permitted=policies.SITE_CONTROL_NONE)
