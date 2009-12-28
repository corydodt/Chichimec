"""
Test the base website included with chichimec
"""
from __future__ import with_statement

from twisted.trial import unittest
from twisted.python import log

import fudge

from chichimec import resource

class WebsiteTest(unittest.TestCase):
    """
    The website starts up and does correctly limit logs
    """
    def setUp(self):
        self.messages = []
        def msg(*a, **kw):
            self.messages.append([a, sorted(kw.items()),
                ])

        Root = fudge.Fake('Root', callable=True).returns(fudge.Fake('Resource'))
        self.restore1 = fudge.patch_object(resource, 'Root', Root)
        self.restore2 = fudge.patch_object(log, 'msg', msg)

    def tearDown(self):
        self.restore2.restore()
        self.restore1.restore()
        self.Root = None
        del self.messages[:]

    def test_logging(self):
        """
        Our website has 80-column logging
        """
        req = fudge.Fake('request')
        req.uri = 'http://foob'
        req.code = 200

        from chichimec.webserver import WebSite
        ws = WebSite()
        ws.log(req)
        self.assertEqual(self.messages, [[('200 http://foob',),
            [('system', 'HTTP')]]])

        del self.messages[:]

        req.code = 500
        ws.log(req)
        self.assertEqual(self.messages, [[('!500! http://foob',),
            [('system', 'HTTP')]]])

        del self.messages[:]

        req.uri = 'http://exeptionally/looooooooooooooooooooooooooooooooooooooooong'
        ws.log(req)
        self.assertEqual(self.messages, [[('!500! ...ooooooooooooooooooooooooooooooooong',),
            [('system', 'HTTP')]]])

    def test_jsmodule(self):
        """
        Special handling for 'jsmodule' in the url should be correct
        """
        req = fudge.Fake('request')
        req.uri = 'http://foob/jsmodule/0127109831029/TestProject'
        req.code = 200

        from chichimec.webserver import WebSite
        ws = WebSite()
        ws.log(req)
        self.assertEqual(self.messages, [[('200 .../jsmodule/0127109831029/TestProject',),
            [('system', 'HTTP')]]])

