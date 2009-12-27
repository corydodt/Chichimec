
start:
	hg serve --daemon --port 28094 --pid-file hgserve.pid -E hgserve.log

stop:
	kill `cat hgserve.pid`

