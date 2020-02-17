"""
Views for generating and serving policy files.

"""

import warnings
from typing import Iterable, Optional

from django.http import HttpRequest, HttpResponse

from . import policies


def serve(request: HttpRequest, policy: policies.Policy) -> HttpResponse:
    """
    Given a ``flashpolicies.policies.Policy`` instance, serializes it
    to XML and serve it.

    Internally, this is used by all other views as the mechanism which
    actually serves the policy file.

    **Required arguments:**

    ``policy``
        The ``flashpolicies.policies.Policy`` instance to serve.

    **Optional arguments:**

    None.

    """
    return HttpResponse(
        policy.serialize(), content_type="text/x-cross-domain-policy; charset=utf-8"
    )


def allow_domains(request: HttpRequest, domains: Iterable[str]) -> HttpResponse:
    """
    Serves a cross-domain access policy allowing a list of domains.

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


def simple(request: HttpRequest, domains: Iterable[str]) -> HttpResponse:
    """
    Deprecated name for the ``allow_domains`` view.

    """
    warnings.warn(
        "flashpolicies.views.simple has been renamed to "
        "flashpolicies.views.allow_domains. Support for referring to it as "
        "flashpolicies.views.simple is deprecated and will be removed in a "
        "future release of django-flashpolicies.",
        DeprecationWarning,
    )
    return allow_domains(request, domains)


def metapolicy(
    request: HttpRequest, permitted: str, domains: Optional[Iterable[str]] = None
) -> HttpResponse:
    """
    Serves a cross-domain policy which can allow other policies
    to exist on the same domain.

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


def no_access(request: HttpRequest) -> HttpResponse:
    """
    Serves a cross-domain access policy which permits no access of any
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
    return metapolicy(request, permitted=policies.SITE_CONTROL_NONE)
