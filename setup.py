#!/usr/bin/env python
"""Setup script for nb-init."""

from setuptools import setup, find_packages

setup(
    name='nb-init',
    author='Netbox Initializer',
    description='Netbox initializer using pynetbox',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nb-init=nb_init.cli:main',
        ],
    },
    install_requires=[
        'pynetbox>=6.0.0',
        'PyYAML>=5.4',
        'click>=8.0.0',
    ],
)