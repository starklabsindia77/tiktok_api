from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
	user         = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=20,null=True)
	image        = models.ImageField(null=True, blank=True, upload_to='image/')
	bio          = models.CharField(max_length=200, default="bio")
	youtube      = models.CharField(max_length=200, default="youtube")
	instagram    = models.CharField(max_length=200, default="instagram")

	class Meta:
		unique_together = ("phone_number",)
	
	def __str__(self):
		return "%s" %(self.user)

class VerificationOTP(models.Model):
	phone_number   = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
	otp            = models.IntegerField(null=True) 

	class Meta:
		unique_together = ('phone_number',)

	def __str__(self):
		return "%s"%(self.phone_number)

class AudioFile(models.Model):
	user           = models.ForeignKey(User, on_delete=models.CASCADE)
	audiofile_name = models.CharField(max_length=500, null=True)
	audio_file     = models.FileField(blank=True, null=True, upload_to='audio/')
	status         = models.BooleanField(default=True)
	created_at     = models.DateTimeField(auto_now_add=True, blank=True)
	audio_time     = models.CharField(max_length=500, null=True,blank=True)


	def __str__(self):
		return "%s" %(self.audiofile_name)

class VideoFile(models.Model):
	audiofile       	=  models.ForeignKey(AudioFile, on_delete=models.CASCADE)
	user            	=  models.ForeignKey(User, on_delete=models.CASCADE)
	videofile_name      =  models.CharField(max_length=500, null=True)
	video_file          =  models.CharField(max_length=500, null=True)
	video_discription   =  models.CharField( max_length=1000,null=True,blank=True)
	status              =  models.BooleanField(default=True)
	created_at          =  models.DateTimeField(auto_now_add=True, blank=True)


	def __str__(self):
		return "%s" %(self.videofile_name)

class VideoComment(models.Model):
	videofile      = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
	user           = models.ForeignKey(User, on_delete=models.CASCADE)
	comment        = models.CharField(max_length=500, null=True)
	comment_status = models.BooleanField(default=True)
	created_at     = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.videofile)

class VideoLike(models.Model):
	videofile      = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
	user           = models.ForeignKey(User, on_delete=models.CASCADE)
	liked_status   = models.BooleanField(default=True)
	created_at     = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.videofile)

class VideoHeart(models.Model):
	videofile     = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
	user          = models.ForeignKey(User, on_delete=models.CASCADE)
	heart_status  = models.BooleanField(default=True)
	created_at    = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.videofile)

class VideoShare(models.Model):
	videofile    = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
	user         = models.ForeignKey(User, on_delete=models.CASCADE)
	share_status = models.BooleanField(default=True)
	created_at   = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.videofile)

class FollowUser(models.Model):
	follower      = models.ForeignKey(User, null=True, related_name='follower',on_delete=models.CASCADE)
	following     = models.ForeignKey(User, null=True, related_name='following',on_delete=models.CASCADE)
	follow_count  = models.IntegerField(blank=True,null=True)
	created_at    = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.follower.username

	def get_follower(self):
		return self.following.username

	def get_following(self):
		return self.follower.username

	class Meta:
		unique_together = ('follower', 'following')

class AudioFileTest(models.Model):
	audio_file = models.FileField(blank=True, null=True, upload_to='audio/')
	created_at = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.audio_file)


class Hastag(models.Model):
	user       = models.ForeignKey(User, on_delete=models.CASCADE)
	name       = models.CharField(max_length=500, null=True)
	count      = models.CharField(max_length=500, null=True)
	status     = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.name)


class language(models.Model):
	name       = models.CharField(max_length=500, null=True)
	image      = models.ImageField(null=True, blank=True, upload_to='image/')
	status     = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return "%s" %(self.name)







