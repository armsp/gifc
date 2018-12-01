#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 setup.py install [--user --prefix=]

from setuptools import setup

setup(
    name='gifc',
    version='0.0.2',
    packages=['gifc'],
    entry_points={
        'console_scripts': [
            'gifc = gifc.__main__:main'
        ]
    }
)
