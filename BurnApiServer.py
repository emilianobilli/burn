#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Stand alone script
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from django.core.management import setup_environ
from burn import settings
setup_environ(settings)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Modelo de la aplicacion
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from burn_app import models

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# RPC XML
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Librerias Utiles
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
import time
import logging
import sys, time
import Settings

from daemon import Daemon

def CreateSubtitleProcess(VideoFileName, SubtitleFileName, Brand, DstBaseName=''):

    brand  = models.Brand.objects.get(name=Brand)

    SubProcess = models.SubProcess()
    SubProcess.brand     = brand
    SubProcess.file_name = VideoFileName
    SubProcess.subtitle  = SubtitleFileName
    SubProcess.dst_basename = DstBaseName
    SubProcess.status	 = 'N'
    SubProcess.save()
    
    
def CreateTranscodeProcess(VideoFileName, VideoProfileName, DstBaseName=''):

    print VideoProfileName

    video_profile = models.VideoProfile.objects.get(name=VideoProfileName)
    
    TranscodeProcess = models.TranscodeProcess()
    TranscodeProcess.file_name     = VideoFileName
    TranscodeProcess.video_profile = video_profile
    TranscodeProcess.dst_basename = DstBaseName
    TranscodeProcess.status        = 'N'    
    TranscodeProcess.save()
    
    

def Main():

    logging.basicConfig(format='%(asctime)s - BurnApiServer.py -[%(levelname)s]: %(message)s', filename='./log/BurnApiServer.log',level=logging.INFO)
    server = SimpleXMLRPCServer((Settings.API_IPADDRESS, int(Settings.API_PORT)), allow_none=True)
    server.register_introspection_functions()
    server.register_function(CreateSubtitleProcess)
    server.register_function(CreateTranscodeProcess)
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







