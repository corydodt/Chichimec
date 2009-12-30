"""
Tool for building bootstrap scripts for applications.
"""
import os
from inspect import cleandoc

import virtualenv

from chichimec.util import RESOURCE

def genBootstrap(options):
    """
    Get the bootstrap file as a string
    """
    devDir = os.path.abspath(RESOURCE('../dist'))
    dev = '"-HNone", "-f{devDir}",'.format(devDir=devDir) if options['develop'] else ''

    tpl = cleandoc("""
        import subprocess
        def after_install(options, home_dir):
            args = [join(home_dir, 'bin', 'easy_install'), {developmentMode} {options[selectedDependencies]}]
            subprocess.call(args)
        """).format(options=options, 
                developmentMode=dev)

    output = virtualenv.create_bootstrap_script(tpl)
    return output


def parseFlags(f):
    """
    Extract flags from a flag-string
    """
    vals = f.split(',')
    r = {}
    for val in vals:
        if val == '~':
            continue
        elif '=' in f:
            k, v = val.split('=', 1)
            r[k] = v
        else:
            r[val] = True
    return r


def generate(options):
    """
    Take our mini-language for copying files and produce the files, flags and
    data that need to be copied into the boilerplated dir
    """
    for line in generatedFiles.splitlines():
        line = line.strip()
        if line:
            source, target, flags = line.split()
            if flags:
                flags = parseFlags(flags)
            data = open(RESOURCE(source)).read()
            if not flags.get('no-format'):
                data = data.format(options=options)
            filename = target.format(options=options)
            yield flags, filename, data


generatedFiles = ( # {{{
"""
YourProject/setup.py    {options[projectDir]}/setup.py  ~
YourProject/yourproject/__init__.py {options[projectDir]}/{options[projectName]}/__init__.py    ~
YourProject/yourproject/resource.py {options[projectDir]}/{options[projectName]}/resource.py    ~
YourProject/twisted/plugins/yourprojecttp.py {options[projectDir]}/twisted/plugins/{options[projectName]}tp.py  ~
YourProject/nevow/plugins/yourprojectnp.py {options[projectDir]}/nevow/plugins/{options[projectName]}np.py  ~
YourProject/yourproject/test/__init__.py {options[projectDir]}/{options[projectName]}/test/__init__.py  best-practices
YourProject/yourproject/test/test_yourproject.py {options[projectDir]}/{options[projectName]}/test/test_{options[projectName]}.py  best-practices
YourProject/yourproject/test/test_twistdplugin.py {options[projectDir]}/{options[projectName]}/test/test_twistdplugin.py   best-practices
YourProject/yourproject/test/test_nevowplugin.py {options[projectDir]}/{options[projectName]}/test/test_nevowplugin.py best-practices
YourProject/yourproject/static/jquery-1.3.2.js {options[projectDir]}/{options[projectName]}/static/jquery-1.3.2.js jquery,no-format
YourProject/yourproject/static/YourProject/__init__.js {options[projectDir]}/{options[projectName]}/static/{options[projectDir]}/__init__.js jquery,no-format
YourProject/yourproject/static/css/yourproject.css  {options[projectDir]}/{options[projectName]}/static/css/{options[projectName]}.css  ~
YourProject/yourproject/templates/yourproject.xhtml {options[projectDir]}/{options[projectName]}/templates/{options[projectName]}.xhtml ~
YourProject/README      {options[projectDir]}/README    ~
YourProject/runtests    {options[projectDir]}/runtests  mode=0o755
YourProject/.hgignore   {options[projectDir]}/.hgignore best-practices
""") # }}}
