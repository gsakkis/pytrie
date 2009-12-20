__all__ = ['Trie']

#TODO:
# - docs, comments
# - bitbucket project
# - profiling/optimization

from copy import copy
from UserDict import DictMixin

# Singleton sentinel - works with pickling/unpickling
class EMPTY(object): pass


class _Node(dict):
    __slots__ = ('value',)

    def __init__(self, value=EMPTY):
        self.value = value

    def size(self, internal=False):
        return ((self.value is not EMPTY or internal) +
                 sum(child.size(internal) for child in self.itervalues()))

    def __eq__(self, other):
        return self.value == other.value and super(_Node,self).__eq__(other)

    def __repr__(self):
        return '(%s, {%s})' % (
            self.value is EMPTY and 'EMPTY' or repr(self.value),
            ', '.join('%r: %r' % t for t in self.iteritems()))

    def __copy__(self):
        clone = self.__class__(self.value)
        for key,child in self.iteritems():
            clone[key] = child.__copy__()
        return clone

    def __getstate__(self):
        return (self.value, self.items())

    def __setstate__(self, state):
        self.value = state[0]
        self.update(state[1])


class Trie(DictMixin, object):

    KeyFactory = ''.join
    _NodeFactory = _Node

    def __init__(self, seq=None, **kwargs):
        self._root = self._NodeFactory()
        self.update(seq, **kwargs)

    def prefix(self, key, strict=True):
        return self.prefix_value_pair(key, default=strict and EMPTY or None)[0]

    def prefixed_value(self, key, default=EMPTY):
        node = self._root
        for part in key:
            next = node.get(part)
            if next is None: break
            node = next
        if node is not None and node.value is not EMPTY:
            return node.value
        if default is not EMPTY:
            return default
        raise KeyError

    def prefix_value_pair(self, key, default=EMPTY):
        try: key[:0]
        except (AttributeError,TypeError):
            prefix = []; prefix_append = prefix.append
            node = self._root
            iterable = iter(key)
            for part in iterable:
                next = node.get(part)
                if next is None: break
                node = next
                prefix_append(part)
        else:
            i = 0
            node = self._root
            for part in key:
                next = node.get(part)
                if next is None: break
                node = next
                i += 1
            prefix = key[:i]
        if node is not None and node.value is not EMPTY:
            value = node.value
        elif default is not EMPTY:
            value = default
        else:
            raise KeyError
        return (prefix, value)

    def __len__(self):
        return self._root.size()

    def __iter__(self):
        return self.iterkeys()

    def __contains__(self, key):
        node = self._find(key)
        return node is not None and node.value is not EMPTY

    def __getitem__(self, key):
        node = self._find(key)
        if node is None or node.value is EMPTY:
            raise KeyError
        return node.value

    def __setitem__(self, key, value):
        node = self._root
        Node = self._NodeFactory
        for part in key:
            next = node.get(part)
            if next is None:
                node = node.setdefault(part, Node())
            else:
                node = next
        node.value = value

    def __delitem__(self, key):
        nodes_parts = []; append = nodes_parts.append
        node = self._root
        for part in key:
            append((node,part))
            node = node.get(part)
            if node is None: break
        if node is None or node.value is EMPTY:
            raise KeyError
        node.value = EMPTY
        pop = nodes_parts.pop
        while node.value is EMPTY and len(node)==0 and nodes_parts:
            node,part = pop()
            del node[part]

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
        def generator(node, EMPTY=EMPTY):
            if node.value is not EMPTY:
                yield node.value
            for part,child in node.iteritems():
                for subresult in generator(child):
                    yield subresult
        if prefix is None:
            node = self._root
        else:
            node = self._find(prefix)
            if node is None:
                node = self._NodeFactory()
        return generator(node)

    def iteritems(self, prefix=None):
        parts = []; append = parts.append
        def generator(node, key_factory=self.KeyFactory, parts=parts,
                      append=append, EMPTY=EMPTY):
            if node.value is not EMPTY:
                yield (key_factory(parts), node.value)
            for part,child in node.iteritems():
                append(part)
                for subresult in generator(child):
                    yield subresult
                del parts[-1]
        node = self._root
        if prefix is not None:
            for part in prefix:
                append(part)
                node = node.get(part)
                if node is None:
                    node = self._NodeFactory()
                    break
        return generator(node)

    def clear(self):
        self._root.clear()

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
            node = node.get(part)
            if node is None: break
        return node
