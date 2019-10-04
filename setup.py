#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from docs_italia_convertitore_web/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\']([^'\']*)['\']", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version('docs_italia_convertitore_web', '__init__.py')


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print('Wheel version: ', wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print('Tagging the version on git:')
    os.system('git tag -a %s -m "version %s"' % (version, version))
    os.system('git push --tags')
    sys.exit()

readme = codecs.open('README.rst', 'r', 'utf-8').read()
requirements = codecs.open('requirements.txt', 'r', 'utf-8').readlines()
history = codecs.open('HISTORY.rst', 'r', 'utf-8').read().replace('.. :changelog:', '')

setup(
    name='docs-italia-convertitore-web',
    version=version,
    description="""Applicazione Django che si interfaccia con il convertitore pandoc""",
    long_description=readme + '\n\n' + history,
    author='Team Digitale',
    author_email='',
    url='https://github.com/italia/docs-italia-convertitore-web',
    packages=[
        'docs_italia_convertitore_web',
    ],
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    keywords='docs-italia-convertitore-web',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
