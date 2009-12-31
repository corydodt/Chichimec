"""
Test that the twistd plugin included works
"""
import sys
import os

from twisted.trial import unittest
from twisted import plugin

from nevow.inevow import IJavascriptPackage
from nevow import athena

from fudge import Fake, patcher, verify

from {options[projectName]} import RESOURCE

class NevowPluginTest(unittest.TestCase):
    """
    AutoJSPackage is a convenience for setting up a static directory
    containing JS files that can be imported like Python modules.  This tests
    the plugin that sets the convenience up.
    """
    def setUp(self):
        self.jsPackages = athena.allJavascriptPackages()

    def test_jsFound(self):
        """
        See if we can pull up the correct plugin, and it has the right
        attributes, and there is an accessible file there.
        """
        if '{options[projectDir]}' not in self.jsPackages:
            self.fail('Could not find the javascript package for {options[projectDir]}')

        athenaResource = athena.LivePage(jsModules=athena.MappingResource(self.jsPackages))
        r, segs = athenaResource.locateChild(None, ('jsmodule', '{options[projectDir]}'))
        r, segs = r.locateChild(None, ('{options[projectDir]}',))
        splits = r.fp.path.rsplit('/', 2)[1:]
        self.assertEqual(splits, ['{options[projectDir]}', '__init__.js'])

