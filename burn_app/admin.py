from django.contrib import admin
from burn_app.models import *

class InternalCustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BillingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class PathAdmin (admin.ModelAdmin):
    list_display = ('key', 'location', 'path_type', 'video_profile_name')
    
class TranscodingServerAdmin (admin.ModelAdmin):
    list_display = ('name', 'ip_address','status')
    
class VideoProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'billing', 'priority', 'path','file_extension', 'status', 'sufix')

class SubtitleProfileAdmin (admin.ModelAdmin):
    list_display = ('name', 'font' )

class VideoRenditionAdmin (admin.ModelAdmin):
    list_display = ('id','creation_date','action', 'priority','file_name', 'video_profile', 'status', 'progress', 'speed',  'transcoding_server', 'subtitle_profile')    
    
class SubProcessAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'brand','status')

class BrandAdmin (admin.ModelAdmin):
    list_display = ('name', 'subtitle_profile', 'video_profile')

class TranscodeProcessAdmin (admin.ModelAdmin):
    list_display = ('file_name', 'status', 'material_type','video_profile')    

class StichProcessAdmin(admin.ModelAdmin):
    list_display = ('dst_basename', 'status')

class StichFragmentAdmin(admin.ModelAdmin):
    list_display = ('stich_process','file_name','order')


admin.site.register(Path, PathAdmin)
admin.site.register(TranscodeProcess, TranscodeProcessAdmin)
admin.site.register(TranscodingServer, TranscodingServerAdmin)
admin.site.register(VideoProfile, VideoProfileAdmin)
admin.site.register(SubtitleProfile, SubtitleProfileAdmin)
admin.site.register(VideoRendition, VideoRenditionAdmin)    
admin.site.register(SubProcess, SubProcessAdmin)
admin.site.register(StichProcess, StichProcessAdmin)
admin.site.register(StichFragment, StichFragmentAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Billing,BillingAdmin)
admin.site.register(InternalCustomer,InternalCustomerAdmin)
