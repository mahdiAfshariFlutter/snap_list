from random import randint

import requests
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.test import Client
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from User.models import User, OtpCode
from serializer import UserSerializer
from snaplist import settings


class LoginRegister(APIView):
    def post(self, request):
        email = request.data.get('email')
        is_edit = request.data.get('is_edit')

        user = User.objects.filter(email=email)

        if is_edit is None:
            if user.exists():
                user_data = User.objects.get(email=email)
                if user_data.has_usable_password():
                    return Response({"meta": {"status-code": 200, "message": "user has a password"}},
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
                        print(email, code)
                        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True,
                                  html_message=html_message)
                        create_otp = OtpCode.objects.create(email=email, code=code)
                        print(email)
                        return Response(
                            {"meta": {"status-code": 201, "message": "user has not a password / otp code sent"}},
                            status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response({"meta": {"status-code": 500, "message": str(e)}},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                    print(email, code)
                    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True,
                              html_message=html_message)
                    create_otp = OtpCode.objects.create(email=email, code=code)
                    return Response({"meta": {"status-code": 404, "message": "user has not exists / otp code sent"}},
                                    status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({"meta": {"status-code": 500, "message": str(e)}},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif is_edit is True:
            if user.exists():
                return Response({"meta": {"status-code": 404, "message": "this email already exists"}},
                                status=status.HTTP_404_NOT_FOUND)
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
                    print(email, code)
                    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True,
                              html_message=html_message)
                    create_otp = OtpCode.objects.create(email=email, code=code)
                    return Response({"meta": {"status-code": 200, "message": "user has not exists / otp code sent"}},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"meta": {"status-code": 500, "message": str(e)}},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtpPass(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        password = request.data.get('password')

        change_email = request.data.get('change_email')

        if change_email is None:
            if email is not None and otp_code is not None and password is None:
                check_otp_code = OtpCode.objects.filter(email=email).order_by('-id').first()

                if check_otp_code:
                    if str(check_otp_code.code) == otp_code:
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
            elif email is not None and otp_code is None and password is not None:
                get_user = User.objects.filter(email=email)

                if get_user.exists():
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
                        return Response({"meta": {"status-code": 401,
                                                  "message": "Wrong Password"}},
                                        status=status.HTTP_401_UNAUTHORIZED)
        elif change_email is True:

            jwt_auth = JWTAuthentication()
            try:
                user, token = jwt_auth.authenticate(request)
                if user is None:
                    raise AuthenticationFailed('Authentication failed')
                request.user = user
            except AuthenticationFailed:
                return Response({"meta": {"status-code": 401, "message": "Authentication required"}},
                                status=status.HTTP_401_UNAUTHORIZED)
            #####
            check_otp_code = OtpCode.objects.filter(email=email).order_by('-id').first()

            if check_otp_code:
                if str(check_otp_code.code) == otp_code:
                    user = request.user
                    user.email = email

                    user.save()

                    access_token = AccessToken().for_user(user)
                    refresh = RefreshToken.for_user(user)

                    user_serializer = UserSerializer(user)

                    return Response({"meta": {"status-code": 200, "message": "email change success"},
                                     "data": {
                                         "user": user_serializer.data,
                                         "access_token": str(access_token),
                                         "refresh_token": str(refresh)}
                                     },
                                    status=status.HTTP_200_OK)


class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        email = request.data.get('email')
        avatar = request.data.get('avatar')
        user_name = request.data.get('user_name')
        password = request.data.get('password')

        if email is not None and avatar is None and password is None and user_name is None:
            if User.objects.filter(email=email).exists():
                return Response({"meta": {"status-code": 406, "message": "email is already exist"}},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                data_to_send = {'email': email, 'is_edit': True}

                response = requests.post('http://127.0.0.1:8000/login_register/', json=data_to_send)
                if response.headers.get('Content-Type') == 'application/json':
                    response_data = response.json()
                else:
                    raise ValueError(f"Unexpected Content-Type: {response.headers.get('Content-Type')}")

                return Response(response_data, status=response.status_code)
        else:
            user_data = request.user
            if user_name is not None:
                user_data.user_name = user_name
            if avatar is not None:
                user_data.avatar = avatar
            if password is not None:
                user_data.set_password(password)

            user_data.save()

            user_serializer = UserSerializer(user_data)
            return Response({"meta": {"status-code": 200, "message": "change set"},
                             "data": {
                                 "user": user_serializer.data}
                             },
                            status=status.HTTP_200_OK)
