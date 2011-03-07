#!/usr/bin/env python
from distutils.core import setup
import os
from helios import __version__


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
	os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('helios'):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		pkg = dirpath.replace(os.path.sep, '.')
		if os.path.altsep:
			pkg = pkg.replace(os.path.altsep, '.')
		packages.append(pkg)
	elif filenames:
		prefix = dirpath[5:] # Strip "helios/" or "helios\"
		for f in filenames:
			data_files.append(os.path.join(prefix, f))

setup(name='helios',
	version=__version__,
	description='Phaethon\'s e-commerce application.',
	author='Panos Laganakos',
	author_email='panos.laganakos@gmail.com',
	packages=packages,
	package_dir={'helios': 'helios'},
	package_data={'helios': data_files},
	classifiers=['Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Utilities'],
)
