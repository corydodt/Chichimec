"""
Test that the examples provided really function
"""
import random

import fudge

from twisted.trial import unittest
from twisted.internet import defer

from nevow import flat, athena, url

from chichimec import example

class ResourceTest(unittest.TestCase):
    """Tests of the generated examples"""
    def test_txGenshiExample(self):
        """
        Templates generated with txGenshi work
        """
        r = example.GenshiMixPage()
        s = r.renderSynchronously()
        username = u'Joe'
        self.assertSubstring('<p>You are %s and your stuff is here.</p>' %
                (username,), s)
        self.assertSubstring('<span>this is the value of the key</span>', s)
        self.assertSubstring('Apples are red', s)
        self.assertSubstring('<span>49 7 59</span>', s)
        self.assertSubstring('<span>27 &lt;= 30: True ... 27 &gt; 10: True</span>', s)

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
            self.assertSubstring('Rate: 50', rendered)

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

