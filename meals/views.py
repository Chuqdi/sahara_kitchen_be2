from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from categories.models import Category
from meals.models import Meal
from meals.serializers import MealSerializer
from rest_framework.views import APIView

class UpdateDeleteMeal(APIView):
    def delete(self, request, meal_id):
        try:
            meal = Meal.objects.get(id=meal_id)
        except:
            return Response(data={
                "message":"Meal does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        meal.delete()
        return Response(data={
            "message":"Meal deleted"
        }, status=status.HTTP_200_OK)

    def patch(self, request, meal_id):
        
        data = {
            "price":request.data.get("price"),
            "name":request.data.get("name"),
            "description":request.data.get("description"),
            "photo":request.data.get("photo"),
            "is_in_stock":request.data.get("is_in_stock"),
        }
        try:
            meal = Meal.objects.get(id=meal_id)
        except:
            return Response(data={
                "message":"Meal does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        category_id = request.data.get("category_id")
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response(data={
                "message":"Category does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(data)
        data["category"] =category_id
        is_in_stock= data.get("is_in_stock")
        if is_in_stock == "0":
            data["is_in_stock"] = False
        else:
            data["is_in_stock"] = True
        
        if not data.get("photo") or data.get("photo") == "null":
            data.pop("photo")
        serializer = MealSerializer(instance=meal, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateGetMeals(APIView):

    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(data={
            "data":{
                "data":serializer.data
            }
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        data = request.data
   
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response(data={
                "message":"Category does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        data["category"] =category.id

        serializer = MealSerializer(data=data)  

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
