
start:
	hg serve --daemon --port 28094 --pid-file hgserve.pid -E hgserve.log

stop:
	kill `cat hgserve.pid`

# get eggs for all the software our projects will need.  this makes it easier
# to run tests.
localPackages:
	easy_install-2.6 -maxd dist/ . Nevow pyflakes distribute fudge Genshi virtualenv zope.interface Twisted storm
	cp support/txGenshi-0.0.1-py2.6.egg dist/
	python -c 'from distribute_setup import download_setuptools; download_setuptools()'
