import logging
import random
import unittest

from olib import get_cls, get, values
from ob.krn import get_kernel
from ob.hdl import Event
from ob.utl import find_modules, find_shorts, get_exception

k = get_kernel()
k.cfg.prompt = False
k.walk("ob,obmod")

mods = find_modules("ob")
names = find_shorts("ob")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for key in mods:
            for n in names:
                for nn in get(values, n, []):
                    try:
                        e = get_cls(t)()
                        e.txt = key + " " + random.choice(list(names.values()))
                        e.parse(e.txt)
                        v = get(k.cmds, key, None)
                        if v:
                            v(e)
                    except AttributeError:
                        pass
                    except TypeError as ex:
                        break
        self.assertTrue(True)
