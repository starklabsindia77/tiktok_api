import requests
from sendotp import sendotp
from rest_framework.response import Response

access_key = "301307Avh9j3eGT55db92087"  

def sending_otp(otp,phone):
	otpobj =  sendotp.sendotp(access_key,	""" I LOVE YOU {{otp}} TIME, YOUR LOVER KHUSHBOO.KEEP IN TUCH AND TAKE CARE YOUR SELF""")
	res = otpobj.send(phone,'AnalogIt',otp)
	return res

#Use this OTP for confirmation please donot share with anyone