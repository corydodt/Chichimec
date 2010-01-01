"""
Tests for the creation of boilerplates
"""
import sys
import io
import glob
import subprocess

from twisted.trial import unittest

from chichimec.scripts import boilerplate

class BoilerplateTest(unittest.TestCase):
    """
    Test the operations that write out a project dir
    """
    def runBoilerplate(self, *args):
        """
        Invoke the boilerplate script with our own setup
        """
        o = boilerplate.Options()
        o['develop'] = True
        o.parseOptions(*args)
        return o

    def assertNoFiles(self, files, messageFn=None):
        """
        Check that each arg filename DOES NOT EXIST in the current directory.
        """
        for f in files:
            if glob.glob(f) != []:
                if messageFn:
                    msg = messageFn(f)
                    self.assertTrue(False, msg)
                else:
                    self.assertTrue(False, "%s should not have existed" % (f,))

    def assertFiles(self, files, messageFn=None):
        """
        Check that each arg filename exists in the current directory.
        """
        for f in files:
            if len(glob.glob(f)) == 0:
                if messageFn:
                    msg = messageFn(f)
                    self.assertTrue(False, msg)
                else:
                    self.assertTrue(False, "%s could not be opened" % (f,))

    def test_newProject(self):
        """
        New projects create a deployment with all the juicy bits
        """
        o = self.runBoilerplate(['TestProject_'])
        outp = o['virtualenvOutput']
        messageFn = lambda x: "%s could not be opened; %s" % (x, outp)
        self.assertFiles(['TestProject_/' + x for x in ['bin/activate',
            'testproject/__init__.py', 
            'testproject/resource.py', 
            'README',
            'nevow/plugins/testprojectnp.py',
            'twisted/plugins/testprojecttp.py',
            'testproject/static/TestProject_/__init__.js',
            'testproject/static/jquery-1.3.2.js',
            'testproject/static/css/testproject.css',
            'testproject/templates/testproject.xhtml',
            'lib/python*/site-packages/Chichimec*.egg',
            'lib/python*/site-packages/Genshi*.egg',
            'lib/python*/site-packages/txGenshi*.egg',
            'lib/python*/site-packages/Twisted*.egg',
            'lib/python*/site-packages/Nevow*.egg',
            'lib/python*/site-packages/distribute*.egg',
            'lib/python*/site-packages/virtualenv*.egg',
            ]], messageFn)

        self.assertNoFiles(['TestProject_/' + x for x in
            ['testproject/test/__init__.py',
             '.hgignore',
             'lib/python*/site-packages/pyflakes*.egg',
             ]])

    def test_cherryPick(self):
        """
        You can exclude bits of a deployment with --no-*
        """
        self.runBoilerplate(['--no-genshi', '--no-txgenshi', 'TestProject__', ])
        self.assertFiles(['TestProject__/testproject/__init__.py'])
        self.assertNoFiles(['TestProject__/lib/python*/site-packages/txGenshi*.egg',
                'TestProject__/lib/python*/site-packages/Genshi*.egg',
                ])

    def test_selectDependencies(self):
        def doTest(options, expected):
            o = boilerplate.Options()
            o.postOptions = lambda: None
            o.parseOptions(options)
            o.selectDependencies()
            self.assertEqual(
                    sorted(o['selectedDependenciesNames']),
                    expected)

        # default packages
        doTest(["Dummy"], 
            ['Chichimec', 'Genshi', 'Nevow', 'Twisted', 'fudge', 'storm', 'txGenshi', 'virtualenv'])
        # all packages
        doTest(['--best-practices', 'Dummy', ],
            ['Chichimec', 'Genshi', 'Nevow', 'Twisted', 'fudge', 'pyflakes', 'storm',
                'txGenshi', 'virtualenv'])
        # simple exclusion
        doTest(['--no-txgenshi', 'Dummy', ],
            ['Chichimec', 'Genshi', 'Nevow', 'Twisted', 'fudge', 'storm',  'virtualenv'])
        # multiple exclusion
        doTest(['--no-storm', '--no-txgenshi', 'Dummy', ],
            ['Chichimec', 'Genshi', 'Nevow', 'Twisted',  'fudge', 'virtualenv'])
        # --best-practices overrides --no-foo exclusions 
        doTest(['--best-practices', '--no-txgenshi', 'Dummy', ],
            ['Chichimec', 'Genshi', 'Nevow', 'Twisted', 'fudge', 'pyflakes', 'storm',
                'txGenshi', 'virtualenv'])

    def test_bestPractices(self):
        """
        Test directory &c. are created with --best-practices
        """
        o = self.runBoilerplate(['--best-practices', 'TestProject___', ])
        outp = o['virtualenvOutput']
        messageFn = lambda x: "%s could not be opened; %s" % (x, outp)
        self.assertFiles(['TestProject___/' + x for x in ['bin/activate',
            '.hgignore', 
            'runtests',
            'testproject/test/__init__.py',
            'lib/python*/site-packages/pyflakes*.egg',
            'lib/python*/site-packages/fudge*egg',
            ]], messageFn)

    def test_generated(self):
        """
        Run the tests we generated in the boilerplate!
        """
        o = self.runBoilerplate(['--best-practices', 'TestProject____', ])
        subprocess.check_call('TestProject____/runtests')


class RunTest(unittest.TestCase):
    """
    The run function works
    """
    def test_run(self):
        sys.stderr = io.BytesIO()
        sys.stdout = io.BytesIO()
        try:
            self.assertRaises(SystemExit, boilerplate.run, ['boilerplate', '--help'])
        finally:
            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__

