#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Stand alone script
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.core.management import setup_environ
from burn import settings
setup_environ(settings)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Modelo de la aplicacion
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from burn_app import models

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RPC XML
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# STL Lib
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from stl			 import *
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Librerias Utiles
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
import time
import logging
import sys, time

from daemon import Daemon


def CreateSubtitleProcess(VideoFileName, SubtitleFileName, Brand):

    try:
	brand  = models.Brand.object.get(name=Brand)
    except:
	return False 

    SubProcess = models.SubProcess()
    SubProcess.brand     = brand
    SubProcess.file_name = VideoFileName
    SubProcess.subtitle  = SubTitleFileName
    SubProcess.status	 = 'N'
    SubProcess.save()
    

def Main():

    logging.basicConfig(format='%(asctime)s - BurnApiServer.py -[%(levelname)s]: %(message)s', filename='./log/BurnApiServer.log',level=logging.INFO)

    server = SimpleXMLRPCServer((ApiSettings.SERVER_HOST, int(Settings.SERVER_PORT)), allow_none=True)
    server.register_introspection_functions()
    server.register_function(CreateSubtitleProcess)
    server.serve_forever()


class main_daemon(Daemon):
    def run(self):
        try:
    	    Main()
	except KeyboardInterrupt:
	    sys.exit()	    

if __name__ == "__main__":
	daemon = main_daemon('./pid/BurnApiServer.pid', stdout='./log/BurnApiServer.log', stderr='./log/BurnApiServer.log')
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







