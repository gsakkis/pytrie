import unittest

from pytrie import Trie, StringTrie, SortedTrie, SortedStringTrie


class TestClearEmptyKey(unittest.TestCase):
    def test_clear_removes_empty_key(self):
        for factory in (Trie, StringTrie, SortedTrie, SortedStringTrie):
            for value in (None, 0, 'root value'):
                with self.subTest(factory=factory, value=value):
                    empty = '' if issubclass(factory, StringTrie) else ()
                    child = 'ab' if issubclass(factory, StringTrie) else (1, 2)
                    trie = factory({empty: value, child: 'child'})
                    trie.clear()
                    trie.clear()
                    self.assertEqual(len(trie), 0)
                    self.assertFalse(trie)
                    self.assertEqual(list(trie.items()), [])
                    self.assertNotIn(empty, trie)
                    self.assertNotIn(child, trie)
                    with self.assertRaises(KeyError):
                        trie[empty]
                    self.assertEqual(
                        trie.longest_prefix(child, 'missing'), 'missing')
                    trie[child] = 'replacement'
                    self.assertEqual(
                        list(trie.items()), [(child, 'replacement')])
