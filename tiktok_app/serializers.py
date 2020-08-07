from rest_framework import serializers
from tiktok_app.models import *

class VideosSerialzers(serializers.ModelSerializer):

	class Meta:
		model = VideoFile
		fields = '__all__'

class AudioSerialzers(serializers.ModelSerializer):

	class Meta:
		model = AudioFile
		fields = '__all__'

class HastagSerialzers(serializers.ModelSerializer):

	class Meta:
		model = Hastag
		fields = '__all__'


class LanguageSerialzers(serializers.ModelSerializer):

	class Meta:
		model = language
		fields = '__all__'


