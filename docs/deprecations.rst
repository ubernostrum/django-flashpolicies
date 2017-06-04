.. _deprecations:


Feature and API deprecation cycle
=================================

The following features or APIs of django-flashpolicies are deprecated
and scheduled to be removed in future releases. Please make a note of
this and update your use of django-flashpolicies accordingly. When
possible, deprecated features will emit a ``DeprecationWarning`` as an
additional warning of pending removal.


The ``flashpolicies.views.simple`` view
---------------------------------------

**Will be removed in:** django-flashpolicies 2.0

This view has been renamed to
:func:`~flashpolicies.views.allow_domains` to better communicate its
purpose. The view ``flashpolicies.views.simple`` continues to exist
for now as an alias for backwards compatibility, but will be removed
(and emits a ``DeprecationWarning``).


The ``flashpolicies`` combined package
--------------------------------------

**Will be removed in:** django-flashpolicies 2.0

For the 2.0 release, django-flashpolicies will be split into two
packages. One -- which will be named "flashpolicies" and provide a
Python module named ``flashpolicies`` -- will contain the
:class:`~flashpolicies.policies.Policy` class and associated code,
which are not dependent on Django in any way. The Django views for
serving policies will become a separate package, retaining the name
"django-flashpolicies" on the Python Package Index and providing a
module named ``django_flashpolicies``.