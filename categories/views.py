from django.shortcuts import render
from meals.models import Meal
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from categories.GetSerializers import GetCategorySerializer
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework import permissions
from django.db.models import Q




class GetCategoriesWithMeal(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        search = request.GET.get('search', "")
        querySet = Category.objects.filter(
            Q(name__icontains=search)
      
        )
    
        return Response (
            status=status.HTTP_200_OK,
            data={
                "data":GetCategorySerializer(querySet, many=True).data
            }
        )



class AddGetCategory(APIView):
    def get(self, request):
        categories = Category.objects.all()
        return Response (
            status=status.HTTP_200_OK,
            data={
                "data":CategorySerializer(categories, many=True).data
            }
        )
    def post(self, request):
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(status=200, data="Category created")