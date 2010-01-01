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
        elif '=' in val:
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
            source = 'YourProject/' + source
            data = open(RESOURCE(source)).read()
            if not flags.get('no-format'):
                data = data.format(options=options)
            target = options['projectDir'] + '/' + target
            filename = target.format(options=options)
            yield flags, filename, data


generatedFiles = ( # {{{
"""
setup.py                                    setup.py                                                         ~
README                                      README                                                           ~

yourproject/__init__.py                     {options[projectName]}/__init__.py                               ~
yourproject/resource.py                     {options[projectName]}/resource.py                               ~
yourproject/static/css/yourproject.css      {options[projectName]}/static/css/{options[projectName]}.css     ~
yourproject/templates/yourproject.xhtml     {options[projectName]}/templates/{options[projectName]}.xhtml    ~
nevow/plugins/yourprojectnp.py              nevow/plugins/{options[projectName]}np.py                        ~
twisted/plugins/yourprojecttp.py            twisted/plugins/{options[projectName]}tp.py                      ~

yourproject/static/jquery-1.3.2.js          {options[projectName]}/static/jquery-1.3.2.js                    jquery,no-format
yourproject/static/YourProject/__init__.js  {options[projectName]}/static/{options[projectDir]}/__init__.js  jquery,no-format

runtests                                    runtests                                                         mode=0o755,best-practices
.hgignore                                   .hgignore                                                        best-practices

yourproject/test/__init__.py                {options[projectName]}/test/__init__.py                          best-practices
yourproject/test/test_twistdplugin.py       {options[projectName]}/test/test_twistdplugin.py                 best-practices
yourproject/test/test_nevowplugin.py        {options[projectName]}/test/test_nevowplugin.py                  best-practices
yourproject/test/test_resource.py           {options[projectName]}/test/test_resource.py                     best-practices
""") # }}}
