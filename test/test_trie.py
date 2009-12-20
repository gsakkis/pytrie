import unittest
from trie import SortedTrie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.words = 'an ant all allot alloy aloe are ate be'.split()
        self.trie = SortedTrie(zip(self.words, range(len(self.words))))

    def test_iterprefixeditems(self):
        self.assertEqual(list(self.trie.iterprefixeditems('antonym')),
                         [('an', 0), ('ant', 1)])
        self.assertEqual(list(self.trie.iterprefixeditems('are')),
                         [('are', 6)])
        self.assertEqual(list(self.trie.iterprefixeditems('alumni')), [])

    def test_iterkeys_wprefix(self):
        self.assertEqual(list(self.trie.iterkeys('al')),
                         ['all','allot','alloy','aloe'])
        self.assertEqual(list(self.trie.iterkeys('are')), ['are'])
        self.assertEqual(list(self.trie.iterkeys('ann')), [])

    def test_itervalues_wprefix(self):
        self.assertEqual(list(self.trie.itervalues('al')), [2,3,4,5])
        self.assertEqual(list(self.trie.itervalues('are')), [6])
        self.assertEqual(list(self.trie.itervalues('ann')), [])

    def test_iteritems_wprefix(self):
        self.assertEqual(list(self.trie.iteritems('al')),
                         [('all',2),('allot',3),('alloy',4),('aloe',5)])
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
            self.assert_(type(self.trie) is type(unpickled))
            self.assert_(self.trie is not unpickled)


if __name__ == "__main__":    
    unittest.main()
