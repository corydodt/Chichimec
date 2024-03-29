try:
    import setuptools
    setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools import setup
# cannot use find_packages, because nevow.plugins is not found (it lacks
# __init__.py on purpose)
setup(name='Chichimec',
      version='0.1.0',
      author='Cory Dodt',
      description='Chichimec: A repackaging of Twisted Web with goodness',
      url='http://goonmill.org/chichimec/',
      download_url='http://chichimec-source.goonmill.org/archive/tip.tar.gz',

      packages=['chichimec', 'chichimec.test', 'chichimec.scripts',
          'nevow.plugins',
          ],

      scripts=['bin/boilerplate',],

      install_requires=[
          'Distribute>=0.6.10',
          'Twisted>=9.0.0',
          'Nevow',
          'fudge',
          'virtualenv>=1.4.3',
          'txGenshi>=0.0.1.0cdd1',
          'Genshi',
          ],

      package_data={
          'chichimec': ['templates/genshimix.xhtml',
                        'templates/athena.xhtml',
                        'templates/RandomNumber',
                        'static/Chichimec/__init__.js'],
        },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries',
          ],

      )
