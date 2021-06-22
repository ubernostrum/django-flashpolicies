.. _install:


Installation guide
==================

The |release| release of django-flashpolicies supports Django 2.2,
3.1, and 3.2 on Python 3.6, 3.7, 3.8, and 3.9.


Normal installation
-------------------

The preferred method of installing django-flashpolicies is via `pip`,
the standard Python package-installation tool. If you don't have
`pip`, instructions are available for `how to obtain and install it
<https://pip.pypa.io/en/latest/installing.html>`_, though if you're
using a supported version of Python, `pip` should have come bundled
with your installation of Python.

Once you have `pip`, type::

    pip install django-flashpolicies

If you don't have a copy of a compatible version of Django, this will
also automatically install one for you, and will install a third-party
library required by some of django-flashpolicies's validation code.


Installing from a source checkout
---------------------------------

If you want to work on django-flashpolicies, you can obtain a source
checkout.

The development repository for django-flashpolicies is at
<https://github.com/ubernostrum/django-flashpolicies>. If you have `git
<http://git-scm.com/>`_ installed, you can obtain a copy of the
repository by typing::

    git clone https://github.com/ubernostrum/django-flashpolicies.git

From there, you can use git commands to check out the specific
revision you want, and perform an "editable" install (allowing you to
change code as you work on it) by typing::

    pip install -e .


Next steps
----------

To get up and running quickly, check out :ref:`the views documentation
<views>`.