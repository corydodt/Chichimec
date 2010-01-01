"""
Test that the examples provided really function
"""
from twisted.trial import unittest

import re

from chichimec import example

class ResourceTest(unittest.TestCase):
    """Tests of the generated examples"""
    # def setUp(self):

    def test_txGenshiExample(self):
        """
        Templates generated with txGenshi work
        """
        r = example.GenshiMixPage()
        s = r.renderSynchronously()
        self.assertSubstring('<p>You are Joe and your stuff is here.</p>', s)
        self.assertSubstring('<span>Your name is Joe</span>', s)
        self.assertSubstring('<span>this is the value of the key</span>', s)
        self.assertSubstring('<span>49 7 59</span>', s)
        self.assertSubstring('Yeah, we can do it!', s)
        self.failIfSubstring("Aw shucks, we can't do it.", s)
        self.assertSubstring('<li>item 0</li>', s)
        self.assertSubstring('<li>item 9</li>', s)
        self.assertTrue(re.search(r'<p class="greeting">\s*Hello, world!\s*</p>', s))
        self.assertTrue(re.search(r'<p class="greeting">\s*Hello, everyone else!\s*</p>', s))
        self.assertTrue(re.search(r'<span>\s*Hello Dude\s*</span>', s))
        self.assertTrue(re.search(r'<span>\s*Hello again, Dude\s*</span>', s))
        self.assertSubstring('<li class="odd">item 0</li>', s)
        self.assertSubstring('<li class="even">item 9</li>', s)
        self.assertSubstring('<li>Joe</li>', s)
        self.assertTrue(re.search(r'<h2>Genshi :replace</h2>\s*Joe\s*</ul>', s))
        self.assertTrue(re.search(r'<h2>Genshi :strip</h2>\s*<b>foo</b>\s*</div>', s))

    def test_athenaExample(self):
        """
        Comet-based app works
        """
        self.fail("You should write a test")
        r = example.AthenaPage()
