import threading

from django.shortcuts import render
from users.models import ReferalCode, User
from users.serializers import (
    ReferalCodeSerializer,
    SignUpSerializer,
)
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import authentication
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from utils.helpers import generateUserOTP, sendUserActivationEmail, validateOTPCode
from utils.TokenGenerator import generateToken
from utils.SMSHelper import send_message
from utils.referals import onDepositForAReferedUser, onUserCreateReferalAction





class Me(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, telegram_id):
        try :
            user = User.objects.get(telegram_id= telegram_id)
        except:
            return Response(data={
                "message":"User is not logged in"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
                "message":"User is logged in"
            }, status=status.HTTP_200_OK)




class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    
    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        user = User.objects.filter(phone_number=request.data.get("phone_number"))
        if user.exists() and not user[0].is_active:
            return Response(
                data="Sorry User account is not activated",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            username=request.data.get("phone_number"), password=request.data.get("password")
        )
       


        if user is not None:
            user.telegram_id = telegram_id
            user.save()
            return Response(
                data={"data": SignUpSerializer(user).data, "token": user.auth_token.key, "message":"User login was successful"}
            )
        return Response(
            data={
                "message": "User Credentials are not correct",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )



class LogoutUser(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, user, telegram_id):
        try:
            user = User.objects.get(telegram_id = telegram_id)
        except User.DoesNotExist as e:
            return Response(data={"message":"User Log out was successful"}, status=status.HTTP_200_OK)
        user.telegram_id = None
        user.save()
        return Response(data={"message":"User Log out was successful"}, status=status.HTTP_200_OK) 
        