"""
HTTP-accessible Resources for {options[projectDir]}
"""

from nevow import athena, loaders, static, url

from chichimec.resource import DefaultResource

from {options[projectName]} import RESOURCE


class {options[projectDir]}Page(athena.LivePage):
    docFactory = loaders.xmlfile(RESOURCE('templates/{options[projectName]}.xhtml'))
    addSlash = True


class Root(DefaultResource):
    """
    Adds child nodes for things common to anonymous and logged-in root
    resources:

    /static goes to the project's static directory
    /app goes to the main application (this is required to be a non-root
    resource, for Athena to work.)

    / redirects to /app
    """
    addSlash = True  # yeah, we really do need this, otherwise 404 on /

    def child_static(self, ctx):
        return static.File(RESOURCE('static'))

    def child_app(self, ctx):
        return {options[projectDir]}Page()

    def renderHTTP(self, ctx):
        return url.root.child("app")

