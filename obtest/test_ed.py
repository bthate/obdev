# OB - write your own commands.
#
#

"edit command tests."

import unittest

from ob.krn import get_kernel
from ob.hdl import Event
from ob.prs import parse

k = get_kernel()

class Test_Ed(unittest.TestCase):

    def setUp(self):
        k.start()
        
    def test_ed1(self):
        e = Event()
        parse(e, "ed log txt==bla txt=mekker")
        k.queue.put(e)
        e.wait()
        self.assertEqual(e.result, [])
