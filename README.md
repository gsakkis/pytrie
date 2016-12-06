# pytrie

`pytrie` is a a pure Python (2 and 3) implementation of the trie data structure.

A _trie_ is an ordered tree data structure that is used to store a mapping
where the keys are sequences, usually strings over an alphabet. In addition to
implementing the mapping interface, tries allow finding the items for a given
prefix, and vice versa, finding the items whose keys are prefixes of a given key.

`pytrie` runs on Python 2.7 and 3.x without modification. To install run:

    pip install pytrie

Documentation is available at [Read the Docs](https://pytrie.readthedocs.io/).

## Changelog

### 0.3

* Fixed bug for tries with zero-length keys.
* Added `__bool__` (`__nonzero__`) and `__cmp__` methods to `Trie`.
* Added `sortedcontainers` dependency.
* Linting.
* Converted from Mercurial to Git.

### 0.2

* Initial Python 3 support (thanks Dmitrijs Milajevs)

### 0.1

* Initial release
