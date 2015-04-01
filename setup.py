import os

from setuptools import setup


setup(name='django-flashpolicies',
      version='1.6b1',
      description='Flash cross-domain policies for Django sites',
      long_description=open(os.path.join(os.path.dirname(__file__),
                                         'README')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://github.com/ubernostrum/django-flashpolicies/',
      packages=['flashpolicies', 'flashpolicies.tests'],
      test_suite='flashpolicies.runtests.run_tests',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Utilities'],
      )
