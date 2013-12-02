#!/usr/bin/env python

from distutils.core import setup

setup(
    name            = 'PyTrie',
    version         = '0.2',
    author          = 'George Sakkis',
    author_email    = 'george.sakkis@gmail.com',
    url             = 'http://bitbucket.org/gsakkis/pytrie/',
    description     = 'A pure Python implementation of the trie data structure.',
    long_description=
'''A *trie* is an ordered tree data structure that is used to store a mapping
where the keys are sequences, usually strings over an alphabet. In addition to
implementing the mapping interface, tries allow finding the items for a given
prefix, and vice versa, finding the items whose keys are prefixes of a given key.
''',
    classifiers     = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules      = ['pytrie'],
)
