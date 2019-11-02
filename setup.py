#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

REQUIREMENTS = [
    'Click==7.0',
    'paramiko==2.6.0'
]

setup(
    name='vmdiag',
    version='1.0',
    description='Simple VM diagnostics tool',
    long_description=README,
    author='Andrés Arias',
    author_email='andres.arias12@gmail.com',
    url='https://github.com/andres-arias/VMDiag',
    install_requires=REQUIREMENTS,
    keywords=['vm', 'cloud', 'aws', 'cpu', 'memory', 'processes'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Development Status :: 3 - Alpha'
    ],
    entry_points={
        'console_scripts': ['vmdiag = vmdiag.vmdiag:main']
    },
)
