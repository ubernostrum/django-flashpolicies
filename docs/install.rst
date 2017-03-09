.. _install:


Installation guide
==================

Before installing django-flashpolicies, you'll need to have a copy of
`Django <https://www.djangoproject.com>`_ already installed. For
information on obtaining and installing Django, consult the `Django
download page <https://www.djangoproject.com/download/>`_, which offers
convenient packaged downloads and installation instructions.

The |version| release of django-flashpolicies supports Django 1.8,
1.9, and 1.10, on the following Python versions:

* Django 1.8 suports Python 2.7, 3.3, 3.4 and 3.5.

* Django 1.9 supports Python 2.7, 3.4 and 3.5.

* Django 1.10 supports Python 2.7, 3.4 and 3.5.

It is expected that django-flashpolicies |version| will work
without modification on Python 3.6 once it is released.

.. important:: **Python 3.2**

   Although Django 1.8 supported Python 3.2 at the time of its
   release, the Python 3.2 series has reached end-of-life, and as a
   result support for Python 3.2 has been dropped from
   django-flashpolicies.


Normal installation
-------------------

The preferred method of installing django-flashpolicies is via
``pip``, the standard Python package-installation tool. If you don't
have ``pip``, instructions are available for `how to obtain and
install it <https://pip.pypa.io/en/latest/installing.html>`_. If
you're using Python 2.7.9 or later (for Python 2) or Python 3.4 or
later (for Python 3), ``pip`` came bundled with your installation of
Python.

Once you have ``pip``, simply type::

    pip install django-flashpolicies


Manual installation
-------------------

It's also possible to install django-flashpolicies manually. To do
so, obtain the latest packaged version from `the listing on the Python
Package Index
<https://pypi.python.org/pypi/django-flashpolicies/>`_. Unpack the
``.tar.gz`` file, and run::

    python setup.py install

Once you've installed django-flashpolicies, you can verify successful
installation by opening a Python interpreter and typing ``import
flashpolicies``.

If the installation was successful, you'll simply get a fresh Python
prompt. If you instead see an ``ImportError``, check the configuration
of your install tools and your Python import path to ensure
django-flashpolicies installed into a location Python can import from.


Installing from a source checkout
---------------------------------

The development repository for django-flashpolicies is at
<https://github.com/ubernostrum/django-flashpolicies>. Presuming you have `git
<http://git-scm.com/>`_ installed, you can obtain a copy of the
repository by typing::

    git clone https://github.com/ubernostrum/django-flashpolicies.git

From there, you can use normal git commands to check out the specific
revision you want, and install it using ``python setup.py install``.


Running tests
-------------

If you have django-flashpolicies installed already, you can add it to
the ``INSTALLED_APPS` of a Django project and use ``manage.py test``
as normal. However, some conveniences are provided for testing without
a project. The simplest way, from an already-installed copy of
django-flashpolicies, is (from the ``flashpolicies/`` directory) to
run ``python runtests.py``, which will set up a minimal runtime
configuration for Django and execute the tests.

From a source checkout, you can also use the included
``Makefile``. Executing ``make test`` will install Django (by default,
the latest 1.10 release), [flake8](http://flake8.pycqa.org/), and
[coverage.py](https://coverage.readthedocs.io/), fun flake8 on
django-flashpolicies' source code, execute the test suite and print a
coverage report. You can also select the Django release series to use
by either setting the environment variable ``DJANGO_VERSION`` before
running ``make test``, or by passing the variable on the command line
when running tests. For example, to run the tests using Django 1.9::

    make test DJANGO_VERSION=1.9

If you have [pyenv](https://github.com/pyenv/pyenv) and
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv), the
included ``Makefile`` supports creating and cleaning up a virtual
environment. Run ``make venv`` to create and locally activate (via
``pyenv local``) the virtual environment; by default this uses Python
3.6.0 (and will *not* install a Python version you don't already
have), but you can select a Python version by setting or passing the
variable ``PYTHON_VERSION``. For example, to use Python 3.5.3::

    make venv PYTHON_VERSION=3.5.3

The virtual environment will be named ``flashpolicies_test``.

The full set of supported ``make`` targets is:

* ``clean`` -- Cleans the local directory and environment by running
  ``python setup.py clean``, removing build and test artifacts and
  ``.pyc`` files, and uninstalling Django. Useful for re-using a
  virtual environment to test against multiple versions of Django.

* ``django`` -- installs Django, defaulting to the latest 1.10 but
  configurable via the variable ``DJANGO_VERSION``.

* ``venv`` -- create and locally activate a a virtual environment,
  defaulting to Python 3.6.0 but configurable via the variable
  ``PYTHON_VERSION``.

* ``lint`` -- runs flake8 over django-flashpolicies' source code,
  using configuration specified in django-flashpolicies' ``setup.cfg``
  file. Executes ``test_deps`` as a dependency.

* ``teardown`` -- Executes ``clean``, and also deactivates and deletes
  the virtual environment created by ``venv``.

* ``test_dependencies`` -- installs dependencies for testing (coverage.py and
  flake8).

* ``test`` -- Executes ``django`` and ``lint`` as dependencies,
  performs a local editable install of django-flashpolicies (via ``pip
  install -e``), and runs the test suite and a coverage report, using
  configuration from django-flashpolicies' ``setup.cfg`` file.

You can, as expected, combine targets in a single run, allowing a
complete cycle of creating a virtual environment, running tests and
tearing down the virtual environment in a single command::

    make venv test teardown
