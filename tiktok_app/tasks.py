# from celery.decorators import task
# import requests
# from django.http import JsonResponse
# from celery.utils.log import get_task_logger
# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
# from celery import Celery
# import os


# logger = get_task_logger(__name__)

# @task(name="TikTok_App.TempFiles")
# def MP3TrimFilesRemoved():
# 	for roots,dirs,files in os.walk("./static/media/temp/save"):
# 		for file in files:
# 			if file.endswith(".mp3"):
# 				print(os.path.join(roots,file))
# 				os.remove(os.path.join(roots,file))
# 	return JsonResponse({"message":"Done"})