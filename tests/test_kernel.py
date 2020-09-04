# OB - write your own commands. 
#
#

import unittest

from ob.krn import Cfg, get_kernel

k = get_kernel()

class Test_Kernel(unittest.TestCase):

    def test_kernel(self):
        self.assertEqual(type(k.cfg), Cfg)
