"""
Create the boilerplate for a new Chichimec-based web application
"""
import sys
import os
import shutil
from inspect import cleandoc
import subprocess
import glob

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
    chichimec   Chichimec
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

EXCLUDEABLE_PACKAGES = 'txgenshi genshi storm pyflakes jquery'.split()


class Options(usage.Options):
    """
    Create a shell of files for starting a web app
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

        # by default, exclude pyflakes
        for k in ('pyflakes',):
            self['no-'+k] = True

    def parseArgs(self, project):
        self['projectDir'] = project
        self['projectName'] = nameFix(project)

    def selectDependencies(self):
        """
        Set self['selectedDependencies'] based on rules and command-line flags
        """
        # when best-practices is turned on, include everything
        ps = []
        ps2 = []
        if self['best-practices']:
            for k in EASY_INSTALLABLE:
                ps.append("'%s'," % (EASY_INSTALLABLE[k],))
                ps2.append(EASY_INSTALLABLE[k])
        else:
            for k in EASY_INSTALLABLE:
                if not self.get('no-'+k, False):
                    ps.append("'%s'," % (EASY_INSTALLABLE[k],))
                    ps2.append(EASY_INSTALLABLE[k])
        self['selectedDependencies'] = '\n'.join(ps)
        self['selectedDependenciesNames'] = ps2

    def postOptions(self):
        # figure out what scripts we're including
        self.selectDependencies()

        # write python files
        def save(fn, data):
            try:
                os.makedirs(os.path.dirname(fn))
            except OSError, e:
                if e.errno != 17:
                    raise # pragma: no cover
            open(fn, 'w').write(data)

        for flags, filename, data in bs.generate(self):
            if flags.get('jquery') and self['no-jquery']:
                continue
            if flags.get('best-practices') and not self['best-practices']:
                continue

            save(filename, data)
            if flags.get('mode'):
                os.chmod(filename, int(flags['mode'], 8))

        # copy the distribute tarball when it's handy.  This speeds up env
        # creation.
        distributeTarball = glob.glob('distribute-*.tar.gz')
        if distributeTarball:
            shutil.copyfile(distributeTarball[0], self['projectDir'])

        # write bootstrap file
        bstxt = bs.genBootstrap(self)
        bsFile = '%s/bootstrap.py' % (self['projectDir'],)
        open(bsFile, 'w').write(bstxt)
        os.chmod(bsFile, 0o755)

        # run the bootstrap file
        proc = subprocess.Popen([bsFile, '--distribute', '--no-site-packages', self['projectDir']],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
        stdout = proc.communicate()[0]
        assert proc.returncode == 0, stdout

        # save the output of running bootstrap in case we need to diagnose
        # later
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

