"""
Create the boilerplate for a new Chichimec-based web application
"""
import sys
import os
import shutil
from inspect import cleandoc
import subprocess

from twisted.python import usage

from chichimec.util import nameFix
from chichimec import bootstrap as bs

def index2Tuples(s):
    """
    RePack a string containing "key   value" pairs into a dict
    """
    r = {}
    s = cleandoc(s).strip().splitlines()
    for id, name in [x.split() for x in s]:
        r[id.strip()] = name.strip()

    return r

EASY_INSTALLABLE = index2Tuples("""
    genshi      Genshi
    storm       storm
    fudge       fudge
    pyflakes    pyflakes
    txgenshi    txGenshi
    twisted     Twisted
    nevow       Nevow
    virtualenv  virtualenv
    """)

MISC_PACKAGES = index2Tuples("""
    jquery      jQuery
    """)

EXCLUDEABLE_PACKAGES = 'fudge genshi storm fudge pyflakes jquery'.split()


class Options(usage.Options):
    """
    Create 
    """
    synopsis = "boilerplate [options] PROJECT"
    optFlags = [ ["best-practices", None, 
            "Create a project configured with all the goodies"],
        ["develop", None,
            "Run in development mode, which does everything locally",],
        ]

    def __init__(self, *a, **kw):
        optFlags = Options.optFlags
        for k in EXCLUDEABLE_PACKAGES:
            v = EASY_INSTALLABLE.get(k, MISC_PACKAGES.get(k, None))
            optFlags.append(['no-%s' % (k,), None, 'Do not include %s' % (v,)])
        usage.Options.__init__(self, *a, **kw)

    def parseArgs(self, project):
        self['projectDir'] = project
        self['projectName'] = nameFix(project)

    def postOptions(self):
        os.mkdir(self['projectDir'])

        # write python files
        pys = bs.genPython(self)
        for fn in pys:
            try:
                os.makedirs(os.path.dirname(fn))
            except OSError, e:
                if e.errno != 17:
                    raise
            open(fn, 'w').write(pys[fn])

        os.makedirs('%s/%s/static' % (self['projectDir'], self['projectName']))
        os.makedirs('%s/%s/static/css' % (self['projectDir'], self['projectName']))
        os.makedirs('%s/%s/templates' % (self['projectDir'], self['projectName']))

        # write jquery, maybe
        if not self['no-jquery']:
            shutil.copyfile(bs.YOURPROJECT('yourproject/static/jquery-1.3.2.js'),
                ('{options[projectDir]}/{options[projectName]}/static/jquery-1.3.2.js'
                ).format(options=self))
            shutil.copyfile(bs.YOURPROJECT('yourproject/static/yourproject.js'),
                ('{options[projectDir]}/{options[projectName]}/static/{options[projectName]}.js'
                ).format(options=self))

        # write css
        shutil.copyfile(bs.YOURPROJECT('yourproject/static/css/yourproject.css'),
            ('{options[projectDir]}/{options[projectName]}/static/css/{options[projectName]}.css'
            ).format(options=self))

        # write xml template
        xmltpl = bs.genTemplateXML(self)
        xmltplFile = (
                '{o[projectDir]}/{o[projectName]}/templates/{o[projectName]}.xhtml'
                ).format(o=self)
        open(xmltplFile, 'w').write(xmltpl)

        ps = []
        # figure out what scripts we're including
        for k in EASY_INSTALLABLE:
            ps.append("'%s'," % (EASY_INSTALLABLE[k],))
        self['optionalScripts'] = '\n'.join(ps)

        bstxt = bs.genBootstrap(self)
        bsFile = '%s/bootstrap.py' % (self['projectDir'],)
        open(bsFile, 'w').write(bstxt)
        os.chmod(bsFile, 0o755)

        proc = subprocess.Popen([bsFile, self['projectDir']],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
        stdout = proc.communicate()[0]
        assert proc.returncode == 0, stdout
        self['virtualenvOutput'] = '\n'.join(['> ' + x for x in
            stdout.splitlines()])


def run(argv=None):
    if argv is None:
        argv = sys.argv
    o = Options()
    try:
        o.parseOptions(argv[1:])
    except usage.UsageError, e:
        if hasattr(o, 'subOptions'):
            print str(o.subOptions)
        else:
            print str(o)
        print str(e)
        return 1

    return 0

