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
        os.mkdir(self['projectDir'])

        # write python files
        pys = bs.genPython(self)
        def save(fn):
            realFN = fn.format(options=self)
            try:
                os.makedirs(os.path.dirname(realFN))
            except OSError, e:
                if e.errno != 17:
                    raise # pragma: no cover
            open(realFN, 'w').write(pys[fn])

        save('{options[projectDir]}/{options[projectName]}/__init__.py')
        save('{options[projectDir]}/{options[projectName]}/resource.py')
        save('{options[projectDir]}/twisted/plugins/{options[projectName]}tp.py')
        save('{options[projectDir]}/nevow/plugins/{options[projectName]}np.py')

        if self['best-practices']:
            save('{options[projectDir]}/{options[projectName]}/test/__init__.py')
            save('{options[projectDir]}/{options[projectName]}/test/test_{options[projectName]}.py')
            save('{options[projectDir]}/{options[projectName]}/test/test_twistdplugin.py')

        os.makedirs('%s/%s/static' % (self['projectDir'], self['projectName']))
        os.makedirs('%s/%s/static/css' % (self['projectDir'], self['projectName']))
        os.makedirs('%s/%s/templates' % (self['projectDir'], self['projectName']))

        # write jquery, maybe
        if self['best-practices'] or not self['no-jquery']:
            shutil.copyfile(bs.YOURPROJECT('yourproject/static/jquery-1.3.2.js'),
                ('{o[projectDir]}/{o[projectName]}/static/jquery-1.3.2.js'
                ).format(o=self))
            shutil.copyfile(bs.YOURPROJECT('yourproject/static/yourproject.js'),
                ('{o[projectDir]}/{o[projectName]}/static/{o[projectName]}.js'
                ).format(o=self))

        # write css
        shutil.copyfile(bs.YOURPROJECT('yourproject/static/css/yourproject.css'),
            ('{o[projectDir]}/{o[projectName]}/static/css/{o[projectName]}.css'
            ).format(o=self))

        # write xml template
        xmltpl = bs.genTemplateXML(self)
        xmltplFile = (
                '{o[projectDir]}/{o[projectName]}/templates/{o[projectName]}.xhtml'
                ).format(o=self)
        open(xmltplFile, 'w').write(xmltpl)

        # figure out what scripts we're including
        self.selectDependencies()

        # write README
        readme = bs.genREADME(self)
        open(self['projectDir'] + '/README', 'w').write(readme)

        # write runtests when best-practices
        runtests = bs.genRunTests(self)
        runtestsFN = self['projectDir'] + '/runtests'
        open(runtestsFN, 'w').write(runtests)
        os.chmod(runtestsFN, 0o755)

        # write .hgignore when best-practices.
        if self['best-practices']:
            shutil.copyfile(bs.YOURPROJECT('.hgignore'),
                ('{o[projectDir]}/.hgignore').format(o=self))

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

