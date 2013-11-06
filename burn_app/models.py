from django.db import models
from datetime import *
# importar User y Datetime.

ACTIVE_STATUS = (
	('E', 'Enabled'),
	('D', 'Disabled'),
)

FORMAT = (
	('SD', 'SD'),
	('HD', 'HD'),
	('', 'Empty'),
)

#TEST

class VideoProfile (models.Model):
	
	name						=models.CharField(unique=True, max_length=32)
	guid						=models.CharField(max_length=256)
	file_extension					=models.CharField(max_length=64)
	status						=models.CharField(max_length=1, choices = ACTIVE_STATUS)
	sufix						=models.CharField(max_length=32)
	def __unicode__(self):
		return self.name

class Path (models.Model):

	key						=models.CharField(max_length=24)
	location					=models.CharField(max_length=256)
	description					=models.CharField(max_length=256)
	def __unicode__(self):
		return self.key

class TranscodingServer (models.Model):

	name						=models.CharField(max_length=256)
	ip_address					=models.CharField(max_length=15)
	status						=models.CharField(max_length=1, choices = ACTIVE_STATUS)
	def __unicode__(self):
		return self.ip_adress


	
class SubtitleProfile (models.Model):
	
	name						=models.CharField(max_length=256)
	font						=models.CharField(max_length=32)
	charsize					=models.CharField(max_length=2)
	posx						=models.CharField(max_length=5, help_text='Values between 0.0 (left) and 1.0 (right)') 
	posy						=models.CharField(max_length=5, help_text='Values between 0.0 (top) and 1.0 (bottom)')
	color_rgb					=models.CharField(max_length=11, help_text='Values between 0.0 - 255.0 (R,G,B)')
	transparency					=models.CharField(max_length=5, help_text='Values between 0.0 (opaque) and 1.0 (transparent')
	shadow_size					=models.CharField(max_length=5, help_text='Values between 0.0 (no glow) and 1.0 (strong glow)')
	hard_shadow					=models.CharField(max_length=1, choices=(('0', 'Normal Shadow'), ('1', 'Shadow with border')), default='0')
	bkg_enable					=models.CharField(max_length=1, choices=(('0', 'Normal'), ('1', 'Black Background behind text')), default='0')
	bkg_semitransparent				=models.CharField(max_length=1, choices=(('0', 'Normal'), ('1', 'Background Semi Transparent')), default='0')
	bkg_extra_width					=models.CharField(max_length=5, help_text ='How wider the background should be in relation to the text')
	bkg_extra_height				=models.CharField(max_length=5, help_text ='How taller the background should be in relation to the text')
	right_to_left					=models.CharField(max_length=1, choices=(('0', 'Normal'), ('1', 'Right to Left order')), default='0')
	h_align						=models.CharField(max_length=1, choices=(('0', 'Center'), ('1', 'Left'), ('2', 'Right')), default='0')
	v_align						=models.CharField(max_length=1, choices=(('0', 'Centered around the first line'), ('1', 'Centered'), ('2', 'Top'), ('3', 'Bottom')), default='0')
	def __unicode__(self):
		return self.name

class VideoSubRendition(models.Model):
	VIDEO_RENDITION_STATUS = (
	    ('Q', 'Queued'),
	    ('F', 'Finished'),
	    ('U', 'Unasigned'),
	    ('E', 'Error'),
	)
	file_name					=models.CharField(max_length=256)
	video_profile					=models.ForeignKey('VideoProfile')
	subtitle_profile				=models.ForeignKey('SubtitleProfile')
	transcoding_server				=models.ForeignKey('TranscodingServer', blank=True, null=True)
	transcoding_job_guid				=models.CharField(max_length=256, blank=True)
	status						=models.CharField(max_length=1, choices=VIDEO_RENDITION_STATUS)
	src_file_name					=models.CharField(max_length=256)
	src_svc_path					=models.CharField(max_length=256)
	sub_file_name					=models.CharField(max_length=512)
	error						=models.CharField(max_length=256, blank=True)
	speed						=models.CharField(max_length=25, blank=True)				
	progress					=models.CharField(max_length=10, blank=True)

	def __unicode__ (self):
		return self.file_name

class Brand (models.Model):

	name						=models.CharField(max_length=256)
	subtitle_profile				=models.ForeignKey('SubtitleProfile')
	video_profile					=models.ForeignKey('VideoProfile')	
	def __unicode__ (self):
		return self.name


class SubProcess (models.Model):
	SUBPROCESS_QUEUE_STATUS = (
		('D', 'Done'),
		('W', 'Waiting'),
		('N', 'New'),
		('E', 'Error'),
	)
	file_name					=models.CharField(max_length=256)
	subtitle					=models.CharField(max_length=256)
	brand 						=models.ForeignKey('Brand')
	status						=models.CharField(max_length=1, choices=SUBPROCESS_QUEUE_STATUS)
	error						=models.CharField(max_length=256, blank=True)
	
	def __unicode__ (self):
		return self.file_name
		
def GetPath(path=None):
    if path is not None:
	try:
	    return Path.objects.get(key=path).location
	except:
	    return None
    return None		

def GetTranscodingServer():
    return TranscodingServer.objects.filter(status='E')




























	    
	    
	
	