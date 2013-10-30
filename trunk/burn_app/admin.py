from django.contrib import admin
from burn_app.models import *

class PathAdmin (admin.ModelAdmin):
    list_display = ('key', 'location')
    
class TranscodingServerAdmin (admin.ModelAdmin):
    list_display = ('name', 'ip_address','status')
    
class VideoProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'file_extension', 'status', 'sufix')

class SubtitleProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'font' )

class VideoSubRenditionAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'video_profile', 'subtitle_profile', 'transcoding_server')    
    
class SubProcessAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'status')

class BrandAdmin (admin.ModelAdmin):
    list_display = ('name', 'subtitle_profile')

admin.site.register(Path, PathAdmin)
admin.site.register(TranscodingServer, TranscodingServerAdmin)
admin.site.register(VideoProfile, VideoProfileAdmin)
admin.site.register(SubtitleProfile, SubtitleProfileAdmin)
admin.site.register(VideoSubRendition, VideoSubRenditionAdmin)    
admin.site.register(SubProcess, SubProcessAdmin)
admin.site.register(Brand, BrandAdmin)
