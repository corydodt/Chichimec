"""
Tests for the chichimec.util module's functions
"""
import os

from twisted.trial import unittest

from chichimec import util as chiutil

class UtilTest(unittest.TestCase):
    """Util's functions"""
    # def setUp(self):

    def test_RESOURCE(self):
        """
        RESOURCE transforms a string into a filename correctly.
        """
        try:
            oldfile = chiutil.__file__
            chiutil.__file__ = '/foo/util.py'
            self.assertEqual(chiutil.RESOURCE('__init__.py'), '/foo/__init__.py')
            self.assertEqual(chiutil.RESOURCE(''), '/foo/')
        finally:
            chiutil.__file__ = oldfile

    def test_nameFix(self):
        """
        The generation of a proper name works
        """
        self.assertRaises(ValueError, chiutil.nameFix, "")
        self.assertRaises(ValueError, chiutil.nameFix, "__")
        self.assertEqual(chiutil.nameFix("x"*200), "x"*128)
        self.assertEqual(chiutil.nameFix("_This Awesome Name"),
            "thisawesomename")
