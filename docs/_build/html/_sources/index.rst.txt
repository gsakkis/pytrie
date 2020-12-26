.. PyTrie documentation master file, created by
   sphinx-quickstart on Sat Dec 26 19:56:21 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyTrie's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: pytrie

Reference documentation
-----------------------

Classes
~~~~~~~
.. autoclass:: Trie
    :show-inheritance:
    :members: __init__, fromkeys, KeyFactory, NodeFactory
.. autoclass:: StringTrie
    :show-inheritance:
.. autoclass:: SortedTrie
    :show-inheritance:
.. autoclass:: SortedStringTrie
    :show-inheritance:

Trie methods
~~~~~~~~~~~~
The following methods are specific to tries; they are not part of the mapping API.

.. automethod:: Trie.longest_prefix(key[, default])
.. automethod:: Trie.longest_prefix_value(key[, default])
.. automethod:: Trie.longest_prefix_item(key[, default])
.. automethod:: Trie.iter_prefixes
.. automethod:: Trie.iter_prefix_values
.. automethod:: Trie.iter_prefix_items

Extended mapping API methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following methods extend the respective mapping API methods with an optional
``prefix`` parameter. If not ``None``, only keys (or associated values/items)
that start with ``prefix`` are returned.

.. automethod:: Trie.keys
.. automethod:: Trie.values
.. automethod:: Trie.items
.. automethod:: Trie.iterkeys
.. automethod:: Trie.itervalues
.. automethod:: Trie.iteritems

Original mapping API methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following methods have the standard mapping signature and semantics.

.. automethod:: Trie.__len__
.. automethod:: Trie.__bool__
.. automethod:: Trie.__iter__
.. automethod:: Trie.__contains__
.. automethod:: Trie.__getitem__
.. automethod:: Trie.__setitem__
.. automethod:: Trie.__delitem__
.. automethod:: Trie.__repr__
.. automethod:: Trie.clear
.. automethod:: Trie.copy

Internals
~~~~~~~~~
Tries are implemented as trees of :class:`Node` instances. You don't need to
worry about them unless unless you want to extend or replace :class:`Node` with
a new node factory and bind it to :attr:`Trie.NodeFactory`.

.. autoclass:: Node
    :show-inheritance:
    :members:
    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
