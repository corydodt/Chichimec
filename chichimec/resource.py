"""
Main resources go here
"""

from nevow import rend


class RootFactory(object):
    """
    Creates the root resource
    """
    rootClass = None

    def createRoot(self, *a, **kw):
        """
        Return a root resource
        """
        return RootFactory.rootClass(*a, **kw)


class DefaultResource(rend.Page):
    """
    Do-nothing resource
    """
    @classmethod
    def setAsRoot(cls):
        RootFactory.rootClass = cls
