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


import time
import logging
import sys, time, os
import shutil
from daemon import Daemon


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Elimina las extensiones (Considera que puede haber puntos en el medio del archivo)	     #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def SplitExtension(filename=None):
    
    if filename is not None:
	basename_tmp_list = filename.split('.')
	i = 1
	basename = basename_tmp_list[0]
	while i < len(basename_tmp_list) -1:
	    basename = basename + '.' + basename_tmp_list[i]
	    i = i + 1
	return basename
    return None



def Main():


    while True:

	dst_process_path = models.GetPath('local_master_local_path')
        #
        # Trae todos los Smart Path
        #
        SmartPathList = models.Path.objects.filter(path_type='S')
        for SmartPath in SmartPathList:
	    FilesListed = os.listdir(SmartPath.location)

	    for File in FilesListed:
		
		TProcess = models.TranscodeProcess()

		if os.path.isfile(dst_process_path + '/' + File):
		    os.unlink(dst_process_path + '/' + File)    
		    
		shutil.move(SmartPath.location + '/' + File, dst_process_path)
		    	    
	        TProcess.file_name     = File
	        TProcess.material_type = 'L'
		try:    
	    	    TProcess.video_profile = models.VideoProfile.objects.get(name=SmartPath.video_profile_name)
	    	    TProcess.dst_basename  = SplitExtension(File)
	    	    TProcess.status	       = 'N'
	    	    TProcess.error         = ''
	    	except:
	    	    TProcess.dst_basename  = ''
	    	    TProcess.status        = 'E'
	    	    TProcess.error	   = 'Unable to find the video profile: %s' % SmartPath.video_profile_name
	        TProcess.save()
    
	time.sleep(300)


class main_daemon(Daemon):
    def run(self):
        try:
    	    Main()
	except KeyboardInterrupt:
	    sys.exit()	    

if __name__ == "__main__":
	daemon = main_daemon('./pid/BurnWathSmartPath.pid', stdout='./log/BurnWathSmartPath.err', stderr='./log/BurnWathSmartPath.err')
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