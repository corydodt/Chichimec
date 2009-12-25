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
    import pudb; pudb.set_trace()
    setup = genSetup(options).encode('string-escape')
    name = options['projectName']
    theDir = options['projectDir']

    dev = '"-HNone -f{devDir}",'.format(devDir=RESOURCE('dist') if options['develop'] else '')

    tpl = cleandoc("""
        import os, subprocess
        setupCode = "{genSetup}"
        setupPy = '{options[projectDir]}/setup.py'
        open(setupPy, 'w').write(setupCode)
        def after_install(options, home_dir):
            subprocess.call([join(home_dir, 'bin', 'easy_install'), 
            {developmentMode} setupPy])
        """).format(options=options, genSetup=genSetup,
                developmentMode=dev)

    output = virtualenv.create_bootstrap_script(tpl)
    return output

def genREADME(options):
    """
    Get the README file as a string
    """
    name = options['projectName']
    theDir = options['projectDir']
    input = open(YOURPROJECT('README')).read()
    return input.format(options)
