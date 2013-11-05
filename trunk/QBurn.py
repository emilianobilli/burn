#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Carbon Coder 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from carbonapi.CarbonSocketLayer import *
from carbonapi.CarbonUtils 	 import *
from carbonapi.CarbonJob 	 import *
from carbonapi.CarbonSched 	 import *
from carbonapi.XmlTitler 	 import *

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STL Lib
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from stl			 import *


def InitCarbonPool(rhozetlist=[]):
    CPool       = CarbonPool()

    for rhozet in rhozetlist:
	CPool.addCarbon(rhozet)

    if CPool.poolLen() == 0:
	return None
    
    return CPool

def MakeTranscodeInfo (TranscodeGuid, DstBasename, DstPath, TCin, XmlTitlerElement):
    #
    # Arma los parametros de transcodificacion
    #	
    TranscodeInfo = { 'd_guid'    : TranscodeGuid, 
                      'd_basename': DstBasename, 
                      'd_path'    : DstPath,
                      'subtitle'  : XmlTitlerElement }

    return TranscodeInfo
    

def BurnSubtitle(Source,File,TranscodeInfo,Cpool, ForceSchedule=False):

    XmlJob    = CreateCarbonXMLJob(Source,File,[],[TranscodeInfo],None,None)

    print XmlJob

    if XmlJob is None:
        ErrorString = '01: Error making Carbon XML Job'
        print ErrorString
        return False


    return StartJobCarbonPool(Cpool,XmlJob, ForceSchedule)

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

    for tti in stl.tti:
	TextAndTiming = Data()
        TextAndTiming.StartTimecode = str(tti.tci) 
        TextAndTiming.EndTimecode   = str(tti.tco)
        TextAndTiming.Title	    = tti.tf.encode_utf8()
        TextAndTiming.PosX	    = '0.50'
        TextAndTiming.PosY	    = '0.75'
        XmlTitler.AppendData(data)
	
    return XmlTitler.ToElement()
    

	
SRC_FILE = 'Atada-a-su-PiXXa_QT.mov'
SRC_PATH = '\\\\10.3.3.70\\VIDEO_PROC\\'
DST_GUID = '{95B787F1-DB73-4013-AE59-9D6E84F7D421}'

STL_FILE = '/home/emilianob/Atada a su PiXXa_Esp_Ok.stl'
DST_BASENAME = 'TEST_SUB'

Xml = StlToXmlTitler(STL_FILE)

print Xml

Cpool = InitCarbonPool(['10.3.3.66'])

TranscodeInfo = MakeTranscodeInfo(DST_GUID,DST_BASENAME,'\\\\10.3.3.70\\VIDEO_PROC\\', '01:00:00:00', Xml)
x = BurnSubtitle(SRC_PATH,SRC_FILE,TranscodeInfo,Cpool)

print x