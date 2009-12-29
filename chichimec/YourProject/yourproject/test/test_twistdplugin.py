"""
Test that the twistd plugin included works
"""
import sys

from twisted.trial import unittest
from twisted.application import service
from twisted import plugin

from fudge import Fake, patcher, verify

class TwistdTest(unittest.TestCase):
    def setUp(self):
        self.plugins = plugin.getPlugins(service.IServiceMaker)

    def test_serviceMakerAttributes(self):
        """
        See if we can pull up the correct plugin, and it has the right
        attributes
        """
        for plugin in self.plugins:
            if plugin.tapname == '{options[projectName]}':
                break
        else:
            self.failTest('Could not find the plugin {options[projectName]}')

        self.assertEqual(plugin.tapname, '{options[projectName]}')

        options = {{'port':8080}}

        TCPServer = Fake(expect_call=True).returns(Fake("TCPServer"))

        with patcher.patched_context(plugin, 'serverClass', TCPServer):
            from {options[projectName]} import resource
            ret = plugin.makeService(options)
            self.assertIsInstance(ret.site.resource, resource.Root)

        verify()

