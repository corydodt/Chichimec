"""
Tests for the creation of boilerplates
"""
import os

from twisted.trial import unittest

from chichimec.scripts import boilerplate

class BoilerplateTest(unittest.TestCase):
    """
    Test the operations that write out a project dir
    """
    def assertFiles(self, *files):
        """
        Check that each arg filename exists in the current directory.
        """
        for f in files:
            if os.path.isdir(f):
                continue 
            else:
                self.assertTrue(open(f),
                        "%s did not exist or was not readable" % (f,))

    def test_newProject(self):
        """
        New projects create a deployment with all the juicy bits
        """
        boilerplate.run(['boilerplate', 'TestProject_'])
        self.assertFiles(*['TestProject_/' + x for x in ['bin/activate',
            'testproject/__init__.py', 'nevow/plugins/testproject.py',
            'twisted/plugins/testproject.py',
            'testproject/static/testproject.js',
            'testproject/static/jquery-1.3.2.js',
            'testproject/templates/'
            'lib/pythonx.x/site-packages/Chichimec.egg',
            'lib/pythonx.x/site-packages/Genshiblah.egg',
            'lib/pythonx.x/site-packages/txGenshi.egg',
            'lib/pythonx.x/site-packages/Hypy.egg',
            'lib/pythonx.x/site-packages/Twisted.egg',
            'lib/pythonx.x/site-packages/Nevow.egg',
            'lib/pythonx.x/site-packages/Distribute.egg',
            'lib/pythonx.x/site-packages/Virtualenv.egg',
            ]])

    def test_cherryPick(self):
        """
        You can exclude bits of a deployment with --no-*
        """
        self.assertTrue(False)
        boilerplate.run(['boilerplate', '--no-genshi', 'TestProject__', ])

    test_cherryPick.todo = "todo"

    def test_bestPractices(self):
        """
        Test directory &c. are created with --best-practices
        """
        boilerplate.run(['boilerplate', '--best-practices', 'TestProject___', ])
        self.assertFiles(*['TestProject___/' + x for x in ['bin/activate',
            '.hgignore', 'testproject/test/test_testproject.py',
            'lib/pythonx.x/site-packages/pyflakes.egg',
            'lib/pythonx.x/site-packages/fudge.egg',
            ]])
