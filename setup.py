# -*- coding: utf-8 -*-
"""
    robo
    ~~~~

    Dead simple bot framework.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages

requires = ['blinker']

app_name = 'robo'

rst_path = os.path.join(os.path.dirname(__file__), 'README.rst')
description = ''
with open(rst_path) as f:
    description = f.read()

setup(
    name=app_name,
    version='0.5.6',
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-robo',
    description='Dead simple bot framework.',
    long_description=description,
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests', 'examples']),
    package_dir={'': '.'},
    install_requires=requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing'
    ],
    tests_require=['blinker'],
    test_suite='tests'
)
