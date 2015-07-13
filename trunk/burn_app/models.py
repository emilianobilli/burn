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
	billing						=models.ForeignKey('Billing', blank=True, null=True)
	guid						=models.CharField(max_length=256)
	file_extension					=models.CharField(max_length=64)
	status						=models.CharField(max_length=1, choices = ACTIVE_STATUS)
	sufix						=models.CharField(max_length=32, blank=True)
	path						=models.ForeignKey('Path')
	priority					=models.IntegerField()
	def __unicode__(self):
		return self.name

class Path (models.Model):

	PATH_TYPE = ( 
	    ('O', 'Only Path'),
	    ('S', 'Smart Path'),
	)

	key						=models.CharField(max_length=24)
	location					=models.CharField(max_length=256)
	description					=models.CharField(max_length=256)
	path_type					=models.CharField(max_length=1, choices = PATH_TYPE, default='O')
	video_profile_name				=models.CharField(max_length=100, blank=True)
		
	def __unicode__(self):
		return self.key


class InternalCustomer (models.Model):
	name						=models.CharField(max_length=50)
	billing_account					=models.ManyToManyField('Billing')

	def __unicode__(self):
		return self.name
		

class Billing (models.Model):
	name						=models.CharField(max_length=50)
	description					=models.CharField(max_length=255)
	
	def __unicode__(self):
	    return str(self.id) + '-' + self.name	


class TranscodingServer (models.Model):

	name						=models.CharField(max_length=256)
	ip_address					=models.CharField(max_length=15)
	status						=models.CharField(max_length=1, choices = ACTIVE_STATUS)
	def __unicode__(self):
		return self.ip_address


	
class SubtitleProfile (models.Model):
	
	name						=models.CharField(max_length=256)
	font						=models.CharField(max_length=32)
	charsize					=models.CharField(max_length=10)
	posx						=models.CharField(max_length=5, blank=True,help_text='Values between 0.0 (left) and 1.0 (right)') 
	posy						=models.CharField(max_length=5, blank=True, help_text='Values between 0.0 (top) and 1.0 (bottom)')
	color_rgb					=models.CharField(max_length=20, help_text='Values between 0.0 - 255.0 (R,G,B)')
	transparency					=models.CharField(max_length=5, help_text='Values between 0.0 (opaque) and 1.0 (transparent')
	shadow_size					=models.CharField(max_length=5, help_text='Values between 0.0 (no glow) and 1.0 (strong glow)')
	hard_shadow					=models.CharField(max_length=1, blank=True, choices=(('0', 'Normal Shadow'), ('1', 'Shadow with border')), default='0')
	bkg_enable					=models.CharField(max_length=1, blank=True, choices=(('0', 'Normal'), ('1', 'Black Background behind text')), default='0')
	bkg_semitransparent				=models.CharField(max_length=1, blank=True, choices=(('0', 'Normal'), ('1', 'Background Semi Transparent')), default='0')
	bkg_extra_width					=models.CharField(max_length=5, blank=True, help_text ='How wider the background should be in relation to the text')
	bkg_extra_height				=models.CharField(max_length=5, blank=True, help_text ='How taller the background should be in relation to the text')
	right_to_left					=models.CharField(max_length=1, choices=(('0', 'Normal'), ('1', 'Right to Left order')), default='0')
	h_align						=models.CharField(max_length=1, choices=(('0', 'Center'), ('1', 'Left'), ('2', 'Right')), default='0')
	v_align						=models.CharField(max_length=1, choices=(('0', 'Centered around the first line'), ('1', 'Centered'), ('2', 'Top'), ('3', 'Bottom')), default='0')
	def __unicode__(self):
		return self.name

class VideoRendition(models.Model):
	VIDEO_RENDITION_STATUS = (
	    ('Q', 'Queued'),
	    ('F', 'Finished'),
	    ('U', 'Unasigned'),
	    ('E', 'Error'),
	)
	ACTION = (
	    ('B', 'Burn Subtitle'),
	    ('T', 'Simple Transcode'),
	    ('S', 'Stich Movies')
	)
	creation_date					=models.DateTimeField(auto_now_add=True, blank=True, null=True)

	action						=models.CharField(max_length=1, choices=ACTION)
	stich_process					=models.ForeignKey('StichProcess', blank=True, null=True)
	file_name					=models.CharField(max_length=256)
	video_profile					=models.ForeignKey('VideoProfile')
	subtitle_profile				=models.ForeignKey('SubtitleProfile', blank=True, null=True)
	transcoding_server				=models.ForeignKey('TranscodingServer', blank=True, null=True)
	transcoding_job_guid				=models.CharField(max_length=256, blank=True)
	status						=models.CharField(max_length=1, choices=VIDEO_RENDITION_STATUS)
	src_file_name					=models.CharField(max_length=256, blank=True)
	src_svc_path					=models.CharField(max_length=256)
	sub_file_name					=models.CharField(max_length=512, blank=True)
	error						=models.CharField(max_length=256, blank=True)
	speed						=models.CharField(max_length=25, blank=True)				
	progress					=models.CharField(max_length=10, blank=True)
	priority					=models.IntegerField()
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
		('N', 'New'),
		('E', 'Error'),
	)
	file_name					=models.CharField(max_length=256)
	subtitle					=models.CharField(max_length=256)
	brand 						=models.ForeignKey('Brand')
	status						=models.CharField(max_length=1, choices=SUBPROCESS_QUEUE_STATUS)
	dst_basename					=models.CharField(max_length=256)
	error						=models.CharField(max_length=256, blank=True)
	
	def __unicode__ (self):
		return self.file_name
	
class TranscodeProcess (models.Model):
	TRANSCODE_QUEUE_STATUS = (
		('D', 'Done'),
		('N', 'New'),
		('E', 'Error'),
	)
	MATERIAL_TYPE = (
		('F', 'Fork Master'),
		('L', 'Local Master'),
	)
	file_name					=models.CharField(max_length=256)
	material_type					=models.CharField(max_length=1, choices=MATERIAL_TYPE, default='P')
	status						=models.CharField(max_length=1, choices=TRANSCODE_QUEUE_STATUS)
	video_profile					=models.ForeignKey('VideoProfile')
	dst_basename					=models.CharField(max_length=255)
	error						=models.CharField(max_length=256, blank=True)
	
	def __unicode__ (self):
		return self.file_name


class StichProcess (models.Model):
	STICH_QUEUE_STATUS = (
	    ('W', 'Waiting'),
	    ('D', 'Done'),
	    ('E', 'Error'),
	)
	dst_basename					=models.CharField(max_length=255)
	status						=models.CharField(max_length=1, choices=STICH_QUEUE_STATUS)
	video_profile					=models.ForeignKey('VideoProfile')
	total_fragments					=models.CharField(max_length=3)
	error						=models.CharField(max_length=256, blank=True)
	
	def __unicode__ (self):
		return self.dst_basename

class StichFragment (models.Model):
	stich_process					=models.ForeignKey('StichProcess')
	file_name					=models.CharField(max_length=256)
	order						=models.CharField(max_length=3)
	
	def __unicode__(self):
		return '%s-%s' % (self.stich_process, self.file_name)
	
def GetPath(path=None):
    if path is not None:
	try:
	    return Path.objects.get(key=path).location
	except:
	    return None
    return None		

def GetTranscodingServer():
    return TranscodingServer.objects.filter(status='E')










	    
	    
	
	