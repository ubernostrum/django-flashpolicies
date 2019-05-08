.. _deprecations:


Feature and API deprecation cycle
=================================

The following features or APIs of django-flashpolicies are deprecated
and scheduled to be removed in future releases. Please make a note of
this and update or plan your use of django-flashpolicies
accordingly. When possible, deprecated features will emit a
:exc:`DeprecationWarning` as an additional warning of pending removal.


The `flashpolicies.views.simple` view
-------------------------------------

**Will be removed in:** django-flashpolicies 2.0

This view has been renamed to
:func:`~flashpolicies.views.allow_domains` to better communicate its
purpose. The view `flashpolicies.views.simple` continues to exist for
now as an alias for backwards compatibility, but will be removed (and
emits a :exc:`DeprecationWarning`).


The `flashpolicies` package name
--------------------------------

**Will be removed in:** django-flashpolicies 2.0

Currently, django-flashpolicies installs a Python module named
`flashpolicies`. For the 2.0 release, this will change to
`django_flashpolicies`.