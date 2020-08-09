from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tiktok_app.views import *

urlpatterns = [
				path('login/',Login.as_view(), name="user login"),
				path('resendotp/',ResendOTP.as_view(), name="resend Otp"),
				path('login_otp/',LoginOtpVerification.as_view(), name="login otp verification"),
				path('logout/',Logout.as_view(), name="user logout"),
				path('user_details/',User_Details.as_view(), name="get user details"),
				path('audioFile/',AudioViews.as_view(), name="audio files"),
				path('audio_search/',AudioSearch.as_view(), name="audio search files"),
				path('videos/',VideoViews.as_view(), name="video files"),
				path('videos_like/',VideoLikeView.as_view(), name="video like"),
				path('videos_heart/',VideoHeartView.as_view(), name="video heart"),
				path('videos_comment/',VideoCommentView.as_view(), name="video comment"),
				path('videos_share/',VideoShareView.as_view(), name="video share"),
				path('user_follow/',UserFollowView.as_view(), name='follow-user-post'),
				path('mp3_trim/',Mp3Trim.as_view(), name='follow-user-post'),
				path('hashtag/',Hash_Updata.as_view(),name="Hash_Updata"),
				path('language/',language.as_view(),name="language"),
				path('hash_video/',Finding_Video_By_Hashtag.as_view(),name="Finding_Video_By_Hashtag")				
			]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)