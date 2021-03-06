# -*- coding: utf-8 -*-

from tests.baseclass import BaseTestCase
from meh.safe_string import SafeStr, PY

class TestClass(object):
    def __str__(self):
        return "string representation of TestClass instance"

class TestClass2():
    pass

class SafeStr_TestCase(BaseTestCase):
    def setUp(self):
        self.safestr = SafeStr()
        self.unistr = u"ááááá"
        self.enc_unistr = self.unistr.encode("utf-8")
        self.asciistr = "aaaa"
        self.bindata = b'\xff\xff\xfe'
        self.test_object = TestClass()
        self.test_object2 = TestClass2()

    def runTest(self):
        self.safestr += self.asciistr
        self.safestr += self.enc_unistr
        self.safestr += self.unistr
        self.safestr += self.bindata
        self.safestr += self.test_object
        self.safestr += self.test_object2

        self.assertIn(self.asciistr, self.safestr)

        if PY == 2:
            self.assertIn("OMITTED OBJECT WITHOUT __str__ METHOD", self.safestr)
            # should be included twice -- appended enc_unistr and unistr
            self.assertIn(str(self.enc_unistr), self.safestr)
        else:
            self.assertIn("<safe_string_test.TestClass2 object at ", self.safestr)
            self.assertIn(str(self.enc_unistr), self.safestr)
            self.assertIn(self.unistr, self.safestr)

        self.assertIn("\\xff\\xff\\xfe", self.safestr)
        self.assertIn(str(self.test_object), self.safestr)

