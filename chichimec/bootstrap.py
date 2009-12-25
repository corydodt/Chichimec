"""
Tool for building bootstrap scripts for applications.
"""
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

    dev = '"-HNone -f{devDir}",'.format(devDir=RESOURCE('dist')) if options['develop'] else ''

    tpl = cleandoc("""
        import os, subprocess
        setupCode = "{genSetup}"
        open('{options[projectDir]}/setup.py', 'w').write(setupCode)
        def after_install(options, home_dir):
            subprocess.call([join(home_dir, 'bin', 'easy_install'), 
            {developmentMode} '{options[projectDir]}'])
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
