"""
Test that the examples provided really function
"""
import re
import random

import fudge

from twisted.trial import unittest
from twisted.internet import defer

from nevow import flat, athena, url

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
        @defer.inlineCallbacks
        def test():
            jsPackages = athena.allJavascriptPackages()
            rr = example.AthenaPage(jsModules=athena.MappingResource(jsPackages))
            rr._becomeLive(url.URL('/app'))
            rendered = yield flat.flatten(rr)

            # set the rate to be too infrequent to have any race possibilities
            # during this test
            rr.rate = 0.00001 # = 100000 seconds between updates

            rr.wid.setFilter(0)
            self.assertEqual(rr.wid.filter, 0)

            rr.wid.liveFragmentChildren = []


            callRemote = fudge.Fake("callRemote", expect_call=True)
            callRemote.with_args("number", 486000).returns(defer.succeed(u'ok'))
            fudge.patch_object(rr.wid, 'callRemote', callRemote)

            random.seed(10)

            # make two calls to random() with this seed.  They should return
            # the tested values, using Python's documented PRNG: Mersenne
            # Twister, and this seed.

            num = yield rr.wid.number()
            self.assertEqual(num, 614262)

            num = yield rr.wid.number()
            self.assertEqual(num, 486000)

            fudge.verify()

            rr.wid._athenaDetachServer()
            rr.action_close(None)
            defer.returnValue(None)

        return test()

