"""
Tool for building bootstrap scripts for applications.
"""
import os
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
            args = [join(home_dir, 'bin', 'easy_install'), {developmentMode} {options[selectedDependencies]}]
            subprocess.call(args)
        """).format(options=options, genSetup=setup,
                developmentMode=dev)

    output = virtualenv.create_bootstrap_script(tpl)
    return output


def genRunTests(options):
    """
    Get the runtests script as a string
    """
    return formatFile(YOURPROJECT('runtests'), options)


def genREADME(options):
    """
    Get the README file as a string
    """
    return formatFile(YOURPROJECT('README'), options)


def formatFile(file, options, **kw):
    """
    Open and read file and emit a string of its contents, formatted using
    options as an argument, and other kw as specified
    """
    input = open(file).read()
    return input.format(options=options, **kw)


def genPython(options):
    """
    Get all the python modules to be generated as a dictionary of strings
    """
    r = {}
    r['{options[projectDir]}/{options[projectName]}/__init__.py'] = formatFile(
            YOURPROJECT('yourproject/__init__.py'), options)
    r['{options[projectDir]}/{options[projectName]}/resource.py'] = formatFile(
            YOURPROJECT('yourproject/resource.py'), options)
    r['{options[projectDir]}/{options[projectName]}/test/__init__.py'] = formatFile(
            YOURPROJECT('yourproject/test/__init__.py'), options)
    r['{options[projectDir]}/{options[projectName]}/test/test_{options[projectName]}.py'] = formatFile(
            YOURPROJECT('yourproject/test/test_yourproject.py'), options)
    r['{options[projectDir]}/twisted/plugins/{options[projectName]}.py'] = formatFile(
            YOURPROJECT('twisted/plugins/yourproject.py'), options)
    r['{options[projectDir]}/nevow/plugins/{options[projectName]}.py'] = formatFile(
            YOURPROJECT('nevow/plugins/yourproject.py'), options)
    return r


def genTemplateXML(options):
    """
    Get the XML for the template file we include
    """
    return formatFile(YOURPROJECT('yourproject/templates/yourproject.xhtml'),
            options)
