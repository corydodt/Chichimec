"""
The test resource can start up.
"""
from twisted.trial import unittest

from chichimec import example

from {options[projectName]}.resource import {options[projectDir]}Page

class ResourceTest(unittest.TestCase):
    """
    The initial sample resource: tests
    """
    # def setUp(self):

    def test_children(self):
        """
        The resource children are present
        """
        r = {options[projectDir]}Page()
        rGenshi = r.locateChild(None, ('genshimix',))[0]
        self.assertIsInstance(rGenshi, example.GenshiMixPage)
        rAthena = r.locateChild(None, ('athena',))[0]
        self.assertIsInstance(rAthena, example.AthenaPage, )


