#!/usr/bin/env python

from distutils.core import setup

setup(
    name            = 'pytrie',
    version         = '0.1',
    py_modules      = ['pytrie'],
    author          = 'George Sakkis',
    author_email    = 'george.sakkis@gmail.com',
    url             = 'http://code.google.com/p/pytrie/',
    description     = 'Trie data structure',
    long_description=
'''*pytrie* exposes a single Python class, *triedict*, an implementation of
tries that extends the mapping interface. A trie (from re**trie**val), is a
multi-way tree structure useful for storing strings over an alphabet. **triedicts**
generalize the standard tries in that the keys are not restricted to strings but
can be any finite iterables of hashable objects, e.g. lists of numbers.
''',
    classifiers     = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
