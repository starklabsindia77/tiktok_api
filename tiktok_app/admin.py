from django.contrib import admin
from tiktok_app.models import *
class AudioAdmin(admin.ModelAdmin):
	list_display=("id","audiofile_name")
	


admin.site.register(UserDetails)
admin.site.register(VerificationOTP)
admin.site.register(AudioFile)
admin.site.register(VideoFile)
admin.site.register(VideoComment)
admin.site.register(VideoLike)
admin.site.register(VideoHeart)
admin.site.register(VideoShare)
admin.site.register(Hastag)
admin.site.register(FollowUser)
admin.site.register(language)
