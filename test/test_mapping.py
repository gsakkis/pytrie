'''Mapping tests adapted from stdlib test.mapping_tests

Essentially replaced non-iterable hardcoded keys with string keys,
plus a few more extra tests.
'''

import sys
import unittest
try:
    from UserDict import UserDict
except ImportError: # Python 3
    from collections import UserDict
from test import mapping_tests

from pytrie import StringTrie


class BasicTestMappingTrie(mapping_tests.BasicTestMappingProtocol):
    # Functions that can be useful to override to adapt to dictionary
    # semantics
    type2test = StringTrie  # which class is being tested (overwrite in subclasses)

    def _reference(self):
        """Return a dictionary of values which are invariant by storage
        in the object under test."""
        return {"key1":"value1", "key2":(1,2,3), "key":None}

    def test_values(self):
        d = self._empty_mapping()
        self.assertEqual(d.values(), [])

    def test_items(self):
        d = self._empty_mapping()
        self.assertEqual(d.items(), [])


class TestMappingTrie(BasicTestMappingTrie, mapping_tests.TestMappingProtocol):

    def test_values(self):
        super(TestMappingTrie,self).test_values()
        d = self._full_mapping({'1':2})
        self.assertEqual(d.values(), [2])

    def test_items(self):
        super(TestMappingTrie,self).test_items()
        d = self._full_mapping({'1':2})
        self.assertEqual(d.items(), [('1',2)])

    def test_clear(self):
        d = self._full_mapping(self.reference)
        d.clear()
        self.assertEqual(d, {})
        self.assertRaises(TypeError, d.clear, None)

    def test_update(self):
        BasicTestMappingTrie.test_update(self)
        # mapping argument
        d = self._empty_mapping()
        d.update({"1":100})
        d.update({"2":20})
        d.update({"1":1, "2":2, "3":3})
        self.assertEqual(d, {"1":1, "2":2, "3":3})

        # no argument
        d.update()
        self.assertEqual(d, {"1":1, "2":2, "3":3})

        # keyword arguments
        d = self._empty_mapping()
        d.update(x=100)
        d.update(y=20)
        d.update(x=1, y=2, z=3)
        self.assertEqual(d, {"x":1, "y":2, "z":3})

        # item sequence
        d = self._empty_mapping()
        d.update([("x", 100), ("y", 20)])
        self.assertEqual(d, {"x":100, "y":20})

        # Both item sequence and keyword arguments
        d = self._empty_mapping()
        d.update([("x", 100), ("y", 20)], x=1, y=2)
        self.assertEqual(d, {"x":1, "y":2})

        # iterator
        d = self._full_mapping({"1":3, "2":4})
        d.update(self._full_mapping({"1":2, "3":4, "5":6}).iteritems())
        self.assertEqual(d, {"1":2, "2":4, "3":4, "5":6})

        class SimpleUserDict:
            def __init__(self):
                self.d = {'1':1, '2':2, '3':3}
            def keys(self):
                return self.d.keys()
            def __getitem__(self, i):
                return self.d[i]
        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, {'1':1, '2':2, '3':3})

    def test_fromkeys(self):
        self.assertEqual(self.type2test.fromkeys("abc"), {"a":None, "b":None, "c":None})
        d = self._empty_mapping()
        self.assert_(not(d.fromkeys("abc") is d))
        self.assertEqual(d.fromkeys("abc"), {"a":None, "b":None, "c":None})
        self.assertEqual(d.fromkeys(("4","5"),0), {"4":0, "5":0})
        self.assertEqual(d.fromkeys([]), {})
        def g(): yield "1"
        self.assertEqual(d.fromkeys(g()), {"1":None})
        self.assertRaises(TypeError, d.fromkeys, 3)
        class dictlike(self.type2test): pass
        self.assertEqual(dictlike.fromkeys("a"), {"a":None})
        self.assertEqual(dictlike().fromkeys("a"), {"a":None})
        self.assert_(dictlike.fromkeys("a").__class__ is dictlike)
        self.assert_(dictlike().fromkeys("a").__class__ is dictlike)
        self.assert_(type(dictlike.fromkeys("a")) is dictlike)
        class mydict(self.type2test):
            def __new__(cls):
                return UserDict()
        ud = mydict.fromkeys("ab")
        self.assertEqual(ud, {"a":None, "b":None})
        self.assert_(isinstance(ud, UserDict))
        self.assertRaises(TypeError, dict.fromkeys)

        class Exc(Exception): pass

        class baddict1(self.type2test):
            def __init__(self):
                raise Exc()

        self.assertRaises(Exc, baddict1.fromkeys, [1])

        class BadSeq(object):
            def __iter__(self):
                return self
            def next(self):
                raise Exc()

        self.assertRaises(Exception, self.type2test.fromkeys, BadSeq())

        class baddict2(self.type2test):
            def __setitem__(self, key, value):
                raise Exc()

        self.assertRaises(Exc, baddict2.fromkeys, [1])

    def test_copy(self):
        d = self._full_mapping({"1":1, "2":2, "3":3, "":[]})
        d2 = d.copy(); self.assertEqual(d2, d)
        d[""].append("x"); self.assertEqual(d2[""], ["x"])
        d["4"] = 4; self.assertNotEqual(d2, d)
        d2["4"] = 4; self.assertEqual(d2, d)
        d2["5"] = 5; self.assertNotEqual(d2, d)
        d = self._empty_mapping()
        self.assertEqual(d.copy(), d)
        self.assert_(isinstance(d.copy(), d.__class__))
        self.assertRaises(TypeError, d.copy, None)

    def test_pop(self):
        BasicTestMappingTrie.test_pop(self)
        # Tests for pop with specified key
        d = self._empty_mapping()
        k, v = "abc", "def"
        self.assertEqual(d.pop(k, v), v)
        d[k] = v
        self.assertEqual(d.pop(k, 1), v)


class TestMappingTrieSubclass(TestMappingTrie):
    class type2test(StringTrie):
        pass


if __name__ == "__main__":
    unittest.main()
