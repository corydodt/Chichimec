"""
Example page resources.  Boilerplate apps will import these.
"""
import random

from twisted.internet import task, defer
from twisted.python import log

from nevow import athena, loaders

from chichimec.util import RESOURCE

from txgenshi.loader import genshifile
from txgenshi.test.example import GenshiMixPage
GenshiMixPage  # pragma: shut up pyflakes


class AthenaPage(athena.LivePage):
    """
    Example page with athena demo
    """
    docFactory = genshifile(RESOURCE('templates/athena.xhtml'))

    def render_random(self, ctx, data):
        """
        The demo widget
        """
        self.wid = wid = RandomNumber(rate=50)
        wid.setFragmentParent(self)
        return ctx.tag[wid]

    def render_source(self, ctx, data):
        ctx.tag.fillSlots('sourceFile', RESOURCE('example.py'))
        return ctx.tag


class RandomNumber(athena.LiveElement):
    """
    Generate random numbers on the server.  When one of them matches a
    particular pattern, send it to the client.
    """
    running = None
    jsClass = u'Chichimec.RandomNumber'
    docFactory = genshifile(RESOURCE('templates/RandomNumber'))

    @athena.expose
    def setFilter(self, num):
        """
        Set a new number filter.  num should be an integer 3 digits or less,
        it will be compared with the final digits of the numbers this widget
        generates on the server.

        If this has never been called before, it also starts the ticker
        running.
        """
        self.filter = num
        if not self.running:
            self.running = self.task.start(1.0 / self.rate, now=False)
        msg = u"Recording new filter: numbers that end with %s" % (num,)
        log.msg(msg)
        return msg

    def number(self):
        """
        Generate a number
        """
        r = int(random.randint(100000, 999999))
        if str(r).endswith(str(self.filter)):
            log.msg("Recording new matching number %s" % (r,))
            return self.callRemote('number', r).addCallback(lambda q: r)
        else:
            return defer.succeed(r)

    def __init__(self, rate, *a, **kw):
        self.rate = rate
        self.task = task.LoopingCall(self.number)

    def detached(self):
        """
        Clean up the looping call we created
        """
        self.task.stop()
