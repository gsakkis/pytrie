import unittest
from pytrie import SortedStringTrie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.words = 'an ant all allot alloy aloe are ate be'.split()
        self.trie = SortedStringTrie(zip(self.words, range(len(self.words))))

    def test_longest_prefix(self):
        self.assertEqual(self.trie.longest_prefix('antonym'), 'ant')
        self.assertEqual(self.trie.longest_prefix('are'), 'are')
        self.assertEqual(self.trie.longest_prefix('alla'), 'all')
        self.assertEqual(self.trie.longest_prefix('allo'), 'all')
        self.assertRaises(KeyError, self.trie.longest_prefix_item, 'alumni')
        self.assertEqual(self.trie.longest_prefix('alumni', default=None), None)
        self.assertEqual(self.trie.longest_prefix('linux', default=-1), -1)

    def test_longest_prefix_value(self):
        self.assertEqual(self.trie.longest_prefix_value('antonym'), 1)
        self.assertEqual(self.trie.longest_prefix_value('are'), 6)
        self.assertEqual(self.trie.longest_prefix_value('alla'), 2)
        self.assertEqual(self.trie.longest_prefix_value('allo'), 2)
        self.assertRaises(KeyError, self.trie.longest_prefix_value, 'alumni')
        self.assertEqual(self.trie.longest_prefix_value('alumni', default=None), None)
        self.assertEqual(self.trie.longest_prefix_value('linux', default=-1), -1)

    def test_longest_prefix_item(self):
        self.assertEqual(self.trie.longest_prefix_item('antonym'), ('ant', 1))
        self.assertEqual(self.trie.longest_prefix_item('are'), ('are', 6))
        self.assertEqual(self.trie.longest_prefix_item('alla'), ('all', 2))
        self.assertEqual(self.trie.longest_prefix_item('allo'), ('all', 2))
        self.assertRaises(KeyError, self.trie.longest_prefix_item, 'alumni')
        self.assertEqual(self.trie.longest_prefix_item('alumni', default=None), None)
        self.assertEqual(self.trie.longest_prefix_item('linux', default=-1), -1)

    def test_iter_prefixes(self):
        self.assertEqual(list(self.trie.iter_prefixes('antonym')), ['an', 'ant'])
        self.assertEqual(list(self.trie.iter_prefixes('are')), ['are'])
        self.assertEqual(list(self.trie.iter_prefixes('alumni')), [])

    def test_iter_prefix_values(self):
        self.assertEqual(list(self.trie.iter_prefix_values('antonym')), [0, 1])
        self.assertEqual(list(self.trie.iter_prefix_values('are')), [6])
        self.assertEqual(list(self.trie.iter_prefix_values('alumni')), [])

    def test_iter_prefix_items(self):
        self.assertEqual(list(self.trie.iter_prefix_items('antonym')),
                         [('an', 0), ('ant', 1)])
        self.assertEqual(list(self.trie.iter_prefix_items('are')), [('are', 6)])
        self.assertEqual(list(self.trie.iter_prefix_items('alumni')), [])

    def test_keys_wprefix(self):
        self.assertEqual(self.trie.keys('al'), ['all','allot','alloy','aloe'])
        self.assertEqual(self.trie.keys('are'), ['are'])
        self.assertEqual(self.trie.keys('ann'), [])

    def test_values_wprefix(self):
        self.assertEqual(self.trie.values('al'), [2,3,4,5])
        self.assertEqual(self.trie.values('are'), [6])
        self.assertEqual(self.trie.values('ann'), [])

    def test_items_wprefix(self):
        self.assertEqual(self.trie.items('al'),
                         [('all',2),('allot',3),('alloy',4),('aloe',5)])
        self.assertEqual(self.trie.items('are'), [('are',6)])
        self.assertEqual(self.trie.items('ann'), [])

    def test_consistency_wprefix(self):
        t = self.trie
        for prefix in 'al','are','ann':
            self.assertEqual(
                t.items(prefix),
                list(zip(t.keys(prefix), t.values(prefix)))
            )

    def test_pickle(self):
        from pickle import dumps, loads, HIGHEST_PROTOCOL
        for proto in range(HIGHEST_PROTOCOL):
            unpickled = loads(dumps(self.trie, proto))
            self.assertEqual(self.trie, unpickled)
            self.assertTrue(type(self.trie) is type(unpickled))
            self.assertTrue(self.trie is not unpickled)

    def test_repr(self):
        evaled = eval(repr(self.trie))
        self.assertEqual(evaled, self.trie)
        self.assertEqual(evaled.__class__, self.trie.__class__)

if __name__ == "__main__":
    unittest.main()
