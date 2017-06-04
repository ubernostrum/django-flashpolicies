.. module:: flashpolicies.views


Views for serving cross-domain policies
=======================================

Included in django-flashpolicies are several views for generating and
serving Flash cross-domain policies. Most sites will need no more than
the :func:`~flashpolicies.views.allow_domains` policy-serving view.

Some of the other views here support more advanced use cases, but note
that not all valid policy file options have direct support in these
views. The :class:`~flashpolicies.policies.Policy` class does support
all valid options, however, so instantiating a
:class:`~flashpolicies.policies.Policy`, setting the desired options,
and passing it to the :func:`~flashpolicies.views.serve` view will
allow use of any options policy files can support.

.. function:: serve(request, policy)

   Given a :class:`~flashpolicies.policies.Policy` instance,
   serializes it to UTF-8 and serve it.

   Internally, this is used by all other included views as the
   mechanism which actually serves the policy file.

   :param policy: The :class:`~flashpolicies.policies.Policy` to serve.

.. function:: allow_domains(request, domains)

   Serves a cross-domain access policy allowing a list of domains.

   Note that if this is returned from the URL ``/crossdomain.xml`` on
   a domain, it will act as a master policy and will not permit other
   policies to exist on that domain. If you need to set meta-policy
   information and allow other policies, use the
   :func:`~flashpolicies.views.metapolicy` view for the master policy
   instead.

   :param domains: A list of domains from which to allow access. Each
      value may be either a domain name (e.g., ``"example.com"``) or a
      wildcard (e.g., ``"*.example.com"``). Due to serious potential
      security issues, it is strongly recommended that you not use
      wildcard domain values.

.. function:: metapolicy(request, permitted, domains=None)

   Serves a cross-domain policy which can allow other policies to
   exist on the same domain.

   Note that this view, if used, must be the master policy for the
   domain, and so must be served from the URL ``/crossdomain.xml`` on
   the domain: setting meta-policy information in other policy files
   is forbidden by the cross-domain policy specification.

   :param permitted: A string indicating the extent to which other
      policies are permitted. :ref:`A set of constants is available,
      defining acceptable values for this argument
      <metapolicy-constants>`.
   :param domains: A list of domains from which to allow access. Each
      value may be either a domain name (e.g., ``"example.com"``) or a
      wildcard (e.g., ``"*.example.com"``). Due to serious potential
      security issues, it is strongly recommended that you not use
      wildcard domain values.

.. function:: no_access(request)

   Serves a cross-domain policy which permits no access of any kind,
   via a meta-policy declaration disallowing all policy files.

   Note that this view, if used, must be the master policy for the
   domain, and so must be served from the URL ``/crossdomain.xml`` on
   the domain. Setting meta-policy information in other policy files is
   forbidden by the cross-domain policy specification.

   Internally, this view calls the :func:`metapolicy` view, passing
   :const:`~flashpolicies.policies.SITE_CONTROL_NONE` as the
   meta-policy.
