from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from User.models import User, OtpCode
from serializer import UserSerializer
from snaplist import settings


class CheckEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.has_usable_password():
                print(1)
                code = randint(10000, 99999)
                subject = 'SnapList Authentication'
                message = ''
                html_message = f"""
                                                <html>
                                                    <body style="text-align: center; font-family: Arial, sans-serif;">
                                                        <h1 style="font-size: 24px; font-weight: bold;">SnapList</h1>
                                                        <p style="font-size: 14px; margin-bottom: 20px;">Your authentication code in snaplist :</p>
                                                        <h2 style="font-size: 32px; font-weight: bold;">{code}</h2>
                                                        <p style="font-size: 12px; margin-bottom: 20px;">If this message is not relevant to you, ignore it</p>
                                                    </body>
                                                </html>
                                            """
                recipient_list = [email]
                try:
                    print(email, code)
                    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True,
                              html_message=html_message)
                    create_otp = OtpCode.objects.create(email=email, code=code)
                    print(email)
                    return Response({"meta": {"status-code": 202, "message": "user has not a password"}},
                                    status=status.HTTP_202_ACCEPTED)
                except Exception as e:
                    return Response({"meta": {"status-code": 500, "message": str(e)}},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(0)
                return Response({"meta": {"status-code": 201, "message": "user has a password"}},
                                status=status.HTTP_200_OK)
        else:
            code = randint(10000, 99999)
            subject = 'SnapList Authentication'
            message = ''
            html_message = f"""
                            <html>
                                <body style="text-align: center; font-family: Arial, sans-serif;">
                                    <h1 style="font-size: 24px; font-weight: bold;">SnapList</h1>
                                    <p style="font-size: 14px; margin-bottom: 20px;">Your authentication code in snaplist :</p>
                                    <h2 style="font-size: 32px; font-weight: bold;">{code}</h2>
                                    <p style="font-size: 12px; margin-bottom: 20px;">If this message is not relevant to you, ignore it</p>
                                </body>
                            </html>
                        """
            recipient_list = [email]
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True,
                          html_message=html_message)
                create_otp = OtpCode.objects.create(email=email, code=code)
                return Response({"meta": {"status-code": 200, "message": "OTP Code Sent"}},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"meta": {"status-code": 500, "message": str(e)}},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PutPassword(APIView):

    def put(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        user_serializer = UserSerializer(user)
        return Response({"meta": {"status-code": 200, "message": "password set"},
                         "data": {
                             "user": user_serializer.data}
                         },
                        status=status.HTTP_200_OK)


class CheckOtpCode(APIView):
    def post(self, request):
        code = request.data.get('code')
        email = request.data.get('email')

        check_otp_code = OtpCode.objects.filter(email=email).order_by('-id').first()

        if check_otp_code:
            if str(check_otp_code.code) == code:
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                else:
                    user = User.objects.create_user(email=email)

                access_token = AccessToken().for_user(user)
                refresh = RefreshToken.for_user(user)

                user_serializer = UserSerializer(user)
                return Response({"meta": {"status-code": 200, "message": "success"},
                                 "data": {
                                     "user": user_serializer.data,
                                     "access_token": str(access_token),
                                     "refresh_token": str(refresh)}
                                 },
                                status=status.HTTP_200_OK)
            else:
                return Response({"meta": {"status-code": 400, "message": "Wrong Code"}},
                                status=status.HTTP_400_BAD_REQUEST)


class LoginWithPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email)

        if user.check_password(password):
            access_token = AccessToken().for_user(user)
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({"meta": {"status-code": 200, "message": "success"},
                             "data": {
                                 "user": user_serializer.data,
                                 "access_token": str(access_token),
                                 "refresh_token": str(refresh)}
                             },
                            status=status.HTTP_200_OK)
        else:
            return Response({"meta": {"status-code": 400,
                                      "message": "Wrong Password"}},
                            status=status.HTTP_401_UNAUTHORIZED)
