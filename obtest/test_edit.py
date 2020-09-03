# OB - write your own commands.
#
#

"edit command tests."

import unittest

from olib import Object, edit
from ob.hdl import Event
from ob.prs import parse

class Log(Object):

    "check class attribute edit as well."

    def __init__(self):
        self.txt = "bla"

l = Log()

class Test_Edit(unittest.TestCase):

    "edit tests."

    def setUp(self):
        l.txt = "bla"
        
    def test_edit1(self):
        e = Event()
        parse(e, "ed log txt==bla txt=mekker")
        edit(l, e.sets)
        self.assertEqual(l.txt, "mekker")

    def test_edit2(self):
        e = Event()
        parse(e, "ed")
        edit(l, e.sets)
        self.assertTrue(True, True)

    def test_edit3(self):
        e = Event()
        parse(e, "ed log txt=#bla")
        edit(l, e.sets)
        self.assertEqual(l.txt, "#bla")

    def test_edit4(self):
        e = Event()
        parse(e, "ed log txt==#bla txt=mekker2")
        edit(l, e.sets)
        self.assertEqual(l.txt, "mekker2")

    def test_edit5(self):
        e = Event()
        parse(e, 'ed log txt==mekker txt=bla1,bla2')
        edit(l, e.sets)
        self.assertEqual(l.txt, ["bla1", "bla2"])

    def test_edit(self):
        e = Event()
        parse(e, "ed log txt==bla txt=#mekker")
        edit(l, e.sets)
        self.assertEqual(l.txt, "#mekker")
