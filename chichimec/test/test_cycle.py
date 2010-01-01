"""
Verify the cycle script is able to run and restart servers
"""
from twisted.trial import unittest

class CycleTest(unittest.TestCase):
    """Tests of the cycle running script"""
    # def setUp(self):

    def test_start(self):
        """
        Running cycle causes trial to be invoked
        """
        self.fail("write a test")

    def test_inotify(self):
        """
        Use of inotify works - modifying a source file causes a restart to
        occur
        """
        self.fail("write a test")
