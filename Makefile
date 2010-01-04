
start:
	hg serve --daemon --port 28094 --pid-file hgserve.pid -E hgserve.log

stop:
	kill `cat hgserve.pid`

# get eggs for all the software our projects will need.  this makes it easier
# to run tests.
localPackages:
	if [ $${#TXGDEV} -gt 0 ]; then $(MAKE) _reinstallTXG; fi
	rm -rf dist/Chichimec* dist/txGenshi*
	easy_install-2.6 -f support/ -maxd dist/ . Nevow pyflakes distribute fudge Genshi virtualenv zope.interface Twisted storm
	python -c 'from distribute_setup import download_setuptools; download_setuptools()'

support:
	rm -rf support/txGenshi*
	easy_install-2.6 -zmaxd support/ ../txGenshi

_reinstallTXG:
	$(MAKE) support
	sudo easy_install-2.6 -fsupport -U txGenshi 


.PHONY: support
