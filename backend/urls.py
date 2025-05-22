
import threading
from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from utils.EmailSender import testEmail


ROOT_URL="api/v1/"


class SendTestEmail(APIView):
    permission_classes = [ AllowAny ]
    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        message = request.data.get("message")
        
        email_message = f"""
        You recieved a message from dean hurst thompson website.\n\n
        Name: {first_name} {last_name}\n\n
        Email: {email}\n\n
        message: {message}\n\n
        
        """
        
        t = threading.Thread(target=testEmail, kwargs={
            "name":f"Dean hurst thompson",
            "to":"morganhezekiah111@gmail.com",
            "message":email_message
        })
        t.start()
        
        return Response(data={
                "message":"Message sent",
            }, status=status.HTTP_200_OK)



urlpatterns = [
    path('admin/', admin.site.urls),
    path(ROOT_URL + "users/", include("users.urls")),
    path(ROOT_URL + "test_email", SendTestEmail.as_view()),
    path(ROOT_URL + "addresses/", include("addresses.urls")),
    path(ROOT_URL + "categories/", include("categories.urls")),
    path(ROOT_URL + "meals/", include("meals.urls")),
    path(ROOT_URL + "payments/", include("payments.urls")),
    path(ROOT_URL + "orders/", include("orders.urls")),
]
