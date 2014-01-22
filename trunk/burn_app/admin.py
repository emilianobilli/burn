from django.contrib import admin
from burn_app.models import *

class PathAdmin (admin.ModelAdmin):
    list_display = ('key', 'location')
    
class TranscodingServerAdmin (admin.ModelAdmin):
    list_display = ('name', 'ip_address','status')
    
class VideoProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'priority', 'file_extension', 'status', 'sufix')

class SubtitleProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'font' )

class VideoRenditionAdmin (admin.ModelAdmin):
    list_display = ('action', 'priority','file_name', 'video_profile', 'status', 'progress', 'speed',  'transcoding_server', 'subtitle_profile')    
    
class SubProcessAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'status')

class BrandAdmin (admin.ModelAdmin):
    list_display = ('name', 'subtitle_profile')

class TranscodeProcessAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'status', 'video_profile')    



admin.site.register(Path, PathAdmin)
admin.site.register(TranscodeProcess, TranscodeProcessAdmin)
admin.site.register(TranscodingServer, TranscodingServerAdmin)
admin.site.register(VideoProfile, VideoProfileAdmin)
admin.site.register(SubtitleProfile, SubtitleProfileAdmin)
admin.site.register(VideoRendition, VideoRenditionAdmin)    
admin.site.register(SubProcess, SubProcessAdmin)
admin.site.register(Brand, BrandAdmin)
