#!/usr/bin/env python
import os
import sys
import Settings

from daemon import Daemon

def Main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burn.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['HttpServer.py', 'runserver', '%s:%s' % (Settings.IPADDRESS,Settings.PORT)])



class main_daemon(Daemon):
    def run(self):
        try:
    	    Main()
	except KeyboardInterrupt:
	    sys.exit()	    

if __name__ == "__main__":
	daemon = main_daemon('./pid/HttpServer.pid', stdout='./log/HttpServer.log', stderr='./log/HttpServer.log')
	if len(sys.argv) == 2:
		if 'start'     == sys.argv[1]:
			daemon.start()
		elif 'stop'    == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'run'     == sys.argv[1]:
			daemon.run()
		elif 'status'  == sys.argv[1]:
			daemon.status()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|run" % sys.argv[0]
		sys.exit(2)
