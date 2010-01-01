try:
    import setuptools
    setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages
setup(name='Chichimec',
      version='0.1.0',
      author='Cory Dodt',
      description='Chichimec: A repackaging of Twisted Web with goodness',
      url='http://goonmill.org/chichimec/',
      download_url='http://chichimec-source.goonmill.org/archive/tip.tar.gz',

      packages=find_packages(),

      scripts=['bin/boilerplate',],

      install_requires=[
          'Distribute>=0.6.10',
          'Twisted>=9.0.0',
          'Nevow',
          'fudge',
          'virtualenv>=1.4.3',
          'txGenshi>=0.0.2-cdd1',
          'Genshi',
          ],

      package_data={
          'chichimec': ['data/data.data',
              ],
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
