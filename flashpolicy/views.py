from django.http import HttpResponse

from flashpolicy.policies import simple_policy


def simple(request, domains):
    """
    A simple Flash cross-domain access policy.

    **Required arguments:**

    ``domains``
        A list of domains from which to allow access. Each value may
        be either a domain name (e.g., ``example.com``) or a wildcard
        (e.g., ``*.example.com``).

    Due to serious security issues, policies which allow access from
    any domain are not supported.
    
    """
    return HttpResponse(simple_policy(domains).toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')
