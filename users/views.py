import threading

from django.shortcuts import render
from meals.models import Meal
from orders.models import Order
from referals.models import Referal
from users.models import ReferalCode, User
from users.serializers import (
    ReferalCodeSerializer,
    SignUpSerializer,
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from utils.EmailSender import actionNotificationEmail
from utils.helpers import generateUserOTP, sendUserActivationEmail, validateOTPCode
from utils.TokenGenerator import generateToken
from utils.referals import onDepositForAReferedUser, onUserCreateReferalAction



PER_PAGE =10


class Contact(APIView):
    permission_classes = [ permissions.AllowAny ]
    def post(self, request):
        data = request.data
        message = data.get('message')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        message =  f"Hi admin, a message was sent from {first_name} {last_name}. Here is the message: {message}"

        t = threading.Thread(target=actionNotificationEmail, kwargs={"name":"Admin", "to":"johnson@saharakitchen.co.uk", "message":message})
        t.start()
        return Response(data={
            "message":"Message sent successfully"
        }, status=status.HTTP_200_OK)
    
class SendUserMessage(APIView):
    def post(self, request):
        message = request.data.get("message")
        email = request.data.get("email")

        t = threading.Thread(target=actionNotificationEmail, kwargs={
            "name":"user",
            "to":email,
            "message":message
        })
        t.start()
        return Response(data={
            "message":"Message sent successfully"
        }, status=status.HTTP_200_OK)


class GetDashboardDetails(APIView):
    def get(self, request):
        users = User.objects.all()
        meals = Meal.objects.all()
        orders = Order.objects.all()
        pendingOrders = orders.filter(is_delivered=False)
        
        data ={
            "users": users.count(),
            "meals": meals.count(),
            "orders": orders.count(),
            "pending_orders": pendingOrders.count(),
        }

        return Response(data={"data":data}, status=status.HTTP_200_OK)

class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response(data={
            "data":{
                "data":SignUpSerializer(users, many=True).data,
            },
            "message":"Users retrieved successfully"
        }, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        s = SignUpSerializer(data=request.data)

        referalCode = request.data.get("referalCode")
        isRefered = False
        if referalCode and len(str(referalCode)) > 4:
            user = User.objects.filter(email = referalCode)
            if user.exists():
                isRefered=True
            else:
                return Response(data={
                    "message":"Referal code is invalid."
                }, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("email"):
            try:
                User.objects.get(email = request.data.get("email"))
                return Response(data={
                    "message":"User with this email already exists"
                }, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
        if s.is_valid():
            s.save()
            otp = generateUserOTP(request.data.get("email"))


            # t = threading.Thread(target=sendUserActivationEmail, args=(request.data.get("email"), request))
            # t.start()

            if isRefered:
                onUserCreateReferalAction(referalCode, s.data.get("email"))
            user = User.objects.get(email = request.data.get("email"))
            t = threading.Thread(target = actionNotificationEmail, kwargs={
                "name":f"{user.first_name} {user.last_name}",
                "to":user.email,
                "message":"Your account was created successfully"
            })
            t.start()
            return Response(data={"data":s.data, "message":"User account created successfully","token": user.auth_token.key,}, status=status.HTTP_200_OK)
        print(s.errors)
        return Response(data={"message": "Error creating user"}, status=status.HTTP_400_BAD_REQUEST)


class ResendUserEmailActivationCode(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        user =User.objects.filter(email=email)
        if not user.exists():
            return Response(
                data={"data": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    

        t = threading.Thread(target=sendUserActivationEmail, args=(request.data.get("email"), request))
        t.start()
        # sendUserActivationEmail(request.data.get("email"), request)

        return Response(
            data={
                "data": SignUpSerializer(user[0]).data,
                "message": "User registered successfully",
            },
            status=status.HTTP_200_OK,
        )


class ActivateUserEmail(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, token, uidb64):
        try:
            uuid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uuid)
        except Exception as e:
            user = None

        if user and generateToken.check_token(user, token):
            user.is_active = True
            user.email_verified=True
            user.save()

            return render(
                request,
                "notification.html",
                {
                    "message": "User account activated successfully, please return to the app to continue process",
                    "user":user
                },

            )

        return render(
            request,
            "notification.html",
            {"message": "Sorry, there was an error activating your account"},
        )



class VerifyUserOTP(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        code = request.data.get("code")

        validatingOTP = validateOTPCode(code)
        if not validatingOTP.get("type"):
            return Response(
                data={
                    "message": validatingOTP.get("message"),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user = validatingOTP.get("code").user
        user.is_active = True
        user.save()
        return Response(
            data={
                "message": "User account activated",
                "token":user.auth_token.key,
                "data":SignUpSerializer(user).data
            },
            status=status.HTTP_200_OK,
        )


class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    
    def post(self, request):
        user = User.objects.filter(email=request.data.get("email"))
        if user.exists() and not user[0].is_active:
            return Response(
                data="Sorry User account is not activated",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user =User.objects.filter(email = request.data.get("email"))
        if not user.exists():
            return Response(
                data={
                    "message": "User with this email does not exist",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = user[0]

       

        if user.check_password(request.data.get("password")):
            if request.data.get("admin") and not user.is_superuser:
                return Response(
                data={
                    "message": "User account not permitted to login",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

            return Response(
                data={"data": SignUpSerializer(user).data, "token": user.auth_token.key, "message":"User login was successful"}
            )
        
        return Response(
            data={
                "message": "User Credentials are not correct",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserMe(APIView):
   
    def get(self, request, id):
        user = User.objects.filter(id=id)

        if user.exists():
            return Response(
                data={"message": "User with this ID does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={
                "data": SignUpSerializer(instance=user[0]),
                "message": "User retrieved successfully",
            },
            status=status.HTTP_200_OK,
        )


class UserMeAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        return Response(
            data={"data":SignUpSerializer(user).data,"message":"User authenticated"}, status=status.HTTP_200_OK
        )

    def delete(self, request):
        id = request.user.id
        user = User.objects.get(id=id).delete()

        return Response(
            data={
                "messgae": "User Deleted Successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutUser(APIView):
    permission_classes = [ permissions.AllowAny ]
    def get(self, request):
        logout(request=request)
        return Response(data={"message": "User Logged Out Successfully"})


class GetUserReferalCode(APIView):
    def get(self, request):
        r = ReferalCode.objects.get(user=request.user)
        return Response(data=ReferalCodeSerializer(r).data, status=status.HTTP_200_OK)



class ForgotPasswordRequest(APIView):
    permission_classes = [permissions.AllowAny ]
    def post(self, request):
        email = request.data.get("email")


        user = User.objects.filter(email= email)

        if not user.exists():
            return Response(
            data={
                "error": "Sorry, User with this email does not exist",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

        otp = generateUserOTP(email)

        

        body = f"Thanks for signing up below is your OTP Code \n {otp}"
        to_number = email
        thread = threading.Thread(target=sendUserActivationEmail, kwargs={"email":email, "request":request})
        thread.start()




       

        
        return Response(
            data={
                "message": f"Forgot password sent successfully",
            },
            status=status.HTTP_200_OK,
        )


class ContinueForgotPassword(APIView):

    permission_classes = [ permissions.AllowAny ]
    def post(self, request):
        password = request.data.get("password")
        email = request.data.get("email")

        try:
            user = User.objects.get(email = email )
        except:
            return Response(
            data={
                "message": "User with this email does not exist",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


     


        user.password = make_password(password)
        user.save()

        return Response(
            data={
                "message": "User password updated successfully",
            },
            status=status.HTTP_200_OK,
        )




class CheckUserPassword(APIView):
    def post(self, request):
        user = request.user
        user = User.objects.get(email = user.email)
        password = request.data.get("password")

        if user.check_password(password):
            return Response(data={
                "data":SignUpSerializer(user).data,
                "message":'User password is correct'
            },
            status=status.HTTP_200_OK
            )
        
        return Response(data={
                "message":'User password is not correct'
            },
            status=status.HTTP_400_BAD_REQUEST
            )




class DeleteUserAccount(APIView):
    def delete(self, request):
        user = request.user
        user = User.objects.get(phone_number = user.phone_number).delete()
        return Response(data={"message":"Account deleted successfully"}, status=status.HTTP_202_ACCEPTED)
    



class ChangePassword(APIView):
     def patch(self, request):
        new_password = request.data.get("new_password")
        old_password = request.data.get("old_password")

        user = User.objects.get(id = request.user.id)
        if not user.check_password(old_password):
            return Response(data={"message":"Your old password is not verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        # user.save()


        return Response(data={
            "data":SignUpSerializer(user).data,
            "message":"User password updated"
        }, status=status.HTTP_200_OK)


class UpdateUserProfile(APIView):
    def patch(self, request):
        data = request.data
        print(data)
        user = User.objects.get(id = request.user.id) 
        serializer = SignUpSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "user":serializer.data,
                "message":"User updated successfully"
            }, status=status.HTTP_200_OK)
        
        return Response(data={
            "message":"User was not updated successfully"
        }, status=status.HTTP_400_BAD_REQUEST)