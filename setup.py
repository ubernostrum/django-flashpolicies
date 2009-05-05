from distutils.core import setup
import os

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('flashpolicies'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[13:] # Strip "flashpolicies/" or "flashpolicies\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(name='django-flashpolicies',
      version='0.1',
      description='Flash cross-domain policies for Django sites',
      author='James Bennett',
      author_email='james@b-list.org',
      url='http://bitbucket.org/ubernostrum/django-flashpolicies/overview/',
      package_dir={'flashpolicies': 'flashpolicies'},
      packages=packages,
      package_data={'flashpolicies': data_files},
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
