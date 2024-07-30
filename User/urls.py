from django.urls import path

from User.views import UpdateUser, OtpPass, LoginRegister, GetUser

urlpatterns = [
    path('login_register/', LoginRegister.as_view()),
    path('otp_pass/', OtpPass.as_view()),
    path('user/', UpdateUser.as_view()),
    path('user_info/', GetUser.as_view()),
]
