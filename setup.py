#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit(
        'Python < 3.6 is not supported. You are using Python {}.{}.'.format(
            sys.version_info[0], sys.version_info[1])
    )

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit claml2transmart/__version__.py
version = {}
with open(os.path.join(here, 'claml2transmart', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt', 'r') as f:
    required_packages = f.read().splitlines()

setup(
    name='claml2transmart',
    version=version['__version__'],
    description="Example ClaML to TranSMART loader",
    long_description=readme + '\n\n',
    author="Gijs Kant",
    author_email='gijs@thehyve.nl',
    url='https://github.com/thehyve/python_claml2transmart',
    packages=[
        'claml2transmart',
    ],
    package_dir={'claml2transmart':
                 'claml2transmart'},
    entry_points={
        'console_scripts': ['claml2transmart=claml2transmart.claml2transmart:main'],
    },
    include_package_data=True,
    license="GNU General Public License v3 or later",
    zip_safe=False,
    keywords='claml2transmart',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    python_requires='>=3.6.0',
    install_requires=required_packages,
    setup_requires=[
        'pygments',
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark',
        # dependency for `python setup.py bdist_wheel`
        'wheel'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
    extras_require={
        'dev':  ['prospector[with_pyroma]', 'yapf', 'isort'],
    }
)
