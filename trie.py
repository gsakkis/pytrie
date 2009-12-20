__all__ = ['Trie', 'SortedTrie', 'Node']

#TODO:
# - docs, comments
# - bitbucket project + ANN
# - (0.2 benchmarks/profiling/optimization)

from copy import copy
from operator import itemgetter
from UserDict import DictMixin

# Singleton sentinel - works with pickling
class NULL(object): pass


class Node(object):
    __slots__ = ('value', 'children')
    
    ChildrenFactory = dict

    def __init__(self):
        self.value = NULL
        self.children = self.ChildrenFactory()
    
    def size(self, internal=False):
        return ((self.value is not NULL or internal) +
                 sum(child.size(internal) for child in self.children.itervalues()))

    def __eq__(self, other):
        return self.value == other.value and self.children == other.children

    def __repr__(self):
        return '(%s, {%s})' % (
            self.value is NULL and 'NULL' or repr(self.value),
            ', '.join('%r: %r' % t for t in self.children.iteritems()))

    def __copy__(self):
        clone = self.__class__()
        clone.value = self.value
        clone_children = clone.children
        for key,child in self.children.iteritems():
            clone_children[key] = child.__copy__()
        return clone

    def __getstate__(self):
        return (self.value, self.children)

    def __setstate__(self, state):
        self.value, self.children = state

    
class Trie(DictMixin, object):

    KeyFactory = ''.join
    NodeFactory = Node

    def __init__(self, seq=None, **kwargs):
        self._root = self.NodeFactory()
        self.update(seq, **kwargs)

    def iterprefixeditems(self, key):
        key_factory = self.KeyFactory
        prefix = []
        append = prefix.append
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
            append(part)
            if node.value is not NULL:
                yield (key_factory(prefix), node.value)

    def __len__(self):
        return self._root.size()

    def __iter__(self):
        return self.iterkeys()

    def __contains__(self, key):
        node = self._find(key)
        return node is not None and node.value is not NULL

    def __getitem__(self, key):
        node = self._find(key)
        if node is None or node.value is NULL:
            raise KeyError
        return node.value

    def __setitem__(self, key, value):
        node = self._root
        Node = self.NodeFactory
        for part in key:
            next = node.children.get(part)
            if next is None:
                node = node.children.setdefault(part, Node())
            else:
                node = next
        node.value = value

    def __delitem__(self, key):
        nodes_parts = []
        append = nodes_parts.append
        node = self._root
        for part in key:
            append((node,part))
            node = node.children.get(part)
            if node is None:
                break
        if node is None or node.value is NULL:
            raise KeyError
        node.value = NULL
        pop = nodes_parts.pop
        while node.value is NULL and not node.children and nodes_parts:
            node,part = pop()
            del node.children[part]

    def has_key(self, key):
        return key in self

    def keys(self, prefix=None):
        return list(self.iterkeys(prefix))

    def values(self, prefix=None):
        return list(self.itervalues(prefix))

    def items(self, prefix=None):
        return list(self.iteritems(prefix))

    def iterkeys(self, prefix=None):
        return (key for key,value in self.iteritems(prefix))

    def itervalues(self, prefix=None):
        def generator(node, NULL=NULL):
            if node.value is not NULL:
                yield node.value
            for part,child in node.children.iteritems():
                for subresult in generator(child):
                    yield subresult
        if prefix is None:
            node = self._root
        else:
            node = self._find(prefix)
            if node is None:
                node = self.NodeFactory()
        return generator(node)

    def iteritems(self, prefix=None):
        parts = []
        append = parts.append
        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, NULL=NULL):
            if node.value is not NULL:
                yield (key_factory(parts), node.value)
            for part,child in node.children.iteritems():
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]
        node = self._root
        if prefix is not None:
            for part in prefix:
                append(part)
                node = node.children.get(part)
                if node is None:
                    node = self.NodeFactory()
                    break
        return generator(node)

    def clear(self):
        self._root.children.clear()

    def __copy__(self):
        return self.copy()

    def copy(self):
        clone = copy(super(Trie,self))
        clone._root = copy(self._root)
        return clone

    @classmethod
    def fromkeys(cls, iterable, value=None, key_factory=None):
        d = cls()
        if key_factory is not None:
            d.KeyFactory = key_factory
        for key in iterable: d[key] = value
        return d

    def _find(self, key):
        node = self._root
        for part in key:
            node = node.children.get(part)
            if node is None:
                break
        return node


# XXX: quick & dirty sorted dict; currently only iteritems() has to be overriden.
# However this is implementation detail that may change in the future
class _SortedDict(dict):
    def iteritems(self):
        return sorted(dict.iteritems(self), key=itemgetter(0))

class _SortedNode(Node):
    ChildrenFactory = _SortedDict

class SortedTrie(Trie):
    NodeFactory = _SortedNode
