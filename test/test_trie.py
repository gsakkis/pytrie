import unittest
from trie import Trie


class TrieTests(unittest.TestCase):
    def setUp(self):
        self.words = 'an ant all allot alloy aloe are ate be'.split()
        self.trie = Trie(zip(self.words, range(len(self.words))))

    def test_prefix(self):
        self.assertEqual(self.trie.prefix('antonym'), 'ant')
        self.assertEqual(self.trie.prefix('are'), 'are')
        self.assertRaises(KeyError, self.trie.prefix, 'alumni')
        self.assertEqual(self.trie.prefix('alumni', strict=False), 'al')
        self.assertEqual(self.trie.prefix('linux', strict=False), '')

    def test_prefixed_value(self):
        self.assertEqual(self.trie.prefixed_value('antonym'), 1)
        self.assertEqual(self.trie.prefixed_value('are'), 6)
        self.assertRaises(KeyError, self.trie.prefixed_value, 'alumni')
        self.assertEqual(self.trie.prefixed_value('alumni', default=None), None)
        self.assertEqual(self.trie.prefixed_value('linux', default=-1), -1)

    def test_prefix_value_pair(self):
        self.assertEqual(self.trie.prefix_value_pair('antonym'), ('ant', 1))
        self.assertEqual(self.trie.prefix_value_pair('are'), ('are', 6))
        self.assertRaises(KeyError, self.trie.prefix_value_pair, 'alumni')
        self.assertEqual(self.trie.prefix_value_pair('alumni', default=None), ('al', None))
        self.assertEqual(self.trie.prefix_value_pair('linux', default=-1), ('',-1))

    def test_iterkeys_prefix(self):
        self.assertEqual(set(self.trie.iterkeys('al')),
                         set(['all','allot','alloy','aloe']))
        self.assertEqual(list(self.trie.iterkeys('are')), ['are'])
        self.assertEqual(list(self.trie.iterkeys('ann')), [])

    def test_itervalues_prefix(self):
        self.assertEqual(set(self.trie.itervalues('al')), set([2,3,4,5]))
        self.assertEqual(list(self.trie.itervalues('are')), [6])
        self.assertEqual(list(self.trie.itervalues('ann')), [])

    def test_iteritems_prefix(self):
        self.assertEqual(set(self.trie.iteritems('al')),
                         set([('all',2),('allot',3),('alloy',4),('aloe',5)]))
        self.assertEqual(list(self.trie.iteritems('are')), [('are',6)])
        self.assertEqual(list(self.trie.iteritems('ann')), [])

    def test_iter_prefix_consistency(self):
        for prefix in 'al','are','ann':
            self.assertEqual(list(self.trie.iteritems(prefix)),
                             zip(self.trie.iterkeys(prefix),
                                 self.trie.itervalues(prefix)))

    def test_pickle(self):
        from pickle import dumps, loads, HIGHEST_PROTOCOL
        for proto in xrange(HIGHEST_PROTOCOL):
            unpickled = loads(dumps(self.trie, proto))
            self.assertEqual(self.trie, unpickled)
            self.assertTrue(type(self.trie) is type(unpickled))
            self.assertFalse(self.trie is unpickled)


if __name__ == "__main__":    
    unittest.main()
