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
    # def setUp(self):

    def test_logging(self):
        """
        Our website has 80-column logging
        """
        Root = fudge.Fake('Root', callable=True).returns(fudge.Fake('Resource'))
        req = fudge.Fake('request')
        req.uri = 'http://foob'
        req.code = 200
        messages = []

        def msg(*a, **kw):
            messages.append([a, sorted(kw.items()),
                ])

        with fudge.patched_context(resource, 'Root', Root):
            with fudge.patched_context(log, 'msg', msg):
                from chichimec.webserver import WebSite
                ws = WebSite()
                ws.log(req)
                self.assertEqual(messages, [[('200 http://foob',),
                    [('system', 'HTTP')]]])

                del messages[:]

                req.code = 500
                ws.log(req)
                self.assertEqual(messages, [[('!500! http://foob',),
                    [('system', 'HTTP')]]])

                del messages[:]

                req.uri = 'http://exeptionally/looooooooooooooooooooooooooooooooooooooooong'
                ws.log(req)
                self.assertEqual(messages, [[('!500! ...ooooooooooooooooooooooooooooooooong',),
                    [('system', 'HTTP')]]])

