"""
Twistd plugin to run PerkCategorizer.

Twisted 2.5 or later is required to use this.
"""

from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application.internet import TCPServer

class Options(usage.Options):
    optParameters = [['port', 'p', '7000', 'Port to run on'],
                     ]


class {options[projectDir]}ServerMaker(object):
    """
    Framework boilerplate class: This is used by twistd to get the service
    class.

    Basically exists to hold the IServiceMaker interface so twistd can find
    the right makeService method to call.
    """
    implements(IServiceMaker, IPlugin)
    tapname = "{options[projectName]}"
    description = "YOU SHOULD FILL IN A DESCRIPTION"
    options = Options

    def makeService(self, options):
        """
        Construct the service
        """
        from chichimec.webserver import WebSite
        site = WebSite()
        ws = TCPServer(int(options['port']), site)
        ws.site = site
        return ws

# Now construct an object which *provides* the relevant interfaces

# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = {options[projectDir]}ServerMaker()
