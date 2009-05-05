from django.http import HttpResponse

from flashpolicy import policies


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
    return HttpResponse(policies.simple_policy(domains).toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')

def no_access(request):
    """
    A Flash cross-domain access policy which permits no access of any
    kind.
    
    """
    return HttpResponse(policies.no_access_policy().toprettyxml(encoding='utf-8'),
                        content_type='text/x-cross-domain-policy')
