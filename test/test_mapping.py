import sys
import unittest
from UserDict import UserDict
from test.mapping_tests import TestMappingProtocol, BasicTestMappingProtocol

from trie import Trie


class GeneralMappingTests(TestMappingProtocol):
    type2test = Trie

    def _empty_mapping(self, **kwds):
        """Return an empty mapping object"""
        return self.type2test(**kwds)

    def _reference(self):
        """Return a dictionary of values which are invariant by storage
        in the object under test."""
        return {"key1":"value1", "key2":(1,2,3), "key":None}

    def test_keys(self):
        d = self._empty_mapping()
        self.assertEqual(d.keys(), [])
        d = self._full_mapping(self.reference)
        self.assert_(self.inmapping.keys()[0] in d.keys())
        self.assert_(self.other.keys()[0] not in d.keys())

    def test_values(self):
        d = self._empty_mapping()
        self.assertEqual(d.values(), [])
        d = self._full_mapping({"1":2})
        self.assertEqual(d.values(), [2])

    def test_items(self):
        d = self._empty_mapping()
        self.assertEqual(d.items(), [])
        d = self._full_mapping({"1":2})
        self.assertEqual(d.items(), [("1", 2)])

    def test_clear(self):
        d = self._full_mapping(self.reference)
        d.clear()
        self.assertEqual(d, {})
        self.assertRaises(TypeError, d.clear, None)

    def test_update(self):
        BasicTestMappingProtocol.test_update(self)
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
            def __init__(this):
                this.d = self._reference()
            def keys(this):
                return this.d.keys()
            def __getitem__(this, i):
                return this.d[i]
        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, self._reference())

    def test_fromkeys(self):
        self.assertEqual(self.type2test.fromkeys("abc"), {"a":None, "b":None, "c":None})
        d = self._empty_mapping()
        self.assert_(not(d.fromkeys("abc") is d))
        self.assertEqual(d.fromkeys("abc"), {"a":None, "b":None, "c":None})
        self.assertEqual(d.fromkeys(("4","5"),0), {"4":0, "5":0})
        self.assertEqual(d.fromkeys([]), {})
        def g(): yield "1"
        self.assertEqual(d.fromkeys(g()), {"1":None})
        self.assertRaises(TypeError, {}.fromkeys, 3)
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

        self.assertRaises(Exc, self.type2test.fromkeys, BadSeq())

        class baddict2(self.type2test):
            def __setitem__(self, key, value):
                raise Exc()

        self.assertRaises(Exc, baddict2.fromkeys, [1])

        class mydict(self.type2test):
            def __new__(cls):
                return UserDict()
        ud = mydict.fromkeys("ab")
        self.assertEqual(ud, {"a":None, "b":None})
        self.assert_(isinstance(ud, UserDict))

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
        BasicTestMappingProtocol.test_pop(self)
        # Tests for pop with specified key
        d = self._empty_mapping()
        k, v = "abc", "def"
        self.assertEqual(d.pop(k, v), v)
        d[k] = v
        self.assertEqual(d.pop(k, 1), v)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        d = self._empty_mapping()
        x = BadHash()
        d[[x]] = 42
        x.fail = True
        self.assertRaises(Exc, d.pop, [x])

    def test_getitem(self):
        TestMappingProtocol.test_getitem(self)
        class Exc(Exception): pass

        class BadEq(object):
            def __iter__(self): yield "ab"
            def __eq__(self, other):
                raise Exc()

        d = self._empty_mapping()
        d[BadEq()] = 42
        self.assertRaises(KeyError, d.__getitem__, "c")

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        d = self._empty_mapping()
        x = BadHash()
        d[[x]] = 42
        x.fail = True
        self.assertRaises(Exc, d.__getitem__, [x])

    def test_setdefault(self):
        TestMappingProtocol.test_setdefault(self)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        d = self._empty_mapping()
        x = BadHash()
        d[[x]] = 42
        x.fail = True
        self.assertRaises(Exc, d.setdefault, [x], [])

    def test_le(self):
        self.assert_(not (self._empty_mapping() < self._empty_mapping()))
        self.assert_(not (self._full_mapping({"1": 2}) < self._full_mapping({"1": 2L})))

        class Exc(Exception): pass

        class BadCmp(object):
            def __eq__(self, other):
                raise Exc()

        class TupleTrie(self.type2test):
            KeyFactory = tuple

        d1 = TupleTrie()
        d1[[1,BadCmp()]] = 3
        d2 = TupleTrie()
        d2[1,2] = 3
        try:
            d1 < d2
        except Exc:
            pass
        else:
            self.fail("< didn't raise Exc")

    def test_delsize(self):
        d = self._empty_mapping(x=1, xyz=3, xyzwv=5)
        del d['xyzwv']
        self.assertEqual(d.items(), [('x',1), ('xyz',3)])
        self.assertEqual(d._root.size(internal=True), 4)
        del d['x']
        self.assertEqual(d.items(), [('xyz',3)])
        self.assertEqual(d._root.size(internal=True), 4)
        del d['xyz']
        self.assertEqual(d.items(), [])
        self.assertEqual(d._root.size(internal=True), 1)


class SubclassMappingTests(GeneralMappingTests):
    class type2test(Trie):
        pass


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.extend(['GeneralMappingTests', 'SubclassMappingTests'])
    unittest.main()
