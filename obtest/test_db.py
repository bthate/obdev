# OB - write your own commands.
#
#

"database tests"

import unittest

from olib import find

class Test_Store(unittest.TestCase):

    def test_emptyargs(self):
        res = find("", {})
        self.assertEqual(list(res), [])

    def test_emptyargs2(self):
        res = find("", {})
        self.assertEqual(list(res), [])
