"""
The boilerplate behind the resources.  Start services and stuff like that.
"""
from twisted.python import log

from nevow import appserver

from chichimec.resource import DefaultResource

class WebSite(appserver.NevowSite):
    """Website with <80 column logging"""
    rootClass = DefaultResource

    def __init__(self, *a, **kw):
        root = self.rootClass()
        appserver.NevowSite.__init__(self, root, *a, **kw)

    def log(self, request):
        uri = request.uri

        if 'jsmodule' in uri:
            uris = uri.split('/')
            n = uris.index('jsmodule')
            uris[n-1] = uris[n-1][:3] + '...'
            uri = '/'.join(uris)

        if len(uri) > 38:
            uri = '...' + uri[-35:]

        code = request.code
        if code != 200:
            code = '!%s!' % (code, )

        log.msg('%s %s' % (code, uri), system='HTTP', )

