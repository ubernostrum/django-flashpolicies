from distutils.core import setup
import os


setup(name='django-flashpolicies',
      version='1.2',
      description='Flash cross-domain policies for Django sites',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.txt')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://bitbucket.org/ubernostrum/django-flashpolicies/overview/',
      download_url='http://bitbucket.org/ubernostrum/django-flashpolicies/downloads/django-flashpolicies-1.1.tar.gz', 
      packages=['flashpolicies'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
