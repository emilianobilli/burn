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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Carbon Coder 										     #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
from carbonapi.CarbonSocketLayer import *
from carbonapi.CarbonUtils 	 import *
from carbonapi.CarbonJob 	 import *
from carbonapi.CarbonSched 	 import *
from carbonapi.XmlTitler 	 import *

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
import datetime

from daemon import Daemon



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Local Carbon Functions
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Retorna el Progreso y el Stado de un Job
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def GetJobState(transcoder_ip, job_guid):
    carbon = CarbonSocketLayer(transcoder_ip)
    Job = CarbonJob(carbon, job_guid)
    return Job.GetState(), str(Job.GetProgress())

def GetJobSpeed(transcoder_ip, job_guid):
    carbon = CarbonSocketLayer(transcoder_ip)
    Job = CarbonJob(carbon, job_guid)
    return Job.GetSpeed()
    
def GetJobError(transcoder_ip, job_guid):
    carbon = CarbonSocketLayer(transcoder_ip)
    Job = CarbonJob(carbon, job_guid)
    return Job.GetError()    


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# InitCarbonPool(): Inicializa el pool de Rhozets					     #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def InitCarbonPool(TServerList = []):

    # Se crea el pool de Carbon
    CPool       = CarbonPool()
    
    # La lista no este vacia
    if len(TServerList) == 0:
	return None

    for TServer in TServerList:
	ret = CPool.addCarbon(TServer.ip_address)
	if ret == False:
	    TServer.status = 'D'
	    TServer.save()
	    logging.warning("InitCarbonPool(): Carbon server [%s] fail to init -> Set Disable" % TServer.ip_address)
	else:
	    logging.info("InitCarbonPool(): Carbon server [%s] init OK" % TServer.ip_address)
    if CPool.poolLen() == 0:
	return None
    
    return CPool


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Comprueba la existencia de un archivo							     #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#	        
def FileExist(path, file):
    if os.path.isfile(path+file):
	return True

    return False


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


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# CheckAssignedVideoSubRenditions(): Chequea el status de los trabajos de Rhozdet	     #
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def CheckAssignedVideoRenditions(VRenditions = []):

    logging.info("CheckAssignedVideoSubRenditions(): Start Check Video Rendition Status")


    for VRendition in VRenditions:
	
	
	logging.info("CheckAssignedVideoSubRenditions(): Video Rendition Check: " + VRendition.file_name)

	logging.info("CheckAssignedVideoSubRenditions(): Transcoding Server: " + VRendition.transcoding_server.ip_address)
	logging.info("CheckAssignedVideoSubRenditions(): Job GUID: " + VRendition.transcoding_job_guid)
	
	
	JobState, Progress = GetJobState(VRendition.transcoding_server.ip_address, VRendition.transcoding_job_guid)
	logging.info("CheckAssignedVideoSubRenditions(): Job Progress: " + str(Progress))
	logging.info("CheckAssignedVideoSubRenditions(): Job State: " + JobState)

	if VRendition.creation_date is None:
	    VRendition.creation_date = datetime.datetime.now()
	    
	
	if JobState == 'NEX_JOB_COMPLETED':
    	    VRendition.status   = 'F'
	    VRendition.progress = '100'
	    VRendition.save()
		
	    logging.info("CheckAssignedVideoSubRenditions(): Video Rendition finish all procesing: " + VRendition.file_name)
	        
	else:
	    if JobState == 'NEX_JOB_STARTED':
		VRendition.speed = GetJobSpeed(VRendition.transcoding_server.ip_address, VRendition.transcoding_job_guid)
		VRendition.progress = str(Progress)
		VRendition.save()
		
    	    if JobState == 'NEX_JOB_ERROR':
    		#
		# Si el job termino con errores
    		#
    		VRendition.status = 'E'
		VRendition.error  = GetJobError(VRendition.transcoding_server.ip_address, VRendition.transcoding_job_guid)
    		logging.error("CheckAssignedVideoSubRenditions(): %s" % VRendition.error)
    		VRendition.save()
	    
	    if JobState == 'NEX_JOB_STOPPED':
    		#
		# Alguien Freno el Job
		# 
		VRendition.status = 'E'
		VRendition.error  = "Stop Job"
		logging.error("CheckAssignedVideoSubRenditions(): %s" % VRendition.error)
		VRendition.save()

	    if JobState == '':
		VRendition.status = 'E'
		VRendition.error  = "Job State Empty"
		logging.error("CheckAssignedVideoSubRenditions(): %s" % VRendition.error)
		VRendition.save()
		
    logging.info("CheckAssignedVideoSubRenditions(): End Check Video Rendition Status")
    return True



def AssignVideoRenditions(UVRenditions = [],CarbonPOOL = None,ForceSchedule=False):
    global ErrorString
    ErrorString = ''

    logging.info("AssignVideoSubRenditions():Start Checking Unassingned Video Renditions")

    if len(UVRenditions) > 0:


	for VRendition in UVRenditions: 

	    if VRendition.action == 'B':
		if VRendition.sub_file_name.endswith('.stl'):
		    XmlTitlerElement = StlToXmlTitler(VRendition.subtitle_profile, VRendition.sub_file_name) 
		else:
		    XmlTitlerElement = SubToXmlTitler(VRendition.subtitle_profile, VRendition.sub_file_name)
		Source = None
		Stich = False
	    elif VRendition.action == 'S':
		Fragments = models.StichFragment.objects.filter(stich_process=VRendition.stich_process).order_by('order')
		FileList = []	
		for fragment in Fragments:
		    FileList.append(VRendition.src_svc_path + fragment.file_name)
			
		Source = StichSource(FileList)	    
		XmlTitlerElement = None
		Stich = True
	    else:
		XmlTitlerElement = None
		Source = None
		Stich = False

	    dst_svc_path     = VRendition.video_profile.path.location

	    TranscodeInfo    = MakeTranscodeInfo(VRendition.video_profile.guid, 
					         SplitExtension(VRendition.file_name), 
					         dst_svc_path,
					         XmlTitlerElement)

	    logging.debug("AssignVideoSubRenditions(): Transcode Info: " +  str(TranscodeInfo))
	    #
	    # Crea el XML con el Job de Transcodificacion
	    #
	    try:
		XmlJob    = CreateCarbonXMLJob(VRendition.src_svc_path,VRendition.src_file_name,[],[TranscodeInfo],Source,None, Stich)
	    except:
		e = sys.exc_info()[0]
	        logging.error("AssignVideoSubRenditions(): 01: Exception making Carbon XML Job. Catch: " + e)
		ErrorString = '01: Exception making Carbon XML Job. Catch: ' + e 
		return False

	    if XmlJob is None:
		logging.error("AssignVideoSubRenditions(): 01: Error making Carbon XML Job")
	        ErrorString = '01: Error making Carbon XML Job'
	        return False

	    JobReply       = StartJobCarbonPool(CarbonPOOL,XmlJob, ForceSchedule)
	    if JobReply.Result == True:
		#
		# Si puedo Asignarle un Transcoding Server
		# 
		# 1- Lo Marca como Encolado
		# 2- Carga en Base de Datos el GUID del Job 
		# 3- Carga el Transcoding Server Asignado
		#
		VRendition.status = 'Q'
		VRendition.transcoding_job_guid = JobReply.Job.GetGUID()

		try:
		    TServer = models.TranscodingServer.objects.get(ip_address=JobReply.Job.GetCarbonHostname())
		    logging.info("AssignVideoSubRenditions(): Carbon Server ->" + TServer.ip_address)
		except:
		    #
		    # Si no encuentra el transcoding Server Asignado
		    #
		    ErrorString = '02: Can not find the Assigned Carbon Server'
		    logging.error("AssignVideoSubRenditions(): Can not find the Assigned Carbon Server -> " + JobReply.Job.GetCarbonHostname())
	    	    return False
	    	        	    	
		VRendition.transcoding_server = TServer
		VRendition.save()
	    else:
		if JobReply.Error == False:
		    logging.info("AssignVideoSubRenditions(): Can Not Assign Carbon Server ( No one have slots )")	
		    return True
		else:
		    ErrorString = '02: Error sending Job'
		    logging.error("AssignVideoSubRenditions(): 02: Error sending Job")
	    	    return False

    logging.info("AssignVideoSubRenditions(): End Checking Unassingned Video Renditions")
    return True


def CreateVideoStichRenditions(StichProcess=None):

    if StichProcess is None:
	return False
	
    svc_path   = models.GetPath('fork_master_svc_path')
    media_path = models.GetPath('fork_master_local_path')

    StichFragments = models.StichFragment.objects.filter(stich_process=StichProcess)
    
    #
    # Si la cantidad de fragmentos 
    #
    if len(StichFragments) == int(StichProcess.total_fragments):
	for fragment in StichFragments:
	    if not FileExist(media_path,fragment.file_name):
		StichProcess.error  = 'StichFragment (%s) -> Does Not exist filename: %s' % (fragment,fragment.file_name)
		StichProcess.status = 'E'
		StichProcess.save()
		return False
	
	VSRendition = models.VideoRendition()    
	VSRendition.file_name 	     	 = StichProcess.dst_basename
	VSRendition.video_profile    	 = StichProcess.video_profile
	VSRendition.stich_process	 = StichProcess
	VSRendition.transcoding_job_guid = ''    
	VSRendition.status		 = 'U'
	VSRendition.src_file_name        = ''
	VSRendition.src_svc_path	 = svc_path
	VSRendition.action		 = 'S'
	VSRendition.priority		 = StichProcess.video_profile.priority
	VSRendition.save()
	StichProcess.status		 = 'D'
	StichProcess.save()	
	
	
    else:
	return True
	
	
def CreateVideoTranscodeRenditions(TranscodeProcess=None):
    if TranscodeProcess is None:
	return False
	
    	
    if TranscodeProcess.material_type == 'F':	
	svc_path   = models.GetPath('fork_master_svc_path')
	media_path = models.GetPath('fork_master_local_path')
    else:
	svc_path   = models.GetPath('local_master_svc_path')
	media_path = models.GetPath('local_master_local_path')

    if FileExist(media_path,TranscodeProcess.file_name):
	VSRendition = models.VideoRendition()
	VSRendition.file_name 	     	 = TranscodeProcess.dst_basename
	VSRendition.video_profile    	 = TranscodeProcess.video_profile
	VSRendition.transcoding_job_guid = ''    
	VSRendition.status		 = 'U'
	VSRendition.src_file_name        = TranscodeProcess.file_name
	VSRendition.src_svc_path	 = svc_path
	VSRendition.action		 = 'T'
	VSRendition.priority		 = TranscodeProcess.video_profile.priority
	VSRendition.save()
	TranscodeProcess.status		 = 'D'
	TranscodeProcess.save()	
    else:
	TranscodeProcess.error  = 'Unable to locate master file [%s]' % media_path + TranscodeProcess.file_name
	TranscodeProcess.status = 'E'
	TranscodeProcess.save()
	return False
    
    return True

def CreateVideoSubRenditions(SubProcess=None):
    
    if SubProcess is None:
	return False
	
    subtitle_path = models.GetPath('subtitle_local_path')
    svc_path	  = models.GetPath('fork_master_svc_path')
    media_path    = models.GetPath('fork_master_local_path')
    
    if FileExist(media_path,SubProcess.file_name):
        
	if FileExist(subtitle_path,SubProcess.subtitle):
	
#	    DstFileName = SplitExtension(SubProcess.file_name) + SubProcess.brand.video_profile.sufix + SubProcess.brand.video_profile.file_extension				        
	
	    VSRendition = models.VideoRendition()
	    VSRendition.file_name 	     = SubProcess.dst_basename
	    VSRendition.video_profile        = SubProcess.brand.video_profile
	    VSRendition.subtitle_profile     = SubProcess.brand.subtitle_profile
	    VSRendition.transcoding_job_guid = ''    
	    VSRendition.status		     = 'U'
	    VSRendition.src_file_name        = SubProcess.file_name
	    VSRendition.src_svc_path	     = svc_path
	    VSRendition.sub_file_name	     = subtitle_path + SubProcess.subtitle
	    VSRendition.action		     = 'B'
	    VSRendition.priority	     = SubProcess.brand.video_profile.priority
	    VSRendition.save()
	    SubProcess.status = 'D'
	    SubProcess.save()
	else:
	    SubProcess.error  = 'Unable to locate subtitle [%s]' % subtitle_path + SubProcess.subtitle
	    SubProcess.status = 'E'
	    SubProcess.save()
	    return False
    
    else:
	SubProcess.error  = 'Unable to locate master file [%s]' % media_path + SubProcess.file_name
	SubProcess.status = 'E'
	SubProcess.save()
	return False
    
    return True	
	
	
def MakeTranscodeInfo (TranscodeGuid, DstBasename, DstPath, XmlTitlerElement):
    #
    # Arma los parametros de transcodificacion
    #	

    if XmlTitlerElement is not None:
	TranscodeInfo = { 'd_guid'    : TranscodeGuid, 
    	                  'd_basename': DstBasename, 
                          'd_path'    : DstPath,
                          'subtitle'  : XmlTitlerElement.ToElement() }
    else:
	TranscodeInfo = { 'd_guid'    : TranscodeGuid, 
    	                  'd_basename': DstBasename, 
                          'd_path'    : DstPath }
                         
                          
    return TranscodeInfo


def SubToXmlTitler(SubProfile, SubFileName):
    sub = SUB()
    sub.load(SubFileName)
    # Crea la estructura de datos XmlTitler
    XmlTitler = TitlerData()

    # Crea el estilo
    Style = Data()
    Style.Font     = SubProfile.font
    Style.CharSize = SubProfile.charsize

    # Carga los valores del estilo en el XML de acuerdo al SubtitleProfile
    R,G,B = SubProfile.color_rgb.split(',')
    Style.ColorR = R
    Style.ColorG = G
    Style.ColorB = B
#    Style.Transparency  = SubProfile.transparency
    Style.ShadowSize    = SubProfile.shadow_size
    Style.HardShadow    = SubProfile.hard_shadow
    Style.StartTimecode = '00:00:00;00'
    Style.EndTimecode   = '00:00:00;01'
    Style.Title		= ''
     
    XmlTitler.AppendData(Style)

    for timing in sub.timing:
	TextAndTiming = Data()
#	TextAndTiming.Font          = SubProfile.font
	TextAndTiming.FontCharSet   = 'ANSI'
        TextAndTiming.StartTimecode = str(timing.tci) 
        TextAndTiming.EndTimecode   = str(timing.tco)
        TextAndTiming.Title	    = timing.text
        TextAndTiming.PosX	    = '0.50'
        TextAndTiming.PosY	    = '0.835'
        XmlTitler.AppendData(TextAndTiming)
	
    return XmlTitler    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# StlToXmlTitler(): Convierte un STL a la estructura de Datos XmlTitler		    #
#										    #
# Argumentos: SubProfile  -> Subtitulo profile					    #
#	      StlFileName -> Nombre del archivo de Subtitulo (stl)		    #	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def StlToXmlTitler(SubProfile, StlFileName):

    # Abre el archivo STL
    stl = STL()
    stl.load(StlFileName)

    print StlFileName

    # Crea la estructura de datos XmlTitler
    XmlTitler = TitlerData()

    # Crea el estilo
    Style = Data()
    Style.Font     = SubProfile.font
    Style.CharSize = SubProfile.charsize


    # Carga los valores del estilo en el XML de acuerdo al SubtitleProfile
    R,G,B = SubProfile.color_rgb.split(',')
    Style.ColorR = R
    Style.ColorG = G
    Style.ColorB = B
#    Style.Transparency  = SubProfile.transparency
    Style.ShadowSize    = SubProfile.shadow_size
    Style.HardShadow    = SubProfile.hard_shadow
    Style.StartTimecode = '00:00:00;00'
    Style.EndTimecode   = '00:00:00;01'
    Style.Title		= ''
    XmlTitler.AppendData(Style)
    # Por Cada TTI del Stl crea una estructura de tipo Data()
    for tti in stl.tti:
	TextAndTiming = Data()
#	TextAndTiming.Font          = SubProfile.font
	TextAndTiming.FontCharSet   = 'ANSI'
        print tti.sn
        TextAndTiming.StartTimecode = str(tti.tci) 
        TextAndTiming.EndTimecode   = str(tti.tco)
        TextAndTiming.Title	    = tti.tf.encode_utf8()
        TextAndTiming.PosX	    = '0.50'
        TextAndTiming.PosY	    = '0.835'
        XmlTitler.AppendData(TextAndTiming)
	
    return XmlTitler

def Main():
    
    while True:
	SubProcessList = models.SubProcess.objects.filter(status='N')
	for SubProcess in SubProcessList:
	    CreateVideoSubRenditions(SubProcess)


	TranscodeProcessList = models.TranscodeProcess.objects.filter(status='N')
	for TranscodeProcess in TranscodeProcessList:
	    CreateVideoTranscodeRenditions(TranscodeProcess)    


	StichProcessList = models.StichProcess.objects.filter(status='W')
	for StichProcess in StichProcessList:
	    CreateVideoStichRenditions(StichProcess)


	Flag = False
	while not Flag:
    	    TServerList     = models.TranscodingServer.objects.filter(status='E')
	    CarbonPOOL      = InitCarbonPool(TServerList)
	    if CarbonPOOL is None:
		time.sleep(10)
	    else:
		Flag = True

	UnassignedList  = models.VideoRendition.objects.filter(status='U').order_by('priority')
	AssignVideoRenditions(UnassignedList, CarbonPOOL)
    
    
	AssignedList    = models.VideoRendition.objects.filter(status='Q')
	CheckAssignedVideoRenditions(AssignedList)

	time.sleep(100)

class main_daemon(Daemon):
    def run(self):
        try:
    	    Main()
	except KeyboardInterrupt:
	    sys.exit()	    

if __name__ == "__main__":
	daemon = main_daemon('/opt/packager/app/burn/pid/QBurn.pid', stdout='/opt/packager/app/burn/log/QBurn.err', stderr='/opt/packager/app/burn/log/QBurn.err')
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

		elif 'zabbix'  == sys.argv[1]:
			daemon.zabbix()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|run" % sys.argv[0]
		sys.exit(2)

