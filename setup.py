# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from uncaptive import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


if not __version__ or __version__ == '<VERSION>':
    raise RuntimeError("Package version not set!")

requirements = []

setup(
    name="uncaptive",
    author="Aljosha Friemann",
    author_email="a.friemann@automate.wtf",
    description="",
    url="",
    download_url="",
    keywords=[],
    version=__version__,
    license=read('LICENSE.txt'),
    long_description=read('README.rst'),
    install_requires=requirements,
    classifiers=[],
    entry_points={ 'console_scripts': ['uncaptive=uncaptive.cli:daemon'] },
    packages=find_packages(exclude=('test*', 'assets')),
    platforms=[]
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
