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
def CheckAssignedVideoSubRenditions(VSubRenditions = [])

    logging.info("CheckAssignedVideoSubRenditions(): Start Check Video Rendition Status")

    video_local_path = models.GetPath('renditions_local_path')
            
    #
    # Agrega / si no es que exite al final
    #
    if not video_local_path.endswith('/'):
	video_local_path = video_local_path + '/'

    for VRendition in VSubRenditions:
	
	logging.info("CheckAssignedVideoSubRenditions(): Video Rendition Check: " + VRendition.file_name)
	logging.info("CheckAssignedVideoSubRenditions(): Video Rendition Item: " + VRendition.item.name)

	logging.info("CheckAssignedVideoSubRenditions(): Transcoding Server: " + VRendition.transcoding_server.ip_address)
	logging.info("CheckAssignedVideoSubRenditions(): Job GUID: " + VRendition.transcoding_job_guid)
	
	
	JobState, Progress = GetJobState(VRendition.transcoding_server.ip_address, VRendition.transcoding_job_guid)
	logging.info("CheckAssignedVideoSubRenditions(): Job Progress: " + str(Progress))
	logging.info("CheckAssignedVideoSubRenditions(): Job State: " + JobState)
	
	if JobState == 'NEX_JOB_COMPLETED':

	    if FileExist(video_local_path, VRendition.file_name):
		    #
		    # Si el archivo existe
		    #
		    # - Calcula su checksum
		    # - Calcula su filesize
		    # - Establece su Status en F -> Finished
	    
		VRendition.status   = 'F'
		VRendition.progress = '100'
		VRendition.save()
		
		logging.info("CheckAssignedVideoSubRenditions(): Video Rendition finish all procesing: " + VRendition.file_name)
	    else:
		    #
		    # Si el archivo no existe es porque se produjo un error
		    #
		logging.error("CheckAssignedVideoSubRenditions(): Video Rendition not exist: [FILE]-> " + VRendition.file_name + ", [PATH]-> " + video_local_path)
		VRendition.status   = 'E'
		VRendition.error    = "Video Rendition not exist: [FILE]-> " + VRendition.file_name + ", [PATH]-> " + video_local_path
		VRendition.save()    
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



def AssignVideoSubRenditions(UVSubRenditions = [],CarbonPOOL,ForceSchedule=False):
    global ErrorString
    ErrorString = ''

    logging.info("AssignVideoSubRenditions():Start Checking Unassingned Video Renditions")

    if len(UVSubRenditions) > 0:
    
	dst_svc_path = models.GetPath('renditions_svc_path')	

	for VSubRendition in UVSubRenditions: 

	    XmlTitlerElement = StlToXmlTitler(VSubRendition.subtitle_profile, VSubRendition.sub_file_name) 

	    TranscodeInfo    = MakeTranscodeInfo(VSubRendition.video_profile.guid, 
					         SplitExtension(VSubRendition.file_name), 
					         dst_svc_path,
					         XmlTitlerElement)

	    logging.debug("AssignVideoSubRenditions(): Transcode Info: " +  str(TranscodeInfo))
	    #
	    # Crea el XML con el Job de Transcodificacion
	    #
	    try:
		XmlJob    = CreateCarbonXMLJob(VSubRendition.src_svc_path,VSubRendition.src_file_name,[],[TranscodeInfo],None,None)
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
		VSubRendition.status = 'Q'
		VSubRendition.transcoding_job_guid = JobReply.Job.GetGUID()

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
	    	        	    	
		VSubRendition.transcoding_server = TServer
		VSubRendition.save()
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


def Main():
    
    SubProcessList = models.SubProcess.objects.filter(status='N')
    for SubProcess in SubProcessList:
	CreateVideoSubRenditions(SubProcess)
	
    	
    


def CreateVideoSubRendition(SubProcess=None):
    
    if SubProcess is None:
	return False
	
    subtitle_path = models.GetPath('subtitle_local_path')
    svc_path	  = models.GetPath('master_svc_path')
    media_path    = models.GetPath('master_local_path')
    
    if FileExist(media_path,SubProcess.file_name):
        
	if FileExist(subtitle_path,SubProcess.subtitle):
	
	    DstFileName = SplitExtension(SubProcess.file_name) + 
		          VSRendition.SubProcess.brand.video_profile.sufix + 
			  VSRendition.SubProcess.brand.video_profile.file_extension				        
	
	    VSRendition = models.VideoSubRendition()
	    VSRendition.file_name 	     = DstFileName
	    VSRendition.video_profile        = SubProcess.brand.video_profile
	    VSRendition.subtitle_profile     = SubProcess.brand.subtitle_profile
	    VSRendition.transcoding_job_guid = ''    
	    VSRendition.status		     = 'U'
	    VSRendition.src_file_name        = SubProcess.file_name
	    VSRendition.src_svc_path	     = svc_path
	    VSRendition.sub_file_name	     = subtitle_path + SubProcess.subtitle
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
    TranscodeInfo = { 'd_guid'    : TranscodeGuid, 
                      'd_basename': DstBasename, 
                      'd_path'    : DstPath,
                      'subtitle'  : XmlTitlerElement.ToElement() }

    return TranscodeInfo

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
    Style.Transparency  = SubProfile.transparency
    Style.ShadowSize    = SubProfile.shadow_size
    Style.HardShadow    = SubProfile.hard_shadow
    Style.StartTimecode = '00:00:00;00'
    Style.EndTimecode   = '99:99:99;99'
    Style.Title		= ''
     
    XmlTitler.append(Style)

    # Por Cada TTI del Stl crea una estructura de tipo Data()
    for tti in stl.tti:
	TextAndTiming = Data()
        TextAndTiming.StartTimecode = str(tti.tci) 
        TextAndTiming.EndTimecode   = str(tti.tco)
        TextAndTiming.Title	    = tti.tf.encode_utf8()
        TextAndTiming.PosX	    = '0.50'
        TextAndTiming.PosY	    = '0.75'
        XmlTitler.AppendData(data)
	
    return XmlTitler



class main_daemon(Daemon):
    def run(self):
        try:
    	    main()
	except KeyboardInterrupt:
	    sys.exit()	    

if __name__ == "__main__":
	daemon = main_daemon('./pid/QBurn.pid', stdout='./log/QBurn.err', stderr='./log/QBurn.err')
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
