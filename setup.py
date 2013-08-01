from distutils.core import setup
import os


setup(name='django-flashpolicies',
      version='1.5',
      description='Flash cross-domain policies for Django sites',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://bitbucket.org/ubernostrum/django-flashpolicies/overview/',
      download_url='http://bitbucket.org/ubernostrum/django-flashpolicies/downloads/django-flashpolicies-1.5.tar.gz', 
      packages=['flashpolicies', 'flashpolicies.tests'],
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
                   'Topic :: Utilities'],
      )
