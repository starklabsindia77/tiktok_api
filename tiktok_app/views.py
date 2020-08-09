from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import requests
import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from django.db.models import Q
from tiktok_app.send_otp import *
from tiktok_app.models import *
from tiktok_app.serializers import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
from subprocess import run
import subprocess
from ffmpy3 import FFmpeg
import ffmpy3
import os
import re
from tiktok_app.models import language, VideoFile, Hastag


def generate_otp():
	"""Generating 4 digits OTP automatically"""
	otp = str(uuid.uuid4().fields[-1])[:6]
	return otp

def generate_username():
	random_num = str(uuid.uuid4().fields[-1])[:4]
	return 'user'+random_num

class Login(APIView):
	def post(self, request, format="json"):
		phone_number = request.data.get('phone_number')
		size = len(phone_number)
		if size == 10:
			try:
				obj = UserDetails.objects.filter(phone_number=phone_number)
				if not obj:
					user_profile = User.objects.create_user(username=generate_username())
					user_details = UserDetails.objects.create(user=user_profile,phone_number=phone_number)
					generated_otp = generate_otp()
					VerificationOTP.objects.create(phone_number=user_details,otp=generated_otp)
					sending_otp(generated_otp,phone_number)
					return Response({'status':True,
										'otp': generated_otp,
										'phone_number': phone_number,
										'message':"Profile created Successful"},status=status.HTTP_201_CREATED)
				else:
					generated_otp = generate_otp()
					profile_obj = UserDetails.objects.get(phone_number=phone_number)
					already_exist = VerificationOTP.objects.filter(phone_number= profile_obj)
					if not already_exist:
						VerificationOTP.objects.create(phone_number=profile_obj, otp= generated_otp)
						sending_otp(generated_otp,phone_number)
						return Response({'status':True,
										'otp': generated_otp,
										'phone_number': phone_number,
										'message':"OTP Send Successful"},status=status.HTTP_200_OK)
					else:
						otp_obj = VerificationOTP.objects.get(phone_number=profile_obj)
						sending_otp(otp_obj.otp,phone_number)

						return Response({'status':True,
										'otp': otp_obj.otp,
										'phone_number': phone_number,
										'message':"OTP Send Successful"},status=status.HTTP_200_OK)
			except Exception as e:
				print(e)
				return Response({"user_status":False,
									"message":"given details does not exist"},status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				'status': False,
				'message': "Phone number is not correct"
			},status=status.HTTP_400_BAD_REQUEST)


class ResendOTP(APIView):
	def post(self, request, format="json"):
		phone_number = request.data.get('phone_number')
		size = len(phone_number)
		if size == 10:
			try:
				obj = UserDetails.objects.filter(phone_number=phone_number)
				if not obj:
					user_profile = User.objects.create_user(username=generate_username())
					user_details = UserDetails.objects.create(user=user_profile,phone_number=phone_number)
					generated_otp = generate_otp()
					VerificationOTP.objects.create(phone_number=user_details,otp=generated_otp)
					sending_otp(generated_otp,phone_number)
					return Response({'status':True,
										'otp': generated_otp,
										'phone_number': phone_number,
										'message':"Profile created Successful"},status=status.HTTP_201_CREATED)
				else:
					generated_otp = generate_otp()
					profile_obj = UserDetails.objects.get(phone_number=phone_number)
					already_exist = VerificationOTP.objects.filter(phone_number= profile_obj)
					if not already_exist:
						VerificationOTP.objects.create(phone_number=profile_obj, otp= generated_otp)
						sending_otp(generated_otp,phone_number)
						return Response({'status':True,
										'otp': generated_otp,
										'phone_number': phone_number,
										'message':"OTP Send Successful"},status=status.HTTP_200_OK)
					else:
						otp_obj = VerificationOTP.objects.get(phone_number=profile_obj)
						sending_otp(otp_obj.otp,phone_number)

						return Response({'status':True,
										'otp': otp_obj.otp,
										'phone_number': phone_number,
										'message':"OTP Send Successful"},status=status.HTTP_200_OK)
			except Exception as e:
				print(e)
				return Response({"user_status":False,
									"message":"given details does not exist"},status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				'status': False,
				'message': "Phone number is not correct"
			},status=status.HTTP_400_BAD_REQUEST)

class LoginOtpVerification(APIView):

	def post(self, request, format="json"):
		phone_number = request.data.get('phone_number')
		OTP = request.data.get('otp')
		size = len(phone_number)
		if size == 10:
			try:
				profile_obj = UserDetails.objects.get(phone_number=phone_number)
				otp_obj = VerificationOTP.objects.get(phone_number=profile_obj)
				if otp_obj.otp == int(OTP):
					otp_obj.delete()
					user = authenticate(request, username=phone_number)
					if user:
						login(request,user)
						if user.is_superuser:
							return Response({'status':True,
											'is_admin': True,
											'username': user.username,
											"user_id":user.id},status=status.HTTP_200_OK)
						else:
							return Response({
											"status":True,
											"user_status":profile_obj.user.is_authenticated, 
											"user_id": profile_obj.user.id,
											"username": profile_obj.user.username,
											"phone_number":phone_number,
											"message": "Login Successful"
											},status=status.HTTP_200_OK)
					else:
						pass
				else:
					return Response({'status':False,
									'msg':"Incorrect OTP",
									"phn_num":profile_obj.phone_number
									},status=status.HTTP_200_OK)
			except Exception as e:
				return Response({'status':False,
									'msg':"otp does not exist"},status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
				'status': False,
				'message': "Phone number is not correct"
			},status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
	def get(self,request,format="json"):
		"""
			Destroys user's logged in session
		"""
		logout(request)
		return Response({"message": "Successful Logout"},status=status.HTTP_200_OK)

class User_Details(APIView):
	def get(self, request, format="json"):
		try:
			user_id = request.GET.get('user_id')
			if user_id:
				user = User.objects.get(id=user_id)
				user_details = UserDetails.objects.get(user__id=user_id)
			else:
				user = User.objects.get(id=request.user.id)
				user_details = UserDetails.objects.get(user__id=request.user.id)
			return Response({
							"user_status":user.is_authenticated, 
							"user_id": user.id,
							"username": user.username,
							"phone_number": user_details.phone_number,
							"image": user_details.image.url if user_details.image else None,
							"Following_count":FollowUser.objects.filter(following=user.id).count(),
							"Followers_count":FollowUser.objects.filter(follower=user.id).count(),
							"bio":user_details.bio,
							"youtube":user_details.youtube,
							"instagram":user_details.instagram,
						},status=status.HTTP_200_OK)
		except Exception as e:
			return Response({
						"message": "please login your account"
						},status=status.HTTP_400_BAD_REQUEST)

	def put(self, request):
		image = request.data.get('image')
		username = request.data.get('username')
		bio = request.data.get('bio')
		youtube = request.data.get('youtube')
		instagram = request.data.get('instagram')
		if username:
			user = User.objects.get(id=request.user.id)
			user.username = username
			user.save()

		if username and image != '' and bio and youtube and instagram:
			user = User.objects.get(id=request.user.id)
			user.username = username
			user_details.image = image
			user_details.bio = bio
			user_details.instagram = instagram
			user_details.youtube = youtube
			user.save()
		
		if username and image != '':
			user = User.objects.get(id=request.user.id)
			user.username = username
			user_details.image = image
			user.save()
		
		if username and image == '' and bio and youtube and instagram:
			user = User.objects.get(id=request.user.id)
			user.username = username
			user_details.bio = bio
			user_details.instagram = instagram
			user_details.youtube = youtube
			user.save()

		if image == '' and bio:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.bio = bio
			user_details.save()
		
		if image == '' and bio and youtube:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.bio = bio
			user_details.youtube = youtube
			user_details.save()
		
		if image == '' and youtube:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.youtube = youtube
			user_details.save()
		
		if image == '' and bio and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.bio = bio
			user_details.instagram = instagram
			user_details.save()
		
		if image == '' and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.instagram = instagram
			user_details.save()

		if image == '' and bio and youtube and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.bio = bio
			user_details.youtube = youtube
			user_details.instagram = instagram
			user_details.save()
		
		if image == '' and youtube and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.youtube = youtube
			user_details.instagram = instagram
			user_details.save()

		if image != '':
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.image = image
			user_details.save()

		if image != '' and bio:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.image = image
			user_details.bio = bio
			user_details.save()

		if image != '' and youtube:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.image = image
			user_details.youtube = youtube
			user_details.save()

		if image != '' and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.image = image
			user_details.instagram = instagram
			user_details.save()

		if image != '' and bio and youtube and instagram:
			user_details = UserDetails.objects.get(user__id=request.user.id)
			user_details.image = image
			user_details.bio = bio
			user_details.instagram = instagram
			user_details.youtube = youtube
			user_details.save()

		return Response({"message": "data has updated Successful"},status=status.HTTP_200_OK)

class AudioViews(APIView):

	def post(self, request, format='json'):
		if not request.POST._mutable:
			request.POST._mutable = True

		data = request.data
		data['status'] = True
		data['user'] = request.user.id
		serializer = AudioSerialzers(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, format='json'):
		pk = request.GET.get('id')
		if pk:
			queryset = AudioFile.objects.filter(id=pk)
		else:
			queryset = AudioFile.objects.all()
		response = {}
		for data in queryset:
			response[data.id] = {
								"id": data.id,
								"user_id":data.user.id,
								"username":data.user.username,
								"audiofile_name":data.audiofile_name,
								"audio_file":data.audio_file.url if data.audio_file else None,
								"audio_time":data.audio_time,
								"status":data.status,
								"created_at":data.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
							}
		return Response(response.values(), status=status.HTTP_200_OK)	

	def put(self, request):
		if not request.POST._mutable:
			request.POST._mutable = True
		pk =  request.GET.get('id')
		queryset = AudioFile.objects.get(id=pk)
		data = request.data 
		try:
			if data['audio_file'] == '':
				del data['audio_file']
				serializer = AudioSerialzers(queryset, data=data, partial=True)
			else:
				serializer = AudioSerialzers(queryset, data=data, partial=True)
		except:
			serializer = AudioSerialzers(queryset, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request):
		queryset = get_object_or_404(AudioFile, id=request.GET.get('id'))
		queryset.delete()
		return Response({"Message":"audio file data hasbeen deleted successful"}, status=status.HTTP_204_NO_CONTENT)

class AudioSearch(APIView):
	def get(self, request, format="json"):
		response = {}
		text = request.GET.get('text')
		text_split = text.split(' ')

		queryset = AudioFile.objects.filter(Q(audiofile_name__icontains=text)|Q(audio_file__icontains=text))
		if len(queryset) == 0:
			for words in text_split:
				queryset = Athletes.objects.filter(Q(audiofile_name__icontains=words)|Q(audio_file__icontains=words))
		
		for data in queryset:
			response[data.id] = {	
								"id": data.id,
								"user_id":data.user.id,
								"username":data.user.username,
								"audiofile_name":data.audiofile_name,
								"audio_file":data.audio_file.url if data.audio_file else None,
								"status":data.status,
								"created_at":data.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
								}	

		return Response(response.values(), status=status.HTTP_200_OK)

class VideoViews(APIView):

	def post(self, request, format='json'):
		if not request.POST._mutable:
			request.POST._mutable = True
		data = request.data		
		data['status'] = True
		data['user'] = request.user.id
		file = request.FILES['video_file']
		fs = FileSystemStorage(location='static/media/temp/') #defaults to   MEDIA_ROOT
		filename = fs.save(file.name,file )
		compress_file = compression()
		print(compress_file)
		com = compress_file.split("static")
		print(com[0])
		print(com[1])
		data['video_file'] = com[1]	
		serializer = VideosSerialzers(data = data)
		discription=data["video_discription"]
		list_discription=discription.split(" ")
		extract_list=[]
		for list_item in list_discription:
			start_with_hash=re.search("^#",list_item)
			if start_with_hash:
				extract_list.append(list_item)
			else:
				pass
		for item in extract_list:
			if Hastag.objects.filter(name__iexact=item).exists():
				obj,created=Hastag.objects.get_or_create(count=1,user=request.user,name=item)
			else:
				obj,created=Hastag.objects.get_or_create(name=item,user=request.user)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, format='json'):
		pk = request.GET.get('id')
		user_id = request.GET.get('user_id')
		if pk:
			queryset = VideoFile.objects.filter(id=pk)
		elif user_id:
			queryset = VideoFile.objects.filter(user__id=user_id)
		else:
			queryset = VideoFile.objects.all()
		response = {}
		for data in queryset:
			response[data.id] = {
								"id": data.id,
								"user_id":data.user.id,
								"username":data.user.username,
								"audiofile_name":data.audiofile.audiofile_name,
								"audio_file":data.audiofile.audio_file.url if data.audiofile.audio_file else None,
								"videofile_name":data.videofile_name,
								"video_discription":data.video_discription,
								"video_file":data.video_file,
								"status":data.status,
								"created_at":data.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
								"likes_count": len(VideoLike.objects.filter(videofile__id=data.id)),
								"heart_count": len(VideoHeart.objects.filter(videofile__id=data.id)),
								"comments_count": len(VideoComment.objects.filter(videofile__id=data.id)),
								"share_count": len(VideoShare.objects.filter(videofile__id=data.id)),
							}
			likes_qs = VideoLike.objects.filter(videofile__id=data.id)
			if likes_qs:
				try:
					for i in likes_qs:
						response[i.videofile.id].update({'liked_status':i.liked_status})
				except Exception as e:
					response[data.id].update({'liked_status':False})
			else:
				response[data.id].update({'liked_status':False})

			heart_qs = VideoHeart.objects.filter(videofile__id=data.id)
			if heart_qs:
				try:
					for i in heart_qs:
						response[i.videofile.id].update({'heart_status':i.heart_status})
				except Exception as e:
					response[data.id].update({'heart_status':False})
			else:
				response[data.id].update({'heart_status':False})

		return Response(response.values(), status=status.HTTP_200_OK)	

	""" def put(self, request):
		if not request.POST._mutable:
			request.POST._mutable = True
		pk =  request.GET.get('id')
		queryset = VideoFile.objects.get(id=pk)
		data = request.data 
		try:
			if data['video_file'] == '':
				del data['video_file']
				serializer = VideosSerialzers(queryset, data=data, partial=True)
			else:
				serializer = VideosSerialzers(queryset, data=data, partial=True)
		except:
			serializer = VideosSerialzers(queryset, data=data, partial=True)
		
		discription=data["video_discription"]

		if discription == '':
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		
		else:
			list_discription=discription.split(" ")
			extract_list=[]
			for list_item in list_discription:
				start_with_hash=re.search("^#",list_item)
				if start_with_hash:
					extract_list.append(list_item)
				else:
					pass
			for item in extract_list:
				if Hastag.objects.filter(name__iexact=item).exists():
					obj,created=Hastag.objects.get_or_create(count=1,user=request.user,name=item)
				else:
					obj,created=Hastag.objects.get_or_create(name=item,user=request.user)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """
		

	def delete(self, request):
		queryset = get_object_or_404(VideoFile, id=request.GET.get('id'))
		queryset.delete()
		return Response({"Message":"video file data hasbeen deleted successful"}, status=status.HTTP_204_NO_CONTENT)

class VideoLikeView(APIView):
	def post(self, request):
		pk =  request.GET.get('video_id')	
		queryset = VideoFile.objects.get(id=pk)
		data = request.data
		if int(data['like']) == 0:
			try:
				liked_obj = VideoLike.objects.get(videofile=queryset,user=request.user)
				liked_obj.delete()
				return Response({"status":True,
								"Message":"Unlike"}, status=status.HTTP_200_OK)
			except Exception as e:
				pass
		else:
			VideoLike.objects.create(videofile=queryset,user=request.user,liked_status=True)
			return Response({"status":True,
							"Message":"like"}, status=status.HTTP_200_OK)
		
		return Response({"status":False,
						"Message":"Please check your update data"}, status=status.HTTP_400_BAD_REQUEST)

class VideoCommentView(APIView):
	def post(self, request):
		pk =  request.GET.get('video_id')
		data = request.data
		queryset = VideoFile.objects.get(id=pk)
		VideoComment.objects.create(videofile=queryset,user=request.user,comment=data['comment'],comment_status=True)
		return Response({"Status":True,
							"Message":"Commented"}, 
							status=status.HTTP_201_CREATED)

	def get(self, request):
		pk =  request.GET.get('video_id')
		response = {}
		comments_qs = VideoComment.objects.filter(videofile__id=pk)
		for comment in comments_qs:
				response[comment.id]={
									"username": comment.user.username,
									"user_id": comment.user.id,
									"comment_id":comment.id,
									"comment": comment.comment,
									"comment_status": comment.comment_status,
									"videofile_id": comment.videofile.id,
									"created_at": comment.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
									}
		return Response(response.values(), status=status.HTTP_200_OK)

	def put(self, request):
		comment_pk = request.GET.get('comment_id')
		data = request.data
		comment_obj = VideoComment.objects.get(id=comment_pk,user=request.user)
		comment_obj.comment = data['comment']
		comment_obj.save()
		return Response({"Status":True,
							"Message":"updated Comment"},status=status.HTTP_200_OK)

	def delete(self, request):
		queryset = get_object_or_404(VideoComment, id=request.GET.get('comment_id'))
		queryset.delete()
		return Response({"Message":"comment has removed"}, status=status.HTTP_200_OK)

class VideoHeartView(APIView):
	def post(self, request):
		pk =  request.GET.get('video_id')	
		queryset = VideoFile.objects.get(id=pk)
		data = request.data
		if int(data['heart']) == 0:
			try:
				liked_obj = VideoHeart.objects.get(videofile=queryset,user=request.user)
				liked_obj.delete()
				return Response({"status":True,
								"Message":"unclicked heart"}, status=status.HTTP_200_OK)
			except Exception as e:
				pass
		else:
			VideoHeart.objects.create(videofile=queryset,user=request.user,heart_status=True)
			return Response({"status":True,
							"Message":"clicked heart"}, status=status.HTTP_200_OK)
		
		return Response({"status":False,
						"Message":"Please check your update data"}, status=status.HTTP_400_BAD_REQUEST)

class VideoShareView(APIView):
	def post(self, request):
		pk =  request.GET.get('video_id')
		queryset = VideoFile.objects.get(id=pk)
		VideoShare.objects.create(videofile=queryset,user=request.user,share_status=True)
		return Response({"status":True,
						"Message":"video shared successful"}, status=status.HTTP_200_OK)

class UserFollowView(APIView):
	def post(self, request, format="json"):
		follower_user = User.objects.get(id=self.request.user.id)
		following_user = User.objects.get(id=request.data.get('following'))
		unfollow = request.data.get('unfollow')
		if int(unfollow) == 0:
			user_follow_obj = FollowUser.objects.get(
							following=following_user,
							follower=follower_user
							)
			user_follow_obj.delete()
			return Response({"status":True,
							"message":"unfollowing"},status=status.HTTP_200_OK)
		else:
			response = FollowUser.objects.create(
								following=following_user,
								follower=follower_user)

			return Response({"status":True,
							"message":"following"},status=status.HTTP_200_OK)

	def get(self,request,format="json"):
		user = User.objects.get(username = request.user)
		my_follower_dict = {}
		my_followings_dict = {}
		my_follower = FollowUser.objects.filter(following=request.user)
		for user in my_follower:
			user_details = UserDetails.objects.get(user__id=user.follower.id)
			my_follower_dict[user.follower.username] = {
				"user_id":user.follower.id,
				"username": user.follower.username,
				"image":user_details.image.url if user_details.image else None,
				"created_at": user.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
			}

		my_following = FollowUser.objects.filter(follower=request.user)
		for user in my_following:
			user_details = UserDetails.objects.get(user__id=user.following.id)
			my_followings_dict[user.following.username] = {
				"user_id":user.following.id,
				"username": user.following.username,
				"image":user_details.image.url if user_details.image else None,
				"created_at": user.created_at.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d"),
			}
		response = {}
		response['followers'] = my_follower_dict.values()
		response['followings'] = my_followings_dict.values()

		return Response(response, status = status.HTTP_200_OK)


class Mp3Trim(APIView):
	
	def post(self,request):
		start_Min = request.data.get('startMin')
		start_Sec = request.data.get('startSec')
		end_Min = request.data.get('endMin')
		end_Sec = request.data.get('endSec')
		file = request.FILES['file']

		# Time to miliseconds
		startTime = int(start_Min)*60*1000+int(start_Sec)*1000
		endTime = int(end_Min)*60*1000+int(end_Sec)*1000
		trim_audio_total_time=(endTime - startTime)/1000


		# Opening file and extracting segment
		song = AudioSegment.from_mp3(file.file)
		extract = song[startTime:endTime]

		# Saving
		fs = FileSystemStorage(location='static/media/temp/') #defaults to   MEDIA_ROOT
		filename = fs.save(file.name, extract.export( 'static/media/temp/extract_{}'.format(file.name), format="mp3"))
		file_url = fs.path(filename)
		file_name = file_url.split('/')

		return Response({"cutting_mp3": '/media/temp/'+file_name[-1],"total_time_of_audio":trim_audio_total_time}, status=status.HTTP_200_OK)


'''compression function for video'''
def compression():
	location=settings.MEDIA_ROOT+"/temp"
	for files in os.listdir(location):
		endmp4=re.search(".mp4$",files)
		endwebm=re.search(".webm$",files)
		endavi=re.search(".avi$",files)
		try:
			if endmp4!=None:
				input_file=location+"/"+files
				output_file=settings.MEDIA_ROOT+"video"+"/"+files
				com_file = FFmpeg(inputs={input_file: None},outputs={output_file: '-crf 44'})
				com_file.run()
				return output_file
			

			if endwebm!=None:
				input_file=location+"/"+files
				output_file=settings.MEDIA_ROOT+"/video"+"/"+"compresssed_"+files
				com_file = FFmpeg(inputs={input_file: None},outputs={output_file: '-crf 44'})
				com_file.run()
				return output_file
			

			if endavi!=None:
				input_file=location+"/"+files
				output_file=settings.MEDIA_ROOT+"/video"+"/"+"compresssed_"+files
				com_file = FFmpeg(inputs={input_file: None},outputs={output_file: '-crf 44'})
				com_file.run()
				return output_file
			



		
		except:FileNotFoundError
		else:

			print("no any file found")


	return files


'''Delete temporary file form temp foleder'''
def temp_delete():
	media=settings.MEDIA_ROOT+"/temp"
	for files in os.listdir(media):
		endmp4=re.search(".mp4",files)
		endavi=re.search(".avi",files)
		endjpeg=re.search(".jpeg",files)
		try:

			if endwebm:
				os.remove(media+"/"+files)
			if endmp4:
				os.remove(media+"/"+files)
			if endavi:
				os.remove(media+"/"+files)
			
				
		except FileNotFoundError as e:
			print("raise error document not found:",e)
		else:
			print("no such file in temporary folder")


	return files



#Cannot resolve keyword 'document' into field. Choices are: audiofile, audiofile_id, created_at, id, status, user, user_id, video_file, videocomment, videofile_name, videoheart, videolike, videoshare
#Hash function
class Hash_Updata(APIView):

	def get(self, request, format="json"):
		pk = request.GET.get('id')
		user_id = request.GET.get('user_id')
		if pk:
			queryset = Hastag.objects.filter(id=pk)
		elif user_id:
			queryset = Hastag.objects.filter(user__id=user_id)
		else:
			queryset = Hastag.objects.all()
		response={}
		for data in queryset:
			response[data.id] = {
				"id": data.id,
				"user_id":data.user.id,
				"username":data.user.username,
				"hash_tag_name":data.name,
				"hash_tag_count":data.count,
				"hash_status":data.status,				
			}

		return Response(response.values(), status=status.HTTP_200_OK)
	
	def post(self,request,format='json'):
		if not request.POST._mutable:
			request.POST._mutable = True

		data = request.data
		data['status'] = True
		data['user'] = request.user.id
		serializer = HastagSerialzers(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request):
		if not request.POST._mutable:
			request.POST._mutable = True
		pk =  request.GET.get('id')
		queryset = Hastag.objects.get(id=pk)
		data = request.data 
		data['status'] = True
		data['user'] = request.user.id
		
		serializer = HastagSerialzers(queryset, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def delete(self, request):
		queryset = get_object_or_404(Hastag, id=request.GET.get('id'))
		queryset.delete()
		return Response({"Message":"audio file data hasbeen deleted successful"}, status=status.HTTP_204_NO_CONTENT)


class Finding_Video_By_Hashtag(APIView):
	def get(self, request, format="json"):
		pk = request.GET.get('id')
		user_id = request.GET.get('user_id')
		hashtag = request.GET.get('hastag')
		print(hashtag)
		if pk:
			queryset = VideoFile.objects.filter(id=pk)
		elif hashtag:
			#queryset = VideoFile.objects.filter(user__id=user_id)
			queryset = VideoFile.objects.filter(video_discription__iexact=hashtag)
			print(queryset)
		else:
			queryset = VideoFile.objects.filter(user__id=user_id)
		response={}

		for data in queryset:
			response[data.id] = {
				"id": data.id,
				"user_id":data.user.id,
				"username":data.user.username,
				"audiofile_name":data.audiofile.audiofile_name,
				"audio_file":data.audiofile.audio_file.url if data.audiofile.audio_file else None,
				"videofile_name":data.videofile_name,
				"video_file":data.video_file.url if data.video_file else None,
				"hash_tag":data.video_discription,
				
			}

		return Response(response.values(), status=status.HTTP_200_OK)


class language(APIView):
	def post(self, request, format="json"):
		data = request.data
		data['status'] = True
		serializer = LanguageSerialzers(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

	def get(self, request, format="json"):
		name = request.GET.get('name')
		if name:
			queryset = language.objects.filter(name=name)
		else:
			queryset = language.objects.all()
		response={}
		for data in queryset:
			response[data.id] = {
				"id": data.id,
				"name":data.name,
				"status":data.status,
				"created_at":data.created_at,
			}

		return Response(response.values(), status=status.HTTP_200_OK)

	

