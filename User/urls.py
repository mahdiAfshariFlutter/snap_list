from django.urls import path

from User.views import CheckEmail, CheckOtpCode, LoginWithPassword, PutPassword

urlpatterns = [
    path('check_email/', CheckEmail.as_view()),
    path('check_code/', CheckOtpCode.as_view()),
    path('put_password/', PutPassword.as_view()),
    path('login_with_password/', LoginWithPassword.as_view()),
]
