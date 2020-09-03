# OB - write your own commands.
#
#

"core tests."

import os, unittest

from olib import Object, load, save, workdir

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = Object()
        o.bla = "mekker"
        p = save(o)
        oo = Object()
        load(oo, p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = Object()
        p = save(o)
        self.assertTrue(os.path.exists(os.path.join(workdir, "store", p)))

    def test_subitem(self):
        o = Object()
        o.test = Object()
        p = save(o)
        oo = Object()
        oo = load(oo, p)
        self.assertTrue(type(oo.test), Object)
