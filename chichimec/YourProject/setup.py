try:
    import setuptools
    setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages
setup(name='{options[projectDir]}',
      version='YOU SHOULD SET THE VERSION',
      author='YOU SHOULD SET THE AUTHOR',
      description='{options[projectDir]}: YOU SHOULD SET THE DESCRIPTION',
      url='YOU SHOULD SET THE URL',
      download_url='YOU SHOULD SET THE DOWNLOAD URL',

      packages=find_packages(),

      scripts=['bin/activate',
          ],

      install_requires=[
          'Distribute>=0.6.10',
          'Twisted>=9.0.0',
          'Nevow',
          'Chichimec',
          'virtualenv>=1.4.3',
{options[selectedDependencies]}
          ],

      package_data={{
          '{options[projectName]}': [ 'sql/*.sql', 
              'templates/*',
              'static/*.css',
              'static/*.js',
              'static/*.gif',
              'static/*.png',
              'static/*.jpg',
              'static/{options[projectDir]}/*.js',
              ],
        }},
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Programming Language :: Python',
          ],

      )
