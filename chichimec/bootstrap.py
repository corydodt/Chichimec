"""
Tool for building bootstrap scripts for applications.
"""
import os
from string import Template
from inspect import cleandoc

import virtualenv

from chichimec.util import RESOURCE

YOURPROJECT = lambda s: RESOURCE('YourProject/' + s)

def genSetup(options):
    """
    Generate a setup script as a string
    """
    input = open(YOURPROJECT('setup.py')).read()
    return input.format(options=options)


def genBootstrap(options):
    """
    Get the bootstrap file as a string
    """
    setup = genSetup(options).encode('string-escape')

    devDir = os.path.abspath(RESOURCE('../dist'))
    dev = '"-HNone", "-f{devDir}",'.format(devDir=devDir) if options['develop'] else ''

    tpl = cleandoc("""
        import os, subprocess
        setupCode = "{genSetup}"
        open('{options[projectDir]}/setup.py', 'w').write(setupCode)
        def after_install(options, home_dir):
            args = [join(home_dir, 'bin', 'easy_install'), {developmentMode} '{options[projectDir]}', {options[optionalScripts]}]
            subprocess.call(args)
        def adjust_options(options, args):
            options.distribute = True
            setattr(options, 'no-site-packages', True)
        """).format(options=options, genSetup=setup,
                developmentMode=dev)

    output = virtualenv.create_bootstrap_script(tpl)
    return output


def genREADME(options):
    """
    Get the README file as a string
    """
    input = open(YOURPROJECT('README')).read()
    return input.format(options)
