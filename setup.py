#!/usr/bin/env python

import sys

from distutils.core import setup
from DeComp import __version__, __license__
# this affects the names of all the directories we do stuff with
sys.path.insert(0, './')

#__version__ = os.getenv('VERSION', default='9999')

setup(
    name='pyDeComp',
    version=__version__,
    description="A Python library for subprocessing various compression "
        "and decompression routines.  Including generating contents listings",
    author='Brian Dolbec',
    author_email='dolsen@gentoo.org',
    url="https://github.com/dol-sen/pyDeComp",
    packages=['DeComp'],
    license=__license__,
    long_description=open('README').read(),
    keywords='archive',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Compression',
    ],
)
