from django.shortcuts import render
from .serializers import ReferializerSerilizer
from users.serializers import SignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Referal
from users.models import User



class GetUserReferals(APIView):
    def get(self, request):
        user = request.user
        referals = Referal.objects.filter(refered_by=user)
        return Response(data={
            "data":ReferializerSerilizer(referals, many=True).data
        }, status=status.HTTP_200_OK)