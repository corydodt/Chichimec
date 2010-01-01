"""
Example page resources.  Boilerplate apps will import these.
"""
from datetime import datetime
import random

from twisted.internet import task

from nevow import athena, rend, loaders

from chichimec.util import RESOURCE

from txgenshi.loader import genshifile

class GenshiMixPage(rend.Page):
    """
    Example page with genshi templates demo
    """
    docFactory = genshifile(RESOURCE('templates/genshimix.xhtml'))
    addSlash = True

    def __init__(self, *args, **kwds):
        rend.Page.__init__(self, *args, **kwds)
        self.key = {'value': 'this is the value of the key'}
        self.doIt = True
        self.items = xrange(10)
        evenOdd = ['odd', 'even']
        self.altItems = [ (x, {'class': evenOdd[x % 2]})
            for x in list(xrange(10))]
        self.username = u'Joe'

    def date(self):
        """
        Right now, formatted as a dotted date
        """
        return datetime.now().strftime("%Y.%m.%d %H:%M:%S")

    date = property(date)

    def render_username(self, context, data):
        """
        It's Joe.
        """
        return self.username


class AthenaPage(athena.LivePage):
    """
    Example page with athena demo
    """
    docFactory = loaders.xmlfile(RESOURCE('templates/athena.xhtml'))

    def render_random(self, ctx, data):
        """
        The demo widget
        """
        wid = RandomNumber()
        wid.setFragmentParent(self)
        return ctx.tag[wid]

class RandomNumber(athena.LiveElement):
    """
    Generate random numbers on the server.  When one of them matches a
    particular pattern, send it to the client.
    """
    running = None
    jsClass = u'Chichimec.RandomNumber'
    docFactory = loaders.xmlfile(RESOURCE('templates/RandomNumber'))

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
            self.running = self.task.start(0.2)
        return 'ok'

    def number(self):
        """
        Generate a number
        """
        r = int(random.random() * 1000000)
        if str(r).endswith(str(self.filter)):
            d = self.callRemote('number', r)

    def __init__(self, *a, **kw):
        self.task = task.LoopingCall(self.number)
