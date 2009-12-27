"""
Create the boilerplate for a new Chichimec-based web application
"""
import sys
import os
from inspect import cleandoc
import subprocess

from twisted.python import usage

from chichimec.util import nameFix
from chichimec.bootstrap import genBootstrap

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

        ps = []
        # figure out what scripts we're including
        for k in EASY_INSTALLABLE:
            ps.append("'%s'," % (EASY_INSTALLABLE[k],))
        self['optionalScripts'] = '\n'.join(ps)

        bs = genBootstrap(self)
        bsFile = '%s/bootstrap.py' % (self['projectDir'],)
        open(bsFile, 'w').write(bs)
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

