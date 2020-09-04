""" configuration tests """

import unittest

from olib import Cfg, last

class O(object):

    def bla(self):
        return "yo!"

class Test_Cfg(unittest.TestCase):

    def test_normal(self):
        o = O()
        o.bla = "bla"
        with self.assertRaises(TypeError) as x:
            res = o.bla()

    def test_last1(self):
        cfg = Cfg()
        cfg.last = "bla"
        self.assertEqual(cfg.last, "bla")
