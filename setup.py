#!/usr/bin/env python

from setuptools import setup

setup(
    name='PyTrie',
    version='0.3',
    author='George Sakkis',
    author_email='george.sakkis@gmail.com',
    url='https://github.com/gsakkis/pytrie/',
    description='A pure Python implementation of the trie data structure.',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['pytrie'],
    install_requires=['sortedcontainers'],
    test_suite='tests',
)
